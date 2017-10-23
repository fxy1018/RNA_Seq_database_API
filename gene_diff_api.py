#gene differential expression table api

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

gene_diff_fields = {
    'id': fields.Integer,
    'experiment_id': fields.String,
    'entrez': fields.String,
    'gene_name': fields.String,
    'condition1_id': fields.String,
    'condition2_id': fields.String,
    'expression': fields.Float,
    'fdr': fields.Float,
    'logcpm':fields.Float,
    'logfc': fields.Float,
    'lr': fields.Float,
    'pvalue': fields.Float 
    }

class GeneDiffExpAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('condition1', type = str, location = 'json')
        self.reqparse.add_argument('condition2', type = str, location = 'json')
        super(GeneDiffExpAPI, self).__init__()
        
    
    def get(self, exp_id, gene_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)

        args = self.reqparse.parse_args()
        condition1 = args['condition1']
        condition2 = args['condition2']
        diff_gene = session.query(DiffGeneExpression).filter(DiffGeneExpression.condition1_id == condition1,
                                                 DiffGeneExpression.condition2_id == condition2,
                                                 DiffGeneExpression.entrez == gene_id).all()
        
        return({'diff_genes': marshal(diff_gene, gene_diff_fields)}, 201)
        

class GeneDiffExpListAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('condition1', type = str, location = 'json')
        self.reqparse.add_argument('condition2', type = str, location = 'json')
        super(GeneDiffExpListAPI, self).__init__()
        
    def get(self, exp_id):
        isExist = session.query(Experiment.id).filter(Experiment.id == exp_id).scalar()
        if not isExist:
            abort(404)

        args = self.reqparse.parse_args()
        condition1 = args['condition1']
        condition2 = args['condition2']
        diff_genes = session.query(DiffGeneExpression).filter(DiffGeneExpression.experiment_id == exp_id,
                                                              DiffGeneExpression.condition1_id == condition1,
                                                              DiffGeneExpression.condition2_id == condition2).all()
        
        return({'diff_genes': marshal(diff_genes, gene_diff_fields)}, 201)
        

        