#Condition DATA API

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


condition_fields = {
    'id':fields.Integer,
    'name': fields.String,
    'experiment_id': fields.Integer, 
    'description': fields.String,
    }

class ConditionAPI(Resource):
#     decorators = [auth.login_required] 
    def get(self,exp_id, condition_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)
        else:
            condition = session.query(Condition).\
                        filter(Condition.experiment_id == exp_id).\
                        all()[0]
                    
        return({'condition': marshal(condition,condition_fields)}, 201)
    
 
class ConditionListAPI(Resource):
#     decorators = [auth.login_required]
    def get(self, exp_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)
        else:
            conditions_tmp = session.query(Condition, Experiment).\
                        join(Experiment, Experiment.id == Condition.experiment_id).\
                        filter(Condition.experiment_id == exp_id).\
                        all()
            conditions = []
            for t in conditions_tmp:
                tmp_dict = {}
                tmp_dict['id'] = t[0].id
                tmp_dict['name'] = t[0].name
                tmp_dict['experiment_id'] = t[0].experiment_id
                tmp_dict['description'] = t[1].description
                conditions.append(tmp_dict)
        return({'conditions': [marshal(condition, condition_fields) for condition in conditions]}, 201)
#         experiments = session.query(Experiment).all()
#         return({'experiments': [marshal(experiment, experiment_fields) for experiment in experiments]})
