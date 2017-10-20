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
from createTable import *

##############authorization##################
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
################################################

# Return engine instances to create tables. 
def createEngine(user, password, ip, database):
    query = 'mysql+pymysql://' + user + ':' + str(password) + '@' + str(ip) + '/' + database
    try:
        engine = create_engine(query)
    except sqlalchemy.exc.DatabaseError:
        print("Can't connect mysql.")
    return engine

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
# Base.metadata.create_all(engine)