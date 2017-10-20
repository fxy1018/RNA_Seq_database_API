#User api

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from anaconda_navigator.utils.launch import console
import sys

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    user = list(filter(lambda u: u['username'] == username, users))
    if len(user) == 1:
        return(user[0]['password'])
    return(None)

@auth.error_handler
def unauthorized():
    return(make_response(jsonify({'error': 'Unauthorized access'}), 403))

users = [
    {
        'id': 1,
        'username': u'abc',
        'password': u'123', 
        'email': u'abc@ironwoodpharma.com'
    },
    {
        'id': 2,
        'username': u'edf',
        'password': u'456', 
        'email': u'edf@ironwoodpharma.com'
    }
]

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
        user = list(filter(lambda u: u['id'] == id, users))
        if len(user) == 0:
            abort(404)
        return({'user': marshal(user,user_fields)}, 201)
    
    def put(self,id):
        user = [user for user in users if user['id']==id]
        if len(user) == 0:
            abort(404)
        user = user[0]
        args = self.reqparse.parse_args()
        for k in args:
            if args[k]:
                user[k] = args[k]
        return({'user': marshal(user, user_fields)}, 201)
        
    def delete(self,id):
        user = [user for user in users if user['id']==id]
        if len(user) == 0:
            abort(404)
        users.remove(user[0])
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
            'id': users[-1]['id'] + 1,
            'username': args['username'],
            'password': args['password'],
            'email': args['email']
            }
        user = list(filter(lambda u: u['username'] == tmp_user['username'], users))
        if len(user) != 0:
            abort(400)
        users.append(tmp_user)
        return({ 'user': marshal(tmp_user, user_fields)}, 201)
    
    def get(self):
        return({'users': [marshal(user, user_fields) for user in users]})
