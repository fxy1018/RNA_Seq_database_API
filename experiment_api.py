#Experiment DATA API
from user_api import auth
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from anaconda_navigator.utils.launch import console
import sys

experiment_fields = {
    'description': fields.String,
    'date': fields.String,
    'tech': fields.String,
    'comments': fields.String,
    'uri': fields.Url('experiment')  
    }

