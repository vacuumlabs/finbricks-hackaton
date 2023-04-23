# finbricks-hackaton

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- fin_advice_invoke - Code for the application's FinAdviceInvokeFunction lambda function and Project Dockerfile. Asynchronous function to invoke the financial advice message generation. Function is to be called from API GW
- fin_advice_ai_message - Code for the application's FinAdviceAiMessageFunction lambda function and Project Dockerfile. Function returns the AI-generated financial advice text.
- transaction_categorization - Code for the application's FinAdviceAiMessageFunction lambda function and Project Dockerfile. Function returns the AI-generated category of a transaction.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/) (Use Python 3.9)

### Setup AWS
  * (First time only) 
    ```bash
    aws configure sso
      >>   SSO session name (Recommended): VacuumSandbox-finbricks
      >>   SSO start URL [None]: http://vacuumlabs.awsapps.com/start
      >>   SSO region [None]: eu-central-1
      >>   SSO registration scopes [sso:account:access]:
      >>   Using the account ID 910309976263
      >>   The only role available to you is: SandboxAdministratorAccess
      >>   Using the role name "SandboxAdministratorAccess"
      >>   CLI default client Region [None]: eu-central-1
      >>   CLI default output format [None]:
      >>   CLI profile name [SandboxAdministratorAccess-910309976263]:
    ```

  * (Every time credentials expire ~ every 12h):
    ```bash
    aws sso login --profile SandboxAdministratorAccess-910309976263
    ls -la ~/.aws/sso/cache # find the json for profile SandboxAdministratorAccess-910309976263
    cat ~/.aws/sso/cache/44c822286c27bb9a045e423765014d034e6f83ea.json # copy the access-token from here
    aws sso get-role-credentials --account-id 910309976263 --role-name SandboxAdministratorAccess  --region eu-central-1 --access-token HERE
    ```
    The last command will give you 3 keys/tokens, they go into `~/.aws/credentials` in this format:
    ```
    [SandboxAdministratorAccess-910309976263]
    aws_access_key_id=...
    aws_secret_access_key=...
    aws_session_token=...
    ```


### Pycharm extension - Matej approves
* install https://aws.amazon.com/pycharm/
* If you haven't filled `~/.aws/credentials` above, do it now
* Now the AWS Toolkit (left bar under Project/Commit/etc.) should show different AWS services in Explorer window once you pick the profile and region in the pickers.
* All you need to deploy is right click on your project/function/resource and click `Sync Serverless Application` or click on the resource in `template.yaml`
  * Note: use existing stack, s3 and ECR repo unless you want to have duplicates
  * Note: always use `Build inside containers`, otherwise you will see some weird behavior with some Python libs compatibility


### Shell
To build and deploy your application for the first time, run the following in your shell:
```bash
sam build
sam deploy --guided
```

The first command will build a docker image from a Dockerfile and then copy the source of your application inside the Docker image. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment OR in AWS Console, CloudFormation > pick deployed Stack > Outputs (provided it is defined as output in `template.yaml`.

## Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash
finbricks-hackaton$ sam build
```

The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `first_function/requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
finbricks-hackaton$ sam local invoke FirstFunction --event events/event.json --env-vars ./.env.json
```
ENV vars are used as secrets

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
finbricks-hackaton$ sam local start-api
finbricks-hackaton$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

`NOTE`: [PyCharm] You can also rightclick on Lambda in the AWS Toolkit Explorer window

```bash
finbricks-hackaton$ sam logs -n FirstFunction --stack-name finbricks-hackaton --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests from your local machine.

## API tests

See Postman test collection in `postman_collection.json`


```bash
finbricks-hackaton$ pip install pytest pytest-mock --user
finbricks-hackaton$ python -m pytest tests/ -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name finbricks-hackaton
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
