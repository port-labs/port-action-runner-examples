# s3_bucket_creation/aws_sdk

## Description

The following example creates S3 bucket using AWS SDK (Boto3)

This example consists of a FastAPI backend, that listen for Port Action Webhook events.

For each event, the backend use AWS SDK (Boto3) to create S3 bucket.

Finally, the backend creates new Port Entity and updates the Port Action run.

## Table of Contents
1. [Local Setup](#Localhost)
2. [Webhook Setup](#Webhook)
3. [Port Setup](#Port)

## Diagram

![diagram.png](diagram.png)

## Setup

### Localhost

1. Make sure that the Docker daemon is available and running
```
$ docker info
```

2. Create `.env` file with the required environment variables
```
$ cat .env

PORT_CLIENT_ID=<PORT_CLIENT_ID>
PORT_CLIENT_SECRET=<PORT_CLIENT_SECRET>
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
```

3. Build example's Docker image
```
$ docker build -t getport.io/s3_bucket_creation/aws_sdk .
```

4. Run example's Docker image with `.env`

To change the default port (`80`) to `8080` for example, replace command's flags with the following: `-p 80:8080 -e PORT="8080"`
```
$ docker run -d --name getport.io-s3_bucket_creation-aws_sdk -p 80:80 --env-file .env getport.io/s3_bucket_creation/aws_sdk
```

5. Verify that the Docker container is up and running, and ready to listen for new webhooks:
```
$ docker logs -f getport.io-s3_bucket_creation-aws_sdk

...
[2022-09-18 12:17:17 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2022-09-18 12:17:17 +0000] [1] [INFO] Listening at: http://0.0.0.0:80 (1)
[2022-09-18 12:17:17 +0000] [1] [INFO] Using worker: uvicorn.workers.UvicornWorker
[2022-09-18 12:17:17 +0000] [10] [INFO] Booting worker with pid: 10
...
[2022-09-18 12:17:19 +0000] [18] [INFO] Application startup complete.
```

`docker logs -f` command follows log output, and helps you also to troubleshoot future action runs.

### Webhook

1. Create public URL for your local application. 

In this tutorial, we create a new channel in [smee.io](https://smee.io/), and use provided `Webhook Proxy URL`. 

2. Install the Smee client:
```
$ pip install pysmee
```

3. Use installed `pysmee` client to forward the events to your localhost API URL (replace `<SMEE_WEBHOOK_PROXY_URL>`):
```
pysmee forward <SMEE_WEBHOOK_PROXY_URL> http://localhost:80/api/bucket
```

### Port

1. Create `S3Bucket` blueprint:
```
{
    "identifier": "S3Bucket",
    "title": "S3 Bucket",
    "icon": "Bucket",
    "schema": {
        "properties": {
            "acl": {
                "type": "string",
                "title": "ACL"
            },
            "awsRegion": {
                "type": "string",
                "title": "AWS Region"
            },
            "createdDate": {
                "type": "string",
                "title": "Created Date",
                "format": "date-time"
            },
            "S3Link": {
                "type": "string",
                "title": "S3 Link",
                "format": "url"
            }
        },
        "required": []
    },
    "mirrorProperties": {}
}
```

2. Create new `CreateBucket` action for blueprint (replace `<WEBHOOK_URL>`):
```
[
    {
        "identifier": "CreateBucket",
        "title": "Create Bucket",
        "userInputs": {
            "properties": {
                "bucket-name": {
                    "type": "string",
                    "title": "Bucket Name"
                },
                "aws-region": {
                    "type": "string",
                    "title": "AWS Region",
                    "default": "eu-west-1"
                },
                "acl": {
                    "type": "string",
                    "title": "ACL",
                    "default": "private"
                }
            },
            "required": [
                "bucket-name"
            ]
        },
        "invocationMethod": {
            "type": "WEBHOOK",
            "url": "<WEBHOOK_URL>"
        },
        "trigger": "CREATE",
        "description": "This will create a new S3 bucket"
    }
]
```

3. Run the action with some input (replace `<GLOBALLY_UNIQUE_BUCKET_NAME>`):
```
{
    "aws-region": "eu-west-1",
    "acl": "private",
    "bucket-name": "<GLOBALLY_UNIQUE_BUCKET_NAME>"
}
```

4. Verify status and outcome of the action run in Port (run status in audit logs, new entities, ...).
