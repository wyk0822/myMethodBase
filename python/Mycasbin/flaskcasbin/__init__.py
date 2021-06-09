import casbin
import casbin_sqlalchemy_adapter
import casbin
import flask
from functools import wraps
adapter = casbin_sqlalchemy_adapter.Adapter('sqlite:///test.db')

e = casbin.Enforcer('model.conf', adapter)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

print(e.get_adapter())

if e.enforce(sub, obj, act):
    # permit alice to read data1casbin_sqlalchemy_adapter
    print(f"允许{sub}读取{obj}")
else:
    # deny the request, show an error
    print("拒绝请求，抛出异常")

class config:
    casbin_db = 'sqlite:///test.db'
    casbin_model = 'model.conf'
class mycasbin():
    def __init__(self):
        self.adapter = casbin_sqlalchemy_adapter.Adapter(config.casbin_db)
        self.efc = casbin.Enforcer(config.casbin_model, self.adapter)

    def check_phone(self, func):
        @wraps(func)
        def wrapper(**kwargs):
            if e.enforce(sub, obj, act):
                # permit alice to read data1casbin_sqlalchemy_adapter
                print(f"允许{sub}读取{obj}")
            else:
                # deny the request, show an error
                print("拒绝请求，抛出异常")


            return func(**kwargs)
        return wrapper







# from flask import Flask, jsonify, request
# from flask_authz import CasbinEnforcer
# from casbin.persist.adapters import FileAdapter
# from functools import wraps
# app = Flask(__name__)
#
#
# def check_phone(f):
#     @wraps(f)
#     def inner(**kwargs):
#         print(request.method)
#         return f(**kwargs)
#     return inner
# @app.route('/', methods=['GET'])
# @check_phone
# def get_root():
#     return jsonify({'message': 'If you see this you have access'})
#
# @app.route('/manager', methods=['POST'])
# def make_casbin_change(manager):
#     # Manager is an casbin.enforcer.Enforcer object to make changes to Casbin
#     return jsonify({'message': 'If you see this you have access'})
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=50006, debug=True)