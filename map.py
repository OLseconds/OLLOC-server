from flask import Flask
from flask_restful import Resource, Api, reqparse
import olsns, urllib.parse
from flask_cors import CORS


class UserApi(Resource):

    def __init__(self):
        self.f = open("./pwd.txt", 'r')
        self.database = olsns.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(self.f.readline()), db="locations")
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

    def get(self, re_id):
        if not re_id:
            return {'error_code':0, 'error_msg':'Missing parameters'}, 400
        else:
            user_profile = self.usermod.user_profile(re_id)
            del user_profile['password']
            del user_profile['_id']
            return user_profile, 200
            #return {'error_code': 1, 'error_msg': 'Username does not exist'}


    def post(self):
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

#
api.add_resource(User, '/v0.0/user/<string:re_id>')
# 회원가입, 탈퇴, 수정
api.add_resource(UserApi, '/v0.0/user/<string:re_id>')등



if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
    #, ssl_context=('./cert/server.crt', './cert/server.key')