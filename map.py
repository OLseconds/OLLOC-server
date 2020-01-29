from flask import Flask
from flask_restful import Resource, Api, reqparse
import olsns, urllib.parse
from flask_cors import CORS
from OpenSSL import SSL


class UserApi(Resource):
    def get(self, re_id):
        return {'msg': re_id}

    def post(self, re_id):
        f = open("./pwd.txt", 'r')
        database = olsns.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(f.readline()), db="locations")
        f.close()
        usermod = olsns.User(database)
        parser = reqparse.RequestParser()

        if re_id == "session":
            pass
        elif re_id == "join":
            args_list = ['username', 'name', 'password', 'mail']
            for i in args_list:
                parser.add_argument(i, location='json')
            args = parser.parse_args()

            for i in args_list:
                if not args[i]:
                    return {'error_code': 0, 'error_msg': i + ' Missing parameters'}, 400

            addMsg = usermod.useradd(username=args['username'], password=args['password'], name=args['name'], mail=args['mail'])
            if addMsg[0] == False:
                return {'error_code': addMsg[1], 'error_msg': "Valid username" if addMsg[1] == 1 else "Username already in use"}, 400

            return {'msg':'join ok'}
        elif re_id == "user_profile":
            pass

        return {'msg': 'post ok'}

    def put(self):
        return {'msg': 'put ok'}

    def delete(self):
        return {'msg': 'delete ok'}


app = Flask(__name__)
CORS(app)
api = Api(app=app)
api.add_resource(UserApi, '/v0.0/user/<re_id>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True, ssl_context=('./cert/server.crt', './cert/server.key'))