
import os
from flask import Blueprint
from flask_restx  import Api
from flask_restx  import apidoc
from flask_restx .api import url_for

from app.apis.chat.resources import ns as chat_ns

api_v1 = Blueprint('api1', __name__, url_prefix='/api/v1')

api = Api(api_v1, version='1.0', title='flask backend reference project',
    description='flask backend reference',
    default='chat', 
    doc=False
)

api.add_namespace(chat_ns)
