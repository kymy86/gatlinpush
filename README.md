GatlinPush [![Build Status](https://travis-ci.org/kymy86/gatlinpush.svg?branch=master)](https://travis-ci.org/kymy86/gatlinpush)
====

Micro service to manage and send push through
[Amazon AWS SNS] service.
With this micro-service you can:

- Add one or more app with the endpoint **/push/manager**
- For each app, add one or more device with the endpoint **/device**
- For each app, add one or more message with the endpoint **/push**

After adding one or more installation, you can send a message with the endpoint **/push/send/<message_id>/<app_id>**. The sending process is managed through [Celery] task queue, wichi use SQS as broker.
To monitor the sending process, you can check the **/push/status/<task_id>** endpoint.

To run Celery, execute:

`docker-compose run --rm gatlinpush celery worker -A app.celery --loglevel=info`

## @TO-DO

- Manage SNS endpoint status: currently, the app doesn't check if the endpoint is a valid SNS endpoint, before processing it. This results in an error in the Celery task queue process.
- Get and display the sending stats from SNS. Create an endpoint to return the sending stats.

## Project set-up

1. Rename env_example in .env
2. run docker-compose up


## Db Migration

`docker-compose run --rm gatlinpush python manage.py db init`

`docker-compose run --rm gatlinpush python manage.py db upgrade`

`docker-compose run --rm gatlinpush python manage.py db migrate`

`docker-compose run --rm gatlinpush python manage.py db downgrade`

## Test

`docker-compose run --rm gatlinpush python -m unittest`

## Database connect

`docker exec -it gatlinpush_postgresdb_1 psql dbname dbuser`

[Amazon AWS SNS]:(http://docs.aws.amazon.com/sns/latest/dg/SNSMobilePush.html)

[Celery]: (http://www.celeryproject.org/)