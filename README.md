### Setting up environment variables
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
