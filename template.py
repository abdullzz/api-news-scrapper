from flask import make_response, jsonify

def success(values):
    res = {
        "status" : 200,
        "length" : len(values),
        "data" : values
    }
    return make_response(jsonify(res), 200)

def not_found(values):
    res = {
        "status" : 404,
        "length" : 0,
        "data" : values
    }
    return make_response(jsonify(res), 404)

def timeout(values):
    res = {
        "status" : 522,
        "length" : 0,
        "data" : values
    }
    return make_response(jsonify(res), 522)

def network_errors(values):
    res = {
        "status" : 522,
        "length" : 0,
        "data" : values
    }
    return make_response(jsonify(res), 523)

def errors(values):
    res = {
        "status" : 600,
        "length" : 0,
        "data" : str(values)
    }
    return make_response(jsonify(res), 600)