# AWS EKS Deployment project

## Description

- This project was built for deployment to AWS Kuberntes Cluster by using CI/CD integration created by AWS CLoud formation
- This contains the base folder structure to be used for my flask backend deployment and a very simple JWT application
- Folder structure is modularized to allow plug and play of new modules/functions

## Requirements

- An AWS Account
- DockerHUB Account with docker desktop installed

## Installation

- make a clone of repository
- python>=3.5 app uses typing feature so this is an important requirement
- If on windows, gitbash will be preferred terminal of choice

## Install Dependencies

- Create a virtual environment

```bash
pip install virtualenv
virtualenv <environment_name>
```

- Activate the environment

linux/Git Bash:

```bash
source <environment_name>/bin/activate
```

Windows:

```bash
'<environment_name>\Scripts\activate'
```

- Install dependencies

```bash
pip install -r requirements.txt
```

## Verify App

- At this point you can verify the app is working by serving/running it either by using flask or gunicorn
- you can use a different port number if u wish to

- using flask

``` bash
flask run -p 8080
```

- using gunicorn

``` bash
gunicorn -b :8080 app:app
```

To test:

``` bash
curl http://localhost:8080
```

This should return a string `Healthy`

```bash
curl -X POST http://localhost:8080/auth -H 'Content-Type: application/json' -d '{"email":"my_email","password":"my_password"}'
```

This should return a json object in the form:

```python
{
  'token':'long jwt token'
}
```

```bash
curl http://localhost:8080/contents -H 'Content-Type: application/json' -H 'Authorization: Bearer long jwt token'
```

This should return a json object in the form:

```python
{
  "email":"my_email",
  "password":"my_password"
}
```

## Docker Image build

- Please follow instructions [here](https://docs.docker.com/engine/install/) on how to setup docker

To build docker image from DockerFile run:

```bash
docker build -t `imagename` .
```

or

```bash
docker build -t `imagename` DockerFile
```

check images list:

```bash
docker image ls
```

remove image:

```bash
docker image rm `imagename`
```

## Docker Container

- Creating a container is also easy, run:

```bash
docker run --name containerName --env-file=.env -p 80:8080 myimage
```

- `--name` is the name of the container to create
- `--env-file` is the env file with variables necessary fr the app to run, in our case it is the .env file in the directory
- `-p 80:8080` specifies the external port assigned to listen to the internal port, the app internally runs at port 8080 and docker exposes it at port 80 for us, this can be changed as you wish

check containers list:

```bash
docker container ls
```

Stop a container:

```bash
docker container stop containerName
```

Remove a container:

```bash
docker container rm containerName
```

## Verify Docker

- Refer to the same commands in [verify-app](#verify-app)
- Change the port number to match -p command when you run the container

## AWS Deployment

- Necessary cli tools needs to be installed to enable aws deployment, it is also required to have an AWS account/AWS IAM user with Administrator role assigned
- ekctl: a simple command line utility for creating and managing Kubernetes clusters on Amazon EKS
- kubectl: command line utility for communicating with the cluster API server, also necessary for `CI/CD`

### AWS Required Installations

- First install aws cli, follow instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Install eksctl, follow instructions [here](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)
- Install kubectl, follow instructions [here](https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html)

Note: if run `kubectl version --short --client` and get an error about not having access to a port, this is most likely because the configmap necessary for kubectl isnt set yet,
worry not, after a successful deployment by eksctl the configmap context will be created and set or you could install `minikube` and run `minikube start` to get a default context but that isnt necessary

### Setup AWS CLI

- On aws create your IAM User with the **AdministratorAccess** policy Attached directly and download the CSV file that contains `Access Key ID` and a `Secret Access Key`
- To setup your AWS credentials follow the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

or simply run:

```bash
# to configure cli
aws configure
# To configure cli with a new profile
aws configure --profile new_profile_name
# View current configs
aws configure list 
# View all profiles
aws configure list-profiles
```

- other cli programs will need to know where your AWS configs are

on linux you can export:

```bash
export AWS_CONFIG_FILE=~/.aws/config
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials
```

Running the above will only make them visible in your current terminal, to make a permanent reference, edit your .profile file **but** if a .bashrc file exist edit that instead and add the above command to the end of the file, for windows users you can simply search envirnment variables in search box and create them in the options

- To verify success run `aws iam list-users` or `aws iam list-users --profile new_profile_name` you should get an output similar to:

```JSON
{
"Users": [
    {
        "Path": "/",
        "UserName": "YOURIAMUSERNAME",
        "UserId": "USERID",
        "Arn": "arn:aws:iam::388752792305:user/YOURIAMUSERNAME",
        "CreateDate": "2019-04-11T13:25:10+02:00"
    }
  ]
}
```

### Setup AWS Role

- To allow kubectl access to our clusters we need to create a ROLE for it on AWS and assign it that ROLE
- This is an important step as kubectl is in charge of deploying the app to the cluster

First, get your AWS IAM ID/Arn run `aws sts get-caller-identity`
Now we need to create a trust relationship using a JSON file, more info [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html)

There is a `trust.json` file in the current directory to use, all you have to do is replace the arn there with the one from the above command:

```JSON
"Principal": {
  "AWS": "arn:aws:iam::413441544942:user/Admin"
}
```

Now we create the policy, which is also convienently in the directory file: `iamrolepolicycloud.json`

The next steps involve createing a **trusted role** then attaching the above policy to it

To create the role run:
`aws iam create-role --role-name YourRoleName --assume-role-policy-document file://trust.json --output json --query 'Role.Arn'`

- `--assume-role-policy-document` imortant to leave the file:// as is or it errors, it links the trust.json file
- `--role-name` name of the role
- `--query` information to query and display, we are querying the ARN/amazon resource names of the role

Now we attach the policy to the role we created above run:
`aws iam put-role-policy --role-name YourRoleName --policy-name eks-describe --policy-document file://iamrolepolicy.json`

That basically gives that role the policy access to eks and ssm, read [here](https://docs.aws.amazon.com/cli/latest/reference/iam/put-role-policy.html)

With that done, you are ready for Deployment! Although we wont be implementing **CI/CD** here as that requires a long cloud formation template which i don't know how to create .. yet :D, we will be deploying manually.

## Deployment

- On your DockerHub create a public repository to use. `simple-jwt-api` will be default going foward.

Create AWS EKS cluster:

```bash
eksctl create cluster --name eksctl-demo  --profile new_profile_name
```

Build docker image if you havent already:

```bash
docker build -t `imagename` .
```

Push image to docker

```bash
docker push <username>/simple-jwt-api:latest
```

If you are logged in to docker desktop (Which you should) You can skip the username:

```bash
docker push simple-jwt-api:latest
```

Now we deploy our simple app to our created cluster by using kubectl

- open the file `simple_jwt_api`, under container replace the CONTAINER_IMAGE with `<docker username>/simple-jwt-api`

Create deployment:
`kubectl apply -f simple_jwt_api.yml`

Other useful Commands:

```bash
# Verify the deployment
kubectl get deployments
# Check the rollout status
kubectl rollout status simple_jwt_api/simple-jwt-api
# Show the pods in the cluster
kubectl get pods
# Show the services in the cluster
kubectl describe services
# Display information about the cluster
kubectl cluster-info
```
