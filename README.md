# Simple Identity Service (w/Terraform&Packer)

A simple identity microservice. NGINX/gunicorn/aiohttp is the server stack.
Packer and Terraform are used to deploy this microservice to the AWS cloud.

## Setup

### Environment Prerequisites

```
1. Python      (>= 3.5.2)
2. PostgreSQL  (>= 9.5.13)
3. NGINX       (>= 1.10.3)
4. Packer      (>= 1.3.2)
5. Terraform   (>= 0.11.10)
```

Install instructions (tested on Ubuntu 16.04; gcc5.4.0)

0. [Install Terraform (Link)](https://learn.hashicorp.com/terraform/getting-started/install.html)
1. [Install Packer (Link)](https://www.packer.io/intro/getting-started/install.html)
2. Install various other packages

```
sudo apt-get update
sudo apt-get install -y \
                        nginx \
                        python3 \
                        python3-pip \
                        postgresql \
                        postgresql-contrib

```


### Install Dependencies

```
python3 -m pip install -r requirements.txt
```

### Download AWS EC2 Key Pair

We will need a EC2 Key Pair to authenticate with EC2 instances over SSH.
Terraform and Packer use the `*.pem` keyfile to provision and configure images.
After deployment, a developer may use this key pair to verify the
deployment by connecting to an instance over SSH.

[The AWS Docs have instructions on how to create and download a key pair.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

#### Setting up environment variables
```
export AWS_PROFILE="default"
export SSH_KEY_PATH="/<PATH_TO_AWS_PEM>/<AWS_PEM_FILE>.pem"
export SIMPLE_IDENTITY_PROJECT="/<PATH_TO_PROJECT>/simple_identity_service"
export DB_NAME="identitytable"
export DB_PORT=5432
export DB_USERNAME="XXXXXXXXXXXXXXXXXXXX"
export DB_PASSWORD="XXXXXXXXXXXXXXXXXXXX"
export DB_HOST="XXXXXXXXXXXXXXXXXXXXXXX"
export AUTH_SIMPLE_IDENT="XXXXXXXXXXXXXXXX"
```

### Connecting to Database Instance
- `psql -h $DB_HOST -U $DB_USERNAME --password -p $DB_PORT -d $DB_NAME`
