# Sample api to get sample table data
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

sample_fields = {
    'id': fields.Integer,
    'sample_name': fields.String,
    'tissue_id': fields.Integer,
    'experiment_id': fields.Integer,
    'condition_id': fields.Integer
    }


class SampleAPI(Resource):
    def get(self, exp_id, sample_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)
        else:
            sample = session.query(Sample).filter(Sample.id == sample_id).all()[0]
        return({'sample': marshal(sample,sample_fields)}, 201)
    
class SampleListAPI(Resource):
    def get(self, exp_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)
        else:
            samples = session.query(Sample).filter(Sample.experiment_id == exp_id).all()
        return({'sample': marshal(samples,sample_fields)}, 201)
     