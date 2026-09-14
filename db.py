from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    "mysql+pymysql://3jGEK1pwgArGM7j.root:S9HJptwoc7sdiT6f@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": r"C:\Users\vaish\Downloads\isrgrootx1.pem"
        }
    },
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()