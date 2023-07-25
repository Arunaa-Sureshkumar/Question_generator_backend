import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = mongodb_uri
mongo = PyMongo(app)

print
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
        questions_collection = mongo.db.questions
        helper_variables = mongo.db.Helper_variables
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
        questions_collection = mongo.db.questions
        helper_variables = mongo.db.Helper_variables
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
    questions_collection = mongo.db.questions
    variables = list(questions_collection.find({}, {'_id': False}))
    return jsonify(variables)

@app.route('/get_data/<string:id>', methods=['GET'])
def get_data_by_id(id):
    questions_collection = mongo.db.questions
    helper_variables = mongo.db.Helper_variables
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
    questions_collection = mongo.db.questions
    data = request.get_json()
    id = data.get('Unique_id')

    result = questions_collection.delete_one({'Unique_id': id})
    return jsonify("deleted")

if __name__ == '__main__':
    app.run(debug=True)