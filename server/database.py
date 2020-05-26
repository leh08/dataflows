import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

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
    from models.flow import FlowModel
    from models.log import LogModel
    from models.user import UserModel
    from models.confirmation import ConfirmationModel
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures
    s3 = SourceModel(name='S3')
    db_session.add(s3)
    google = SourceModel(name='Google')
    db_session.add(google)
    database = SourceModel(name='Database')
    db_session.add(database)
    file = SourceModel(name='File')
    db_session.add(file)
    db_session.commit()
    
    default_credential = AuthorizationModel(
        name='PHD Media',
        credential={
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"]
        },
        source = s3
    )
    db_session.add(default_credential) 
    db_session.commit()