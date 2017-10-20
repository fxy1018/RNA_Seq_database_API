#User api

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase
from numba.cuda.api import synchronize


auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    isExist = session.query(User).filter(User.username == username).scalar()
    if isExist:
        return(session.query(User.password).filter(User.username == username).scalar())
    return(None)

@auth.error_handler
def unauthorized():
    return(make_response(jsonify({'error': 'Unauthorized access'}), 403))

# Return engine instances to create tables. 
def createEngine(user, password, ip, database):
    query = 'mysql+pymysql://' + user + ':' + str(password) + '@' + str(ip) + '/' + database
    try:
        engine = create_engine(query)
    except sqlalchemy.exc.DatabaseError:
        print("Can't connect mysql.")
    return engine

#create Base object
Base = declarative_base(cls=(JsonSerializableBase,))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100))
 
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


local = ['root', '1234', 'localhost', 'rna_seq2']
server = local

session = createSession(*server)
    
#create tables
engine = createEngine(*server)
Base.metadata.create_all(engine)
users = session.query(User).all()





###########Users Access Right Api##################
user_fields = {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
    'uri': fields.Url('user')
    }

class UserAPI(Resource):
    decorators = [auth.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, location = 'json')
        self.reqparse.add_argument('password', type = str, location = 'json')
        self.reqparse.add_argument('email', type = str, location = 'json')
        super(UserAPI, self).__init__()
        
    def get(self,id):
        isExist = session.query(User.id).filter(User.id == id).scalar()
        if not isExist:
            abort(404)
        else:
            user = session.query(User).filter(User.id == id).all()[0]
        return({'user': marshal(user,user_fields)}, 201)
    
    def put(self,id):
        isExist = session.query(User.id).filter(User.id == id).scalar()
        if not isExist:
            abort(404)

        args = self.reqparse.parse_args()
        print(args, file=sys.stdout)
        session.query(User).filter(User.id == id).update(args)
        session.commit()
        
        args['id'] = id
        return({'user': marshal(args, user_fields)}, 201)
        
    def delete(self,id):
        isExist = session.query(User.id).filter(User.id == id).scalar()
        if not isExist:
            abort(404)
        session.query(User).filter(User.id == id).delete(synchronize_session = False)
        session.commit()
        return({'result': True})
        
class UserListAPI(Resource):
    decorators = [auth.login_required]
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,
            help = 'Username to create user', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'Password to create user', location = 'json')
        self.reqparse.add_argument('email', type = str, default = '',
            help = 'Email to create user', location = 'json')
        super(UserListAPI, self).__init__()
    
    
    def post(self):
        args = self.reqparse.parse_args()
        tmp_user = {
            'username': args['username'],
            'password': args['password'],
            'email': args['email']
            }
        
        isExist = session.query(User.id).filter(User.username == tmp_user['username']).scalar()
        if not isExist:
            user = User(username = tmp_user['username'], password = tmp_user['username'], email = tmp_user['email'])
            session.add(user)
            session.commit()
            tmp_user['id'] = session.query(User.id).filter(User.username == tmp_user['username']).scalar() 
        else:
            abort(400)
        return({ 'user': marshal(tmp_user, user_fields)}, 201)
    
    def get(self):
        return({'users': [marshal(user, user_fields) for user in users]})
