from flask import Flask
from . import status
app = Flask(__name__)
COUNTERS = {}


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    ''' Create a counter '''
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        return {"Messgae": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    ''' Update a counter '''
    app.logger.info(f"Request to update counter: {name}")
    global COUNTERS
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND
    COUNTERS[name] += 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    ''' Read from counter '''
    app.logger.info(f"Request to read from counter: {name}")
    global COUNTERS
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND
    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    ''' Delete a counter '''
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS
    if name in COUNTERS:
        del COUNTERS[name]
        return {"Message": f"Counter {name} has been deleted"}, status.HTTP_204_NO_CONTENT
    else:
        return {"Message": f"Counter {name} does not exist"}, status.HTTP_404_NOT_FOUND
