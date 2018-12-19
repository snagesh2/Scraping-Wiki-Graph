#!flask/bin/python
from flask import Flask, jsonify, abort, request
import json
app = Flask(__name__)


with open('../Tests/movies.json', 'r') as json_data:
    movie_data = json.load(json_data)
with open('../Tests/actors.json', 'r') as json_data:
    actor_data = json.load(json_data)
with open('../Tests/edges.json', 'r') as json_data:
    edges_data = json.load(json_data)


@app.route('/Assignment2.1/movies', methods=['GET','POST'])
def puppiesFunction_m():
    if request.method == 'GET':
        return get_movies()
    elif request.method == 'POST':
        return create_movie()


def get_movies():
    return jsonify(movie_data)


def create_movie():
    if not request.json or not 'Name' in request.json:
        abort(400)
    task = {
        'Name': request.json['Name'],
        'Release Year': request.json.get('Release Year',0),
        'Box office': request.json.get('Box office',0),
        'Actors': request.json.get('Actors',[])
    }
    movie_data['Movies'].append(task)
    return jsonify(movie_data), 201


@app.route('/Assignment2.1/actors', methods=['GET','POST'])
def puppiesFunction_a():
    if request.method == 'GET':
        return get_actors()
    elif request.method == 'POST':
        return create_actor()


def get_actors():
    return jsonify(actor_data)


def create_actor():
    if not request.json or not 'Name' in request.json:
        abort(400)
    task = {
        'Name': request.json['Name'],
        'Age': request.json.get('Age',0),
        'Movies': request.json.get('Movies',[])
    }
    actor_data['Actors'].append(task)
    return jsonify(actor_data), 201


@app.route('/Assignment2.1/edges', methods=['GET'])
def get_edges():
    return jsonify(edges_data)


@app.route('/Assignment2.1/actors/<string:name>', methods=['GET','PUT','DELETE'])
def puppiesPutFunction_a(name):
    if request.method == 'GET':
        return get_task_a(name)
    elif request.method == 'PUT':
        return update_task_a(name)
    elif request.method == 'DELETE':
        return delete_task_a(name)


def get_task_a(name):
    task = [task for task in actor_data['Actors'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    return jsonify(task)


def update_task_a(name):
    task = [task for task in actor_data['Actors'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['Age']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['Movies']) is not bool:
        abort(400)
    task[0]['Name'] = request.json.get('Name', task[0]['Name'])
    task[0]['Age'] = request.json.get('Age', task[0]['Age'])
    task[0]['Movies'] = request.json.get('Movies', task[0]['Movies'])
    return jsonify({'Actor': task[0]})


def delete_task_a(name):
    task = [task for task in actor_data['Actors'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    actor_data['Actors'].remove(task[0])
    return jsonify({'result': True})


@app.route('/Assignment2.1/movies/<string:name>', methods=['GET','PUT','DELETE'])
def puppiesPutFunction_m(name):
    if request.method == 'GET':
        return get_task_m(name)
    elif request.method == 'PUT':
        return update_task_m(name)
    elif request.method == 'DELETE':
        return delete_task_m(name)

def get_task_m(name):
    task = [task for task in movie_data['Movies'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    return jsonify(task)


def update_task_m(name):
    task = [task for task in movie_data['Movies'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['Name']) != unicode:
        abort(400)
    if 'des' in request.json and type(request.json['Actors']) != unicode:
        abort(400)
    if 'yr' in request.json and type(request.json['Release Year']) is not unicode:
        abort(400)
    if 'gross' in request.json and type(request.json['Box office']) is not unicode:
        abort(400)

    task[0]['Name'] = request.json.get('Name', task[0]['Name'])
    task[0]['Release Year'] = request.json.get('Release Year', task[0]['Release Year'])
    task[0]['Box office'] = request.json.get('Box office', task[0]['Box office'])
    task[0]['Actors'] = request.json.get('Actors', task[0]['Actors'])
    return jsonify({'Movie': task[0]})


def delete_task_m(name):
    task = [task for task in movie_data['Movies'] if name in task['Name']]
    if len(task) == 0:
        abort(404)
    movie_data['Movies'].remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)