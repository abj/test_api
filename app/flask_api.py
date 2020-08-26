from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource, abort
from app import db, app
from app.models import File
import os
import threading

USERNAME = 'anna'
PASSWORD = 'pass'

class Auth(Resource):
    def post(self):
        args = dict(request.args)
        if args['username'] != USERNAME or args['password'] != PASSWORD:
            return jsonify({'error': 'Invalid username or password', 'status_code': 400})
        return jsonify(access_token=create_access_token(identity=USERNAME))

class FileOperation(Resource):
    decorators = [jwt_required]
    def get(self, filename):
        f = File.query.get(filename)
        if f:
            return jsonify(f.as_dict())
        return jsonify({'error': 'Нет такого файла', 'status_code': 400})

    def post(self, filename):
        extension = filename.split('.')[-1]
        f = File()
        db.session.add(f)
        db.session.commit()
        with open(os.path.join(app.config['UPLOAD_DIRECTORY'], '.'.join([str(f.id), extension])), "wb") as file:
            file.write(request.data)
        response = jsonify(f.as_dict())
        response.status_code = 201
        f.extension = extension
        thread = threading.Thread(f.process())
        thread.start()
        return response

#api.add_resource(FileOperation, '/files/<filename>')
#api.add_resource(Auth, '/auth')

