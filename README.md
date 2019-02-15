# Simple Identity Service (w/Terraform&Packer)

A simple identity microservice. NGINX/gunicorn/aiohttp is the server stack.
Packer and Terraform are used to deploy this microservice to the AWS cloud.

## Setup

### Prerequisites

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


### Install Python Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Download AWS EC2 Key Pair

We will need a EC2 Key Pair to authenticate with EC2 instances over SSH.
Terraform and Packer use the `*.pem` keyfile to provision and configure images.
After deployment, a developer may use this key pair to verify the
deployment by connecting to an instance over SSH.

[The AWS Docs have instructions on how to create and download a key pair.](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) You will likely have to use `chmod 400 <PATH_TO_KEY>/<KEY_NAME>.pem`
to set the correct file permisions.

### Setup PostgreSQL

We may either target a local or AWS RDS PostgreSQL database. The chosen option
will dictate the values of environment variables, when we set them up later.


0. Create database and database user, either locally on on AWS.

  ---------------------------------------------------------------------------

#### Local PostgreSQL Setup

```bash
$ sudo su - postgres
$ psql
psql (10.6 (Ubuntu 10.6-0ubuntu0.18.04.1))
Type "help" for help.

postgres=# CREATE DATABASE identitydb;
CREATE DATABASE
postgres=# CREATE USER identity_db_user PASSWORD 'YYYYYYYYYY';
CREATE ROLE
postgres=# \q
```

#### AWS RDS PostgreSQL Setup

[Follow instructions to create a PostgreSQL database in AWS RDS.](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html)

  - `NOTE` Be sure to make note of your database username, database password,
    and public DNS endpoint of created database.

  ---------------------------------------------------------------------------

1. Setup environment variables with the information entered into AWS.

  - We only need to set the `DB_NAME`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`,
    and `DB_HOST` variables. The other env vars may be ignored -- for now.
  - If using AWS, `DB_HOST` is the public DNS endpoint of the created database.
  - If using localhost, `DB_HOST` is `127.0.0.1`.

2. Login as new user, to validate role creation

```bash
$ psql -h $DB_HOST -U $DB_USERNAME --password -p $DB_PORT -d $DB_NAME
```

3. Import DB Schema

```bash
$ psql -h $DB_HOST -U $DB_USERNAME --password -p $DB_PORT -d $DB_NAME < db_schema.psql
```

### Setup AWS credentials

Terraform and Packer need access to your AWS credentials, in order to provision
resources on your behalf.

[The easiest way to do this is to setup your credentials for the AWS CLI.](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
If the AWS CLI works, then your credentials should be properly configured!

### Setup up environment variables

0. Create a `.env` file

1. Populate it with environment variable information, using your favorite text editor:

```bash
export AWS_PROFILE="default"
export SSH_KEY_PATH="/<PATH_TO_AWS_PEM>/<AWS_PEM_FILE>.pem"
export SIMPLE_IDENTITY_PROJECT="/<PATH_TO_PROJECT>/simple_identity_service"
export DB_NAME="identitydb"
export DB_PORT=5432
export DB_USERNAME="identity_db_user"
export DB_PASSWORD="YYYYYYYYYY"
export DB_HOST="XXXXXXXXXXXXXXXXXXXXXXX"
export AUTH_SIMPLE_IDENT="XXXXXXXXXXXXXXXX"
```

Variable notes

  - `DB_HOST` is either `127.0.0.1` or the IP of your AWS RDS PostgreSQL instance.
  - `AUTH_SIMPLE_IDENT` is a secret that every client must include with every API request.

2. Load the environment variables into the environment

   - `NOTE` This step is necessary whenever we open a new shell, unless fully
      qualified path is sourced from `~/.bashrc`.

```bash
source ./env
```
