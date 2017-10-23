#Experiment DATA API

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

experiment_fields = {
    'description': fields.String,
    'date': fields.DateTime(dt_format='rfc822'),
    'tech': fields.String,
    'comments': fields.String,
    'mim_read_length': fields.String,
    'species_id': fields.String,
    'uri': fields.Url('experiment')  
    }

class ExperimentAPI(Resource):
    decorators = [auth.login_required]
        
    def get(self,id):
        isExist = session.query(Experiment.id).filter(Experiment.id == id).scalar()
        if not isExist:
            abort(404)
        else:
            experiment = session.query(Experiment).filter(Experiment.id == id).all()[0]
        return({'experiment': marshal(experiment,experiment_fields)}, 201)
    
 
class ExperimentListAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        experiments = session.query(Experiment).all()
        return({'experiments': [marshal(experiment, experiment_fields) for experiment in experiments]})
