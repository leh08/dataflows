#from typing import List
#from database import Base, db_session
#from sqlalchemy import Column, Integer, String, ForeignKey
#from sqlalchemy.orm import relationship
#
#
#class FlowModel(Base):
#    __tablename__ = "flows"
#    
#    id = Column(Integer, primary_key=True)
#    name = Column(String(80), nullable=False, unique=True)
#    report = Column(String(80))
#    
#    user_id = Column(Integer, ForeignKey("users.id"))
#    
#    logs = relationship('LogModel', lazy="dynamic")
#        
#    @classmethod
#    def find_by_id(cls, _id: int) -> "FlowModel":
#        return cls.query.filter_by(id=_id).first()
#
#    @classmethod
#    def find_by_name(cls, name: str) -> "FlowModel":
#        return cls.query.filter_by(name=name).first()
#
#    @classmethod
#    def find_all(cls) -> List["FlowModel"]:
#        return cls.query.all()
#
#    def save_to_db(self) -> None:
#        db_session.add(self)
#        db_session.commit()
#
#    def delete_from_db(self) -> None:
#        db_session.delete(self)
#        db_session.commit()

from typing import List
from database import Base, db_session
from models.log import LogModel
from log.logger import get_logger
from filesystem import FileSystem
from parsers.pandas_parser import PandasParser
from stores.redshift import Redshift
from scheduler import scheduler
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from datetime import datetime, date, time, timedelta
from concurrent.futures import ThreadPoolExecutor

import re
import gzip
import io


