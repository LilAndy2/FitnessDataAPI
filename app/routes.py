'''
    This file contains the routes for the webserver.
'''
import json
from flask import request, jsonify
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    '''
        Example POST endpoint that receives data and processes it.
    '''
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    '''
        Function that returns the result of the job with the given job_id
    '''
    job_id = int(job_id)
    webserver.log.info("Received request for job_id %s", job_id)
    # Check if the job_id is valid
    if job_id <= webserver.job_counter:
        task = webserver.tasks_runner.job_status.get(job_id, None)
        # Check if the task is still running
        if task is not None:
            result = get_result(job_id)
            webserver.log.info("Task %s is done.", job_id)
            return jsonify({
                "status": "done",
                "data": result
            }), 200

        webserver.log.info("Task %s is still running.", job_id)
        return jsonify({
            "status": "running"
        }), 200

    webserver.log.error("Invalid job_id %s.", job_id)
    return jsonify({
        "status": "error",
        "reason": "Invalid job_id"
    }), 405

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    '''
        Function that handles the request for the states_mean endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for states_mean.")
    return_value = add_task(data, 1)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    '''
        Function that handles the request for the state_mean endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for state_mean.")
    return_value = add_task(data, 2)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    '''
        Function that handles the request for the best5 endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for best5.")
    return_value = add_task(data, 3)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    '''
        Function that handles the request for the worst5 endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for worst5.")
    return_value = add_task(data, 4)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    '''
        Function that handles the request for the global_mean endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for global_mean.")
    return_value = add_task(data, 5)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    '''
        Function that handles the request for the diff_from_mean endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for diff_from_mean.")
    return_value = add_task(data, 6)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    '''
        Function that handles the request for the state_diff_from_mean endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for state_diff_from_mean.")
    return_value = add_task(data, 7)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    '''
        Function that handles the request for the mean_by_category endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for mean_by_category.")
    return_value = add_task(data, 8)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    '''
        Function that handles the request for the state_mean_by_category endpoint.
    '''
    # Get request data
    data = request.json

    webserver.logger.info("Received request for state_mean_by_category.")
    return_value = add_task(data, 9)
    if return_value != -1:
        return jsonify({
            "status": "done",
            "job_id": return_value
        }), 200

    return jsonify({
        "status": "error",
        "reason": "Thread Pool is shutting down, no more tasks can be added."
    }), 405

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    '''
        Function that triggers the graceful_shutdown Event in the ThreadPool.
        The Thread Pool will finish all the tasks in the queue before shutting down.
    '''
    webserver.logger.info("graceful_shutdown request called")
    webserver.tasks_runner.shutdown()
    return jsonify({
        "status": "done"
    }), 200

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    '''
        Function to get the status of all the tasks
    '''
    webserver.logger.info("jobs request called")
    jobs = []

    for job_id in range(1, webserver.job_counter):
        if job_id in webserver.tasks_runner.job_status:
            jobs.append({job_id: "done"})
        else:
            jobs.append({job_id: "running"})

    return jsonify({
        "status": "done", 
        "data": jobs
    }), 200

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    '''
        Function to get the number of tasks that are still being processed
    '''
    webserver.logger.info("num_jobs request called")
    return jsonify({
        "status": "done", 
        "data": webserver.job_counter - len(webserver.tasks_runner.job_status)
    }), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    '''
        Function that returns the index page of the webserver.
    '''
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += "<p>%s</p>", route

    msg += paragraphs
    return msg

def get_defined_routes():
    '''
        Function that returns the defined routes of the webserver.
    '''
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append("Endpoint: \"%s\" Methods: \"%s\"", rule, methods)
    return routes

def add_task(data, job_type):
    '''
        Function that adds a task to the queue.
    '''
    webserver.log.info("Adding task %s of type %s", data, job_type)
    data['job_id'] = webserver.job_counter
    data['job_type'] = job_type
    result = webserver.tasks_runner.add_task(data)

    if result != -1:
        webserver.log.info("Task %s added to the queue.", data['job_id'])
        webserver.job_counter += 1
        return result

    webserver.log.warning("Task was not registered.")
    return -1

def get_result(job_id):
    '''
        Function that gets the result of a task.
    '''
    with open(f"results/result-{job_id}.json", "r", encoding="utf-8") as f:
        result = json.load(f)
    return result
