import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util # from storage package > util module


server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)
# manages MongoDB connections for the Flask App

fs = gridfs.GridFS(mongo.db)
# GridFS API allows MongoDB work with larger than 16mb (BSON size limit) by sharding the file (divides the file into chunks of <= 16mb grids)
# uses two collections. One stored the chunks. the other stores the metadata (info needed to reassemble the chunks) fs.chunks & fs.files


# connection with RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) 
channel = connection.channel()

# login endpoint for GateWay - communicate with Auth SVC to logn the user in and assign a token to user
@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    
    if not err:
        return token
    else:
        return err
    

# upload endpoint - to upload video for conversion | validate token from validate module with token fn
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request) # from validate.py
    
    access=json.loads(access) # deserialize/convert a JSON Token (from create JWT) to a python object
    
    if access["admin"]: # if authz boolean returns TRUE. i.e is user is an admin
        if len(request.files) > 1 or len(request.files) < 1:
            return "excatly 1 file required", 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access) # from upload Fn
            
            if err:
                return err
            
        return "success!", 200
    
    else:
        return "not authorized", 401

# download endpoint for the mp3 files    
@server.route("/download", methods=["GET"])
def download():
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)