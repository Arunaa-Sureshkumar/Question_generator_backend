import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")

app = Flask(__name__)

CORS(app)
# app.config['MONGO_URI'] = mongodb_uri
myclient = pymongo.MongoClient(mongodb_uri)
# mongo = PyMongo(app)

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    ques = data.get('ques')
    soln = data.get('soln')
    variables = data.get('variables')
    options = data.get('options')
    quesname = data.get('quesname')
    unique_id = data.get('unique_id')
    actions = data.get('actions')
    lcmvariables = data.get('lcmvariables')
    addvariables = data.get('addvariables')
    subvariables = data.get('subvariables')
    mulvariables = data.get('mulvariables')
    divvariables = data.get('divvariables')
    sqvariables = data.get('sqvariables')
    sqrootvariables = data.get('sqrootvariables')
    cubevariables = data.get('cubevariables')
    curootvariables = data.get('curootvariables')
    factvariables = data.get('factvariables')
    diffvariables = data.get('diffvariables')
    pervariables = data.get('pervariables')
    logvariables = data.get('logvariables')
    optionvariables = data.get('optionvariable')
    if len(unique_id)>0:
        # If unique_id exists, perform the update
        questions_collection = mongo.db.Questions
        helper_variables = mongo.db.HelperVariables
        questions_collection.update_one(
            {'Unique_id': unique_id},
            {
                '$set': {
                    'Ques_name': quesname,
                    'Question': ques,
                    'Solution': soln,
                    'Variables': variables,
                    'Options': options,
                    'Actions': actions,
                }
            }
        )
        helper_variables.update_one(
            {'Unique_id': unique_id},
            {
                '$set': {
                    'Ques_name': quesname,
                    'Unique_id': unique_id,
                    'optionvariables': optionvariables,
                },
                '$push': {
                    'lcm': { '$each': lcmvariables },  
                    'add': { '$each': addvariables },  
                    'sub': { '$each': subvariables },  
                    'mul': { '$each': mulvariables },  
                    'div': { '$each': divvariables },  
                    'square': { '$each': sqvariables },
                    'sqroot': { '$each': sqrootvariables },
                    'cube': { '$each': cubevariables },
                    'fact': { '$each': factvariables },
                    'percentage': { '$each': pervariables },
                    'log': { '$each': logvariables },  
                }
            }
        )
        return jsonify('Record updated successfully')
    else:
        # If unique_id is not present, generate a new one and insert a new record
        unique_id = str(uuid.uuid4())
        questions_collection = mongo.db.Questions
        helper_variables = mongo.db.HelperVariables
        questions_collection.insert_one({
            'Ques_name': quesname,
            'Unique_id': unique_id,
            'Question': ques,
            'Solution': soln,
            'Variables': variables,
            'Options': options,
            'Actions': actions
        })
        helper_variables.insert_one({
            'Ques_name': quesname,
            'Unique_id': unique_id,
            'lcm': lcmvariables,
            'add': addvariables,
            'sub': subvariables,
            'mul': mulvariables,
            'div': divvariables,
            'square': sqvariables,
            'sqroot': sqrootvariables,
            'cube': cubevariables,
            'curoot': curootvariables,
            'fact': factvariables,
            'difference': diffvariables,
            'percentage': pervariables,
            'log': logvariables,
            'optionvariables': optionvariables,
        })
        return jsonify('Record inserted successfully')

@app.route('/get_variables', methods=['GET'])
def get_variables():
    print("inside getvariables")
    try:
        # questions_collection = mongo.db.Questions
        mydb = myclient["question_generator"]
        print(mydb)
        mycol = mydb["Questions"]
        print(mycol)
        # variables = list(questions_collection.find({}, {'_id': False}))
        variables = list(mycol.find({}, {'_id': False}))
        print(variables)
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"Error: {e}")
    except pymongo.errors.CursorNotFound as e:
        print("The cursor was not found. It might have expired or closed:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
    print("after question collection")

    # return jsonify(variables)
    return jsonify("hello")

@app.route('/get_data/<string:id>', methods=['GET'])
def get_data_by_id(id):
    questions_collection = mongo.db.Questions
    helper_variables = mongo.db.HelperVariables
    document = (questions_collection.find_one({'Unique_id': id}))
    document1 = (helper_variables.find_one({'Unique_id': id}))
    if document:
        document['_id'] = str(document['_id'])
        document1['_id'] = str(document1['_id'])
    alldocument = {**document, **document1}
    return jsonify(alldocument)
    print(alldocument)

@app.route('/delete', methods=['DELETE'])
def delete():
    questions_collection = mongo.db.Questions
    data = request.get_json()
    id = data.get('Unique_id')

    result = questions_collection.delete_one({'Unique_id': id})
    return jsonify("deleted")

if __name__ == '__main__':
    app.run(debug=True, port=7070)