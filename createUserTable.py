import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from binstar_client.requests_ext import NullAuth


# Return session instances. 
def createSession(user, password, ip, database):
    query = 'mysql+pymysql://' + user + ':' + str(password) + '@' + str(ip) + '/' + database
    try:
        engine = create_engine(query)
    except sqlalchemy.exc.DatabaseError:
        print("Can't connect mysql.")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Return engine instances to create tables. 
def createEngine(user, password, ip, database):
    query = 'mysql+pymysql://' + user + ':' + str(password) + '@' + str(ip) + '/' + database
    try:
        engine = create_engine(query)
    except sqlalchemy.exc.DatabaseError:
        print("Can't connect mysql.")
    return engine

    

#create Base object
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
    
    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == "__main__":
    local = ['root', '1234', 'localhost', 'rna_seq2']
    serve = ['ironwood', 'irtest', '172.20.203.118:3306', 'rna_seq2']
    serve_local = ['ironwood', 'irtest', 'localhost', 'rna_seq2']
    server = local

    session = createSession(*server)
    
    #create tables
    engine = createEngine(*server)
    Base.metadata.create_all(engine)