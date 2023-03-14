from flask import Flask, Response, request

import pymongo
import json
from bson.objectid import ObjectId
app= Flask(__name__)
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    db= mongo.company
    mongo.server_info()
except:
    print("Error-Cannot connect to db")

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse= db.users.delete_one({"_id":ObjectId(id)})

        if dbResponse.deleted_count is 1:
            return Response(
            response= json.dumps({"message":"deleted"}),
            status=200, 
            mimetype='application/json')
        return Response(
            response= json.dumps({"message":"nothing deleted"}),
            status=200, 
            mimetype='application/json')
        
    except Exception as ex:
        print("*****")
        print(ex)
    return Response(
            response= json.dumps({"message":"sorry"}),
            status=500, 
            mimetype='application/json')

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        #for attr in dir(dbResponse):
            #print(f"*****{attr}*****")
        if dbResponse.modified_count is 1:
            return Response(
            response= json.dumps({"message":"updated"}),
            status=200, 
            mimetype='application/json')
        else:
            return Response(
            response= json.dumps({"message":"nothing updated"}),
            status=200, 
            mimetype='application/json')
    except Exception as ex:
        print("**********")
        print(ex)
        return Response(
            response= json.dumps({"message":"sorry"}),
            status=500, 
            mimetype='application/json')

@app.route("/users", methods=["GET"])
def get_user():
    try:
        data= list(db.users.find())
        for user in data:
            user["_id"]=str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500, 
            mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps(
            {"message":"cannot read user",}),
              status=500, mimetype='application/json')

@app.route("/users",methods=["POST"])
def create_user():
    try:
        user ={"name":request.form["name"], "lastname":request.form["lastname"]}
        dbResponse =db.users.insert_one(user)
        print(dbResponse.inserted_id)
        #for attr in dir(dbRespose):
         #   print(attr)
        return Response(response=json.dumps(
            {"message":"user craeted",
             "id":f"{dbResponse.inserted_id}"}),
              status=200, mimetype='application/json')

    except Exception as ex:
        print("******")
        print(ex)



if __name__== '__main__':
    app.run(port=80,debug=True)