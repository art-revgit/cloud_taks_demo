from google.cloud import tasks_v2beta3 as tasks


def do_external():
    """example of call to external http endpoint through push queue"""
    # Queue details
    project = "revolut-ds"
    queue = "my-queue"
    location = "europe-west1"
    # Task details
    url = "https://enfi2o6y5sm0g.x.pipedream.net/"  # request bin url for example
    payload = "input to the task"
    return create_http_request_task(project, queue, location, url, payload)


def do_app_engine():
    """example of call to google cloud app engine through push queue"""
    # Queue details
    project = "revolut-ds"
    queue = "my-queue"
    location = "europe-west1"
    # Task details
    url = "/example_task_handler"  # request bin url for example
    payload = "input to the task"
    service = "art-test-two"  # service name where the handler is, defined in app.yaml
    return create_app_engine_http_request_task(project, queue, location, url, payload, service)


def create_app_engine_http_request_task(project, queue, location, url, payload, service="default"):
    # Create a client.
    client = tasks.CloudTasksClient()

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": "POST",
            "relative_uri": url,
            "app_engine_routing": {"service": service},
        }
    }
    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["app_engine_http_request"]["body"] = converted_payload

    # Use the client to build and send the task.
    response = client.create_task(parent, task)

    print("Created task {}".format(response.name))
    return response


def create_http_request_task(project, queue, location, url, payload):
    """Create a task for a given queue with an arbitrary payload."""
    # Create a client.
    client = tasks.CloudTasksClient()

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": "POST",
            "url": url,  # The full url path that the task will be sent to.
        }
    }
    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload

    # Use the client to build and send the task.
    response = client.create_task(parent, task)

    print("Created task {}".format(response.name))

    return response
