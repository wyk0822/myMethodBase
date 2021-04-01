
from flask import g, jsonify, session, request, make_response
from flask_restful import Resource
from ..tasks import task


class Login(Resource):
    def get(self):
        rest = task.send_email.delay("login")
        # g.username = "username"
        # g.test = "test"
        # a= g.username
        # print(a)
        return make_response(rest.id)

class Get_rest(Resource):
    def get(self):
        taskid = request.args.get("taskid")
        # print(g.username, g.test)
        check_rest(taskid)
        return "ok"


def check_rest(task_id):
    print("查询id: {}".format(task_id))



