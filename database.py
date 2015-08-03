from sqlalchemy import Column, Integer, Text, ForeignKey, create_engine, SmallInteger
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Timestamp(Base):
    __tablename__ = 'timestamps'
    timestamp = Column(Text, unique=True)
    ROWID = Column(Integer, autoincrement=True, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    name = Column(Text, unique=True)
    ROWID = Column(Integer, autoincrement=True, primary_key=True)

class Datapoint(Base):
    __tablename__ = 'datapoints'
    timestamp_id = Column(Integer, ForeignKey(Timestamp.ROWID), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.ROWID), primary_key=True)
    status = Column(Integer)
    timestamp = relationship('Timestamp', foreign_keys="Datapoint.timestamp_id")
    user = relationship('User', foreign_keys="Datapoint.user_id")


def get_session() -> sqlalchemy.orm.session.Session:
    db_path = "datastore.db"
    engine = create_engine('sqlite:///' + db_path)
    Base.metadata.create_all(engine)
    session = sessionmaker()
    session.configure(bind=engine)
    return session()


session = get_session()
