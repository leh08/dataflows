import os
# from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# load_dotenv(".env")
DATABASE_URL = os.getenv('DATABASE_URL') or os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         expire_on_commit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models.source import SourceModel
    from models.authorization import AuthorizationModel
    from models.log import LogModel
    from models.flow import FlowModel
    from models.user import UserModel
    from models.confirmation import ConfirmationModel

    Base.metadata.create_all(bind=engine)
   
def restart_db():
    from models.source import SourceModel
    from models.authorization import AuthorizationModel
    from models.log import LogModel
    from models.flow import FlowModel
    from models.user import UserModel
    from models.confirmation import ConfirmationModel
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create the fixtures
    s3 = SourceModel(name='S3')
    s3.save_to_db()
    google = SourceModel(name='Google')
    google.save_to_db()
    database = SourceModel(name='Database')
    database.save_to_db()
    file = SourceModel(name='File')
    file.save_to_db()
    
    default_credential = AuthorizationModel(
        name='Default',
        credential={
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"]
        },
        source = s3
    )
    default_credential.save_to_db()
    
    admin = UserModel(email="admin", password="123456")
    admin.save_to_db()
    new_confirmation = ConfirmationModel(user_id=admin.id)
    new_confirmation.save_to_db()
    new_confirmation.confirmed = True
    new_confirmation.save_to_db()
    
    flow = FlowModel(
        name = "name",
        report = "report",
        profile = "profile",
        parser_name = "parser_name",
        store_name = "store_name",
        day_unit = "Monday",
        time_unit = 6,
        sql_script = "sql_script",
        source_name = "S3",
        authorization_id = 1,
    )
    flow.save_to_db()
    