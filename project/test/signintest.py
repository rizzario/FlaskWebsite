from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/NHKDB'

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(username='kitipong', password='1234')
session.add(new_user)
session.commit()

user = session.query(User).first()
print(user.username)

session.close()