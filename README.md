#  Simple example async API with Google Cloud Tasks and App Engine    
  
###  Usage:    
  
#### Setup gcloud project  
This expects queue to be created and gcloud tasks api enabled  
details can be found here:  
https://cloud.google.com/tasks/docs/quickstart-appengine#create_a_cloud_tasks_queue  
You will need a service account to create tasks from local -   
https://cloud.google.com/compute/docs/access/service-accounts  
  
#### Install     
clone repo    
cd into the repo folder      
remember to activate your python virtual environment of preference (e.g. pipenv shell)    
pip install -r  requirements.txt     
  
#### Run    
  
##### I just want to poke what is already done!  
Go for it:  
1) Queue -  https://console.cloud.google.com/cloudtasks/queue/my-queue?project=revolut-ds&organizationId=367080375030  
2) Endpoint that will create a task in queue - https://art-test-two-dot-revolut-ds.appspot.com/add_task_app_engine  
3) Logs of the queue:  
https://console.cloud.google.com/logs/viewer?project=revolut-ds&minLogLevel=0&expandAll=false&timestamp=2019-11-13T10:00:56.458000000Z&customFacets=&limitCustomFacetWidth=true&dateRangeStart=2019-11-13T09:00:56.713Z&dateRangeEnd=2019-11-13T10:00:56.713Z&interval=PT1H&resource=cloud_tasks_queue  
4) You can call the external task endpoint:  
https://art-test-two-dot-revolut-ds.appspot.com/add_task_external  
and see that request was passed through queue and into the bin-bucket:  
https://requestbin.com/r/enfi2o6y5sm0g/  
  
  
#### DIY  
  
##### web application:    
activate your virtual environment    
export GOOGLE_APPLICATION_CREDENTIALS=/pass/to/service_accounts_creds.json    
python main.py  
you are in business! you can call localhost:8088/do_external_task and async task will be added to the queue:  
https://console.cloud.google.com/cloudtasks/queue/my-queue?project=revolut-ds&organizationId=367080375030  
If you want to deploy worker to handle the task - check deploy handler  
    
#####  Deploy Google App Engine handler:  
gcloud app deploy   
this will  deploy service specified in app.yaml to the gcloud project.  All the endpoints in main.py will be available by the https://{SERVICE-NAME}-dot-revolut-ds.appspot.com/{ENDPOINT_ROUTE}, e.g. https://art-test-two-dot-revolut-ds.appspot.com/add_task_app_engine  
As the tasks queue used here is the Push queue, it will make sure that every task that has available handler specified is pushed to the handler for execution  
  
##### Calling App Engine Endpoints from code(optional):    
In terms of providing async api to the machine consumption one might want to create end-point in app engine that will create task in queue. This endpoint can be used along the lines of request_to_app_engine_example code.  
To run provided example:  
export GOOGLE_APPLICATION_CREDENTIALS=/pass/to/service_accounts_creds.json    
export TARGET_AUDIENCE=yourtargetaudience.apps.googleusercontent.com   
python request_to_app_engine_example.py  
  
### What to see?    
Worker is expressed as standard endpoint, that will be called by push queue. Using the app engine endpoint allows to utilize it's scalability, and hence avoid thinking about queue or worker servers - pretty much serverless setup.  
Queue is created declaratively on the project.   
https://cloud.google.com/tasks/docs/quickstart-appengine#create_a_cloud_tasks_queue  
Task can be published from endpoint(or anywhere) using any of the Task Client libraries.  
https://cloud.google.com/tasks/docs/reference/libraries  
Example of publishing a task are in create_task.py  
Create_app_engine_http_request_task shows how task can be created to be handled by the endpoint in Google App Engine  
Create_http_request_task is using feature of pushing request to anywhere in the internet via http. (Feature is in beta right now)  
Example of publishing a task from another end_point in main.py add_task_external and add_task_app_engine  
  
##### Basic concepts:    
  
Worker/Subscriber - connects to the queue and waits for items to work on.    
Queue - sits in the middle, receives messages and supplies those to the workers. Rabbitmq in current repo.    
Push queue - queue that has active life position and nags downstream handler to do stuff when it's not empty.  
App/Publisher - something pushing items into queue. In current repo it's flask app listening to http requests and transferring those into queue for async processing.    
Async processing - we don't want to wait for when job is done, we need worker to take the item, say 'SIR, YES, SIR' and disappear in the distance.    
  
  
##### Stack:    
flask - web api/app    
google-cloud-tasks - task creation  
google-auth - authentication  
  
### Reference    
Google Cloud Tasks docs  
https://cloud.google.com/tasks/docs/  
Google app engine:  
https://cloud.google.com/appengine/docs/  
Google auth:  
https://github.com/googleapis/google-cloud-python/blob/0.8.0/docs/gcloud-auth.rst#id2  