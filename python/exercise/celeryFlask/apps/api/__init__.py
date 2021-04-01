from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, default_mediatype='application/json')
from . import (
    login
)


to_login = login.Login.as_view('login')
api_bp.add_url_rule('/auth/login/', view_func=to_login)

get_rest = login.Get_rest.as_view('get_rest')
api_bp.add_url_rule('/auth/get_rest/', view_func=get_rest)