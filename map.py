from flask import Flask
from flask_restful import Resource, Api, reqparse
import olsns, urllib.parse
from flask_cors import CORS
from OpenSSL import SSL

# https://velog.io/@city7310/flask-restful-A-to-Z-2.-flaskrestful.Resource-flaskrestful.Api 참고 하자 이거


class UserApi(Resource):
    def get(self, re_id):
        return {'msg': re_id}

    def post(self, re_id):
        if re_id == "login":
            pass
        elif re_id == "join":
            pass
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
    f = open("./pwd.txt", 'r')
    database = olsns.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(f.readline()), db="locations")
    f.close()
    usermod = olsns.User(database)
    usermod.useradd("test", "testpwd", "TEST", "test@test.com")

    #app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True, ssl_context=('./cert/server.crt', './cert/server.key'))