import os
from sqlalchemy import create_engine, text


class Redshift:
    def __init__(self):
        self.engine = self.get_engine()
    
    def get_engine(self):
        return create_engine(os.environ["SQLALCHEMY_COLUMNAR_DATABASE_URI"])
    
    def copy(self, table_name, blob_key, columns ,schema='public'):
        try:
            schema = '"{}"'.format(schema)
            table = '"{}"'.format(table_name)
            columns = ', '.join('"{}"'.format(column) for column in columns)

            query = '''
                COPY {}.{} ({})
                FROM '{}'
                IAM_ROLE 'arn:aws:iam::142255444761:role/Redshift'
                REMOVEQUOTES
                DELIMITER '\t'
                GZIP
                IGNOREHEADER 1
                MAXERROR 20;
            '''.format(schema, table, columns, blob_key)
            
            with self.engine.connect() as con:
                con.execute(text(query).execution_options(autocommit=True))
                
            return True
        
        except Exception as err:
            print(err)
            
            return False   
        
    def execute(self, query):
        try:
            with self.engine.connect() as con:
                con.execute(text(query).execution_options(autocommit=True))
                
            return True
        
        except Exception as err:
            print(err)
            
            return False