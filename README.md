GatlinPush
====

Micro service to manage and send push through
[Amazon AWS SNS] service

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