import os
import io
import re
import gzip
from concurrent.futures import ThreadPoolExecutor

from services.log import create_logger
from services.filesystem import FileSystem

from components.sources import get_source
from components.parsers import get_parser
from components.stores import get_store


class Flow:
    def __init__(
        self, name, report, profile,
        parser_name, store_name, is_model, schema,
        load_mode, frequency, hour, day,
        sql_script, source_name, authorization, logs,
        **kwargs
    ):  
        self.name = name
        self.report = report
        self.source_name = source_name
        self.authorization = authorization
        self.profile = profile
        self.parser_name = parser_name
        self.is_model = is_model
        self.store_name = store_name
        self.schema = schema
        self.load_mode = load_mode
        self.frequency = frequency
        self.hour = hour
        self.day = day
        self.sql_script = sql_script
        self.logs = logs

    def run(self):
        self.logger = create_logger(self.name)
        self.fs = FileSystem(authorization_name="Default")
        self.source = get_source(self.source_name, self.authorization.get('credential'))
        self.parser = get_parser(self.parser_name)
        self.store = get_store(self.store_name)
        
        file_list = self.discover()
        processed_files = [log['file'] for log in self.logs if log.get('status') == 'Success']
        to_process = [file_id for file_id in file_list if file_id not in processed_files]

        if to_process:
            self.logger.info("Found new report! Start to process.")
            self.blob_root = "s3://" + os.environ["DATA_LAKE_NAME"] + '/' + self.schema + '/' + self.name + '/'
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
        blob_key = self.blob_root + 'log' + '/' + file_id
        extension = re.search('[.].+$', file_id).group()
        
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
            blob_key = self.blob_root + 'model' + '/' + file_id
            df = self.model(df) 
            
        else:
            blob_key = self.blob_root + 'data' + '/' + file_id
    
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
            self.logger.extra['file'] = file_id
            if is_success:
                self.logger.extra['status'] = "Success"
                self.logger.info("File {} succeed to insert into a table".format(file_id))
            else:
                self.logger.extra['status'] = "Failure"
                self.logger.info("File {} fail to insert into a table".format(file_id))