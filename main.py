from flask import Flask, request, jsonify
import create_task

app = Flask(__name__)


@app.route("/example_task_handler", methods=["POST"])
def example_task_handler():
    payload = request.get_data(as_text=True) or "(empty payload)"
    print("Received task with payload: {}".format(payload))
    return "Printed task payload: {}".format(payload)


@app.route("/add_task_external")
def add_task_external():
    return str(create_task.do_external())


@app.route("/add_task_app_engine")
def add_task_app_engine():
    return jsonify(str(create_task.do_app_engine()))


@app.route("/")
def default():
    return "Usual endpoint"


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8088, debug=True)
