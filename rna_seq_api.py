'''
Create Rest API for ran_seq_result databasae

'''

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from anaconda_navigator.utils.launch import console
import sys
from user_api import *
from experiment_api import *
from gene_api import *
from gene_diff_api import *
from sample_api import *

app = Flask(__name__)

api = Api(app)

#################RNA-Seq User API
api.add_resource(UserAPI, '/rna_seq/api/v1.0/users/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/rna_seq/api/v1.0/users', endpoint = 'users')

#################RNA-Seq database API#####################
api.add_resource(ExperimentAPI, '/rna_seq/api/v1.0/experiments/<int:id>', endpoint='experiment')
api.add_resource(ExperimentListAPI, '/rna_seq/api/v1.0/experiments', endpoint = 'experiments')

api.add_resource(SampleAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/samples/<int:sample_id>', endpoint='sample')
api.add_resource(SampleListAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/samples', endpoint='samples')

api.add_resource(GeneExpAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/genes/<int:gene_id>', endpoint='gene')
api.add_resource(GeneExpListAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/genes', endpoint = 'genes')

api.add_resource(GeneDiffExpAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/diff_exp_genes/<int:gene_id>', endpoint='diff_exp_gene')
api.add_resource(GeneDiffExpListAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/diff_exp_genes', endpoint = 'diff_exp_genes')

class KeggPathwayAPI(Resource):
    def get(self, exp_id, kegg_id):
        pass
class KeggPathwayListAPI(Resource):
    def get(self, exp_id):
        pass
    
api.add_resource(KeggPathwayAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/kegg_pathways/<int:kegg_id>', endpoint='kegg_pathway')
api.add_resource(KeggPathwayListAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/kegg_pathways', endpoint = 'kegg_pathways')

class ReactomeAPI(Resource):
    def get(self, exp_id, reactome_id):
        pass
class ReactomeListAPI(Resource):
    def get(self, exp_ud):
        pass

api.add_resource(ReactomeAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/reactome_pathways/<int:reactome_id>', endpoint='reactome_pathway')
api.add_resource(ReactomeListAPI, '/rna_seq/api/v1.0/experiments/<int:exp_id>/reactome_pathways', endpoint = 'reactome_pathways')




if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=3134)
#     app.run(debug=True)

