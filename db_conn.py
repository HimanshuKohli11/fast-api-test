# import urllib.parse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# DATABASE_URL="postgres://thqzghojnxgfvi:e7db00a08fd236f0e15d1ccfefb41d9891b3d0c03cc6ba9a46db3786f24884af@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d2vbttev840ial
# "

# engine = create_engine(DATABASE_URL, echo=True)
# Base = declarative_base()
# SessionLocal = sessionmaker(bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db

#     except Exception as e:
#         print("Exception Occurred!! {0}".format(e))
#         db.close()
