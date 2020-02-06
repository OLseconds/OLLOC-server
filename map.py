from flask import Flask
from flask_restful import Resource, Api, reqparse
import olsns, urllib.parse
from flask_cors import CORS


class UserApi(Resource):

    def __init__(self):
        self.f = open("./pwd.txt", 'r')
        self.database = olsns.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(f.readline()), db="locations")
        self.f.close()
        self.usermod = olsns.User(self.database)
        self.parser = reqparse.RequestParser()

    def argParser(self, parser, args_list):
        for i in args_list:
            parser.add_argument(i, location='json')
        args = parser.parse_args()

        for i in args_list:
            if not args[i]:
                return {'error_code': 0, 'error_msg': i + ' Missing parameters'}, 400
        return args


    def get(self, re_id, re_id2):
        if re_id == "user": # 회원정보 조회
            if not re_id2:
                return {'error_code':1, 'error_msg':''}

    def post(self, re_id):


        if re_id == "session":
            pass
        elif re_id == "join":
            # JSON Parser
            args = self.argParser(parser=self.parser, args_list=['username', 'name', 'password', 'mail'])

            try:
                addMsg = self.usermod.useradd(username=args['username'], password=args['password'], name=args['name'], mail=args['mail'])
            except TypeError:
                return args
            try:
                return {'error_code': addMsg[1], 'error_msg': "Valid username" if addMsg[1] == 1 else "Username already in use"}, 200
            except TypeError:
                return {'msg':'join ok'}, 200


        return {'msg': 'post ok'}

    def put(self):
        return {'msg': 'put ok'}

    def delete(self):
        return {'msg': 'delete ok'}


app = Flask(__name__)
CORS(app)
api = Api(app=app)
api.add_resource(UserApi, '/v0.0/user/<re_id>/<re_id2>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
    #, ssl_context=('./cert/server.crt', './cert/server.key')