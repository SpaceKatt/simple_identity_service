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

```bash
sudo apt-get update
sudo apt-get install -y \
                        nginx \
                        python3 \
                        python3-pip \
                        postgresql \
                        postgresql-contrib

```


### Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Download AWS EC2 Key Pair

We will need a EC2 Key Pair to authenticate with EC2 instances over SSH.
Terraform and Packer use the `*.pem` keyfile to provision and configure images.
After deployment, a developer may use this key pair to verify the
deployment by connecting to an instance over SSH.

[The AWS Docs have instructions on how to create and download a key pair.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

### Setup PostgreSQL

We may either target a local or AWS RDS PostgreSQL database. The chosen option
will dictate the values of environment variables, when we set them up later.

#### Local PostgreSQL Setup

0. Create database and database user

```bash
$ sudo su - postgres
$ psql
psql (10.6 (Ubuntu 10.6-0ubuntu0.18.04.1))
Type "help" for help.

postgres=# CREATE DATABASE identity;
CREATE DATABASE
postgres=# CREATE USER identity_db_user PASSWORD 'YYYYYYYYYY';
CREATE ROLE
postgres=# \q
```

1. Login as new user, to validate role creation

```bash
$ psql identity_db_user -h 127.0.0.1 -d identity
```

2. Import DB Schema

```bash
$ psql identity_db_user -h 127.0.0.1 -d identity < db_schema.psql
```

#### AWS RDS PostgreSQL Setup

### Setting up environment variables

0. Create a `.env` file

1. Populate it with environment variable information, using your favorite text editor:

```bash
export AWS_PROFILE="default"
export SSH_KEY_PATH="/<PATH_TO_AWS_PEM>/<AWS_PEM_FILE>.pem"
export SIMPLE_IDENTITY_PROJECT="/<PATH_TO_PROJECT>/simple_identity_service"
export DB_NAME="identitytable"
export DB_PORT=5432
export DB_USERNAME="identity_db_user"
export DB_PASSWORD="YYYYYYYYYY"
export DB_HOST="XXXXXXXXXXXXXXXXXXXXXXX"
export AUTH_SIMPLE_IDENT="XXXXXXXXXXXXXXXX"
```

2. Load the environment variables into the environment

   - `NOTE` This step is necessary whenever we open a new shell, unless fully
      qualified path is sourced from `~/.bashrc`.

```bash
source ./env
```

### Connecting to Database Instance
- `psql -h $DB_HOST -U $DB_USERNAME --password -p $DB_PORT -d $DB_NAME`
