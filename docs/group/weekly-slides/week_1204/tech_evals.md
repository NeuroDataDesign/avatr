# StackDriver Tech Evaluation
We are exploring StackDriver for it's logging functionalities. More specifically, we are evaluating this tool on it's capabilities to log the results and commands used to run a data pipeline.

## Overview
StackDriver is an API designed for monitoring, logging, and diagnosing applications deployed on AWS and Cloud Platform.  

**Relevant Features:**  
- Error Reporting
  - When your cloud application fails, errors are automatically detected and reported.
  - This may be useful for catching when specific pipelines stop working. After all, very few pipelines are fully scoped out to handle all the potential exceptions in data modalities, etc.
  - Catching these errors will be useful in improving the pipelines themselves.
- Logging
  - Logs the statuses of your cloud application.
  - Can export logs to a dashboard and define metrics based off of log.

## How it works
You can connect an AWS account to your Google Cloud Platform account under the premium trial account. These steps involve creating AWS roles to authorize StackDriver and a bunch of Google Cloud Platform setup.  

Once this is done, you can install Stackdriver agents onto your EC2 instance to perform various tasks.

## Thoughts
This seems to work very well with EC2 applications. You can easily setup metrics to log what an instance is doing That being said, this can only be used on EC2 instances. You will need to monitor a ton of EC2 instances if you are using AWS Batch. I can see StackDriver being useful in deploying with pipeline services. However, in terms of an actual logging tool, we could probably just use AWS CloudWatch instead which is already built into AWS.

At the moment, this also doesn't really apply the actual data pipelines which is what we care about. The main purpose of this tool is for monitoring the entire application (i.e. the service the pipeline is being deployed on).

Furthermore, none of this stuff directly benefits the LIMS. We still have to parse these logs to store pipeline runs. I think DataJoin does a better job of handling this but DataJoin does seem a little overkill at the moment.


# DataJoint Tech Evaluation

## How it works
DataJoint is a framework for creating data pipelines in Python with a relational database and non-relational store (NoSQL) at the end to store results. Database can be on the cloud or local.

You can use DataJoint to setup a pipeline with the following functionalities:
1. Take in raw data (new or old)
2. Automated pipelines can take over and run on data, producing derivatives.
3. Each pipeline is connected to a respective database where they can store results.

## Thoughts
This is actually really cool and potentially useful for all teams. If teams setup their pipelines in this manner, the end results can be automatically stored correctly and we can also attach our LIMS as one of the endpoints in this overall pipeline to store metadata, commands, etc.

This also allows for very quick iterative development on pipelines themselves. You can split the pipeline into a series of nodes and just adjust the step you want to fix.

This will be a pretty time consuming thing to do though because it involves proper database server hosting.
