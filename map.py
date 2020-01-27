from flask import Flask
from flask_restful import Resource, Api, reqparse
import db, urllib.parse
from flask_cors import CORS

#https://velog.io/@city7310/flask-restful-A-to-Z-2.-flaskrestful.Resource-flaskrestful.Api 참고 하자 이거

app = Flask(__name__)
CORS(app)
title = 'my homepage'
api = Api(app=app)


class UserApi(Resource):
    def get(self):
        return {'msg': 'get ok'}, 201

    def post(self):
        return {'msg': 'post ok'}

    def put(self):
        return {'msg': 'put ok'}

    def delete(self):
        return {'msg': 'delete ok'}


api.add_resource(UserApi, '/v0.0/test')


if __name__ == '__main__':
    f = open("./pwd.txt", 'r')
    database = db.Db(host="127.0.0.1", user="location", pwd=urllib.parse.quote(f.readline()), db="locations")
    f.close()
    usermod = db.User(database)
    usermod.useradd("test", "testpwd", "TEST", "test@test.com")

    #app.debug = True
    app.run(host="0.0.0.0", port="5000")