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

gene_fields = {
    'id': fields.Integer,
    'sample_id': fields.String,
    'ensembl_id': fields.String,
    'expression': fields.Float
    }

class GeneExpAPI(Resource):
    def get(self, exp_id, gene_id):
        isExistExp = session.query(Experiment).filter(Experiment.id == exp_id).scalar()
        isExistGene = session.query(GeneExpressionTPM.id).filter(GeneExpressionTPM.ensembl_id == gene_id).all()
        if not isExistExp and not isExistGene:
            abort(404)
        else:
            samples = session.query(Sample.id).filter(Sample.experiment_id==exp_id).all()
            samples_id = [s[0] for s in samples]
            gene = session.query(GeneExpressionTPM).filter(GeneExpressionTPM.ensembl_id == gene_id, GeneExpressionTPM.sample_id.in_(samples_id)).all()
        return({'gene': marshal(gene,gene_fields)}, 201)
        

class GeneExpListAPI(Resource):
    def get(self, exp_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)
        else:
            samples = session.query(Sample.id).filter(Sample.experiment_id==exp_id).all()
            samples_id = [s[0] for s in samples]
            genes = session.query(GeneExpressionTPM).filter(GeneExpressionTPM.sample_id.in_(samples_id)).all()
        return({'genes': marshal(genes,gene_fields)}, 201)