class FlowModel(Base):
    __tablename__ = 'flows'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    report = Column(String, nullable=False)
    profile = Column(String)
    parser_name = Column(String, default="Pandas")
    target = Column(String, default="Redshift") # Target: "Redshift", "S3-Only"
    is_model = Column(Boolean, default=False)
    schema = Column(String, default='public')
    load_mode = Column(String, default='Replace') # Load mode: Append, Replace, Upsert
    frequency = Column(String, default='Daily') # Frequency: Daily, Weekly, Minutes, Hours, Days, Weeks
    day_unit = Column(String)
    time_unit = Column(Integer)
    sql_script = Column(String)
    status = Column(String, default='Active')
    created_on = Column(DateTime, default=func.now())

    source_id = Column(Integer, ForeignKey('sources.id'))
    source = relationship('SourceModel')
    
    authorization_id = Column(Integer, ForeignKey('authorizations.id'))
    authorization = relationship('AuthorizationModel')
    
    logs = relationship('LogModel', lazy='dynamic', cascade='delete,all')
    
    @property
    def most_recent_log(self) -> "LogModel":
        return self.logs.order_by(LogModel.date.desc()).first()
    
    def get_all_logs_by_status(self, status):
        self.logs.filter_by(status=status).all()
        
    @classmethod
    def find_by_id(cls, _id: str) -> "FlowModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["FlowModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()
        
    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
    
    def schedule(self):
        params = dict()
        
        if self.frequency == 'Daily':
            params['days'] = 1
            params['next_run_time'] = datetime.combine(date.today() + timedelta(1), time(self.time_unit))
            
        else:
            raise ValueError("A frequency, " + self.frequency + ", wasn't set up to run in this system.")
            
        scheduler.add_job(self.run, id=str(self.id), trigger='interval', **params)


    def run(self):
        self.logger = get_logger(self.id, status="In Progress")
        self.fs = FileSystem()
        self.service = self.get_service()
        self.parser = self.get_parser()
        self.store = self.get_store()
    
        file_list = self.discover(self.report)
        processed_logs = self.get_all_logs_by_status("Success")
        to_process = [file_id for file_id in file_list if file_id not in processed_logs]
        
        if to_process:
            self.logger.info("Found new report! Start to process.")
            self.blob_root = "s3://phdmedia-nz-dw" + '/' + self.schema + '/' + self.name + '/'
            self.sql_table = None
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                results = dict(
                    zip(file_list, executor.map(self.etl, to_process))
                )
                
            self.verify(results)
    
    
    def etl(self, file_id):
        # Check unprocessed files
        logger = self.logger
        logger.extra['file'] = file_id
        file_name = self.generate_file_name(file_id)
        blob_key = self.blob_root + 'log' + '/' + file_name
        extension = re.search('[.].+$', file_name).group()
        
        stream = self.extract(file_id)
        
        if stream:
            logger.info("File {} has been extracted.".format(file_id))
            
        else:
            logger.extra['status'] = 'Failed'
            logger.exception("Fail to extract {} file!!".format(file_id))
            
        self.fs.cloud_upload(stream, blob_key)
        logger.info("File {} has been copied to {}.".format(file_id, blob_key))
        
        df = self.transform(stream, extension)
        logger.info("File {} succeed to transform.".format(blob_key))
        
        if self.is_model:
            blob_key = self.blob_root + 'model' + '/' + file_name
            df = self.model(df) 
            
        else:
            blob_key = self.blob_root + 'data' + '/' + file_name

        return {file_id: self.load(df, blob_key)}
    
    
    def discover(self):
        raise NotImplementedError("Subclass must implement instance method")
    
    
    def extract(self, file_id):
        raise NotImplementedError("Subclass must implement instance method")
        
    
    def transform(self, stream):
        raise NotImplementedError("Subclass must implement instance method")
    
    
    def model(self, df):
        pass
    
        
    def load(self, df, blob_key):
        # When you develope real data warehouse architect with ORM, look into
        # how to combine Pandas and SQLAlchemy.
        blob_key = blob_key + '.gz'
        bytes_buffer = io.BytesIO()
        with gzip.open(bytes_buffer, 'wb') as file:
            file.write(df.to_csv(sep="\t", index=False).encode())
            
        self.fs.cloud_upload(bytes_buffer.getvalue(), blob_key)
        
        # Create empty table
        table_name = self.name.lower()
        staging_table_name = table_name + '_' + 'staging'
        columns = df.columns
        
        if self.sql_table is None:
            # Obtain SQL table object
            self.sql_table = df[:0]
            # Create staging table
            self.sql_table.to_sql(
                staging_table_name,
                con=self.store.engine,
                schema=self.schema,
                if_exists='replace',
                index=False
            )
            # Update table
            self.sql_table.to_sql(
                    table_name,
                    con=self.store.engine,
                    schema=self.schema,
                    if_exists='append',
                    index=False
                )
        return self.store.copy(staging_table_name, blob_key, columns, schema=self.schema)
        
          
    def verify(self, results):
        table_name = self.name.lower()
        staging_table_name = table_name + '_' + 'staging'
        
        schema = '"{}"'.format(self.schema)
        table = '"{}"'.format(table_name)
        staging_table = '"{}"'.format(staging_table_name)
        columns = ', '.join('"{}"'.format(column) for column in self.sql_table.columns)
        
        try:
            if self.load_mode == "Replace":
                query = """
                    DROP TABLE IF EXISTS {schema}.{table};
                    ALTER TABLE {schema}.{staging_table} RENAME TO {table};
                """.format(schema=schema, staging_table=staging_table, table=table)
                self.store.execute(query)

            elif self.load_mode == "Append":
                query = """
                    INSERT INTO {schema}.{table} ({columns})
                    SELECT * FROM {schema}.{staging_table};
                    DROP TABLE {schema}.{staging_table};
                """.format(schema=schema, table=table, columns=columns, staging_table=staging_table)
                self.store.execute(query)

            else:
                raise ValueError("A load mode, " + self.load_mode + ", wasn't set up to run in this system.")
                
        except:
            raise
            
            
        for file_id, is_success in results.items():
            if is_success:
                logger = get_logger(self.name, status="Success", file=file_id, flow_id=self.id)
                logger.info("the result of flow.")
            else:
                logger = get_logger(self.name, status="Failure", file=file_id, flow_id=self.id)
                logger.info("the result of flow.")
    
    
    def get_service(self):
        """ Get a source API for retrieve a report """
        source_name = self.source.name
        credential = self.authorization.credential

        if source_name == "S3":
            return FileSystem(credential=credential)
        
        else:
            raise ValueError("A source, " + source_name + ", wasn't set up to run in this system.")
    
    
    def get_parser(self):
        """ Get a parser for preparing and transforming a report """
        parser_name = self.parser_name
        
        self.logger.info(parser_name)
        if parser_name == 'Pandas':
            return PandasParser()
        
        else:
            raise ValueError("A parser, " + parser_name + ", wasn't set up to run in this system.")
            
            
    def get_store(self):
        target = self.target
        
        if target == 'Redshift':
            return Redshift()
        
        else:
            raise ValueError("A target, " + target + ", wasn't set up to run in this system.")
        
    
    def generate_file_name(self):
        raise NotImplementedError("Subclass must implement instance method")
