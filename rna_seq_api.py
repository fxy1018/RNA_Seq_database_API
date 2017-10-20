'''
Create Rest API for ran_seq_result databasae

'''

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from anaconda_navigator.utils.launch import console
import sys
from user_api import UserAPI, UserListAPI


app = Flask(__name__)
api = Api(app)

api.add_resource(UserAPI, '/rna_seq/api/v1.0/users/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/rna_seq/api/v1.0/users', endpoint = 'users')

#################RNA-Seq database API#####################
class ExperimentAPI(Resource):
    def get(self,exp_id):
        pass
class ExperimentListAPI(Resource):
    def get(self):
        pass

class GeneExpAPI(Resource):
    def get(self, exp_id, gene_id):
        pass

class GeneExpListAPI(Resource):
    def get(self, exp_id):
        pass

class GeneDiffExpAPI(Resource):
    def get(self, exp_id, gene_id):
        pass

class GeneDiffExpListAPI(Resource):
    def get(self, exp_id):
        pass

class KeggPathwayAPI(Resource):
    def get(self, exp_id, kegg_id):
        pass
class KeggPathwayListAPI(Resource):
    def get(self, exp_id):
        pass
class ReactomeAPI(Resource):
    def get(self, exp_id, reactome_id):
        pass
class ReactomeListAPI(Resource):
    def get(self, exp_ud):
        pass





if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=3134)
#     app.run(debug=True)

