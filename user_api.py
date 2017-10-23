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
from table_model import *
from createTable import *

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
        users = session.query(User).all()
        return({'users': [marshal(user, user_fields) for user in users]})
