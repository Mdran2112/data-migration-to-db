# Data Migration app

This project consists in an app for data migration to a new Database.
It includes:

* A data pipeline to move historic data from CSV files to the new database.
* A Scheduler that generates a database backup once a day in avro format, and save it in the file system.
* A REST API to insert new data in batches. It can also restore a table from its correspondent backup file.

### Build and deploy
The script `docker_build.sh` will build a docker image with tag `db-migration-api:latest`.

Use the `docker-compose.yml` to deploy the services: MySQL database and the API. 
The compose will use some environment variables that have to be defined in a .env file:

```
API_ADMIN_USER=<Admin's User name for api authentication.>
API_ADMIN_PASSWORD=<Admin's Password for api authentication.>
STAKEHOLDER_USER=<Stakeholder's name for api authentication.>
STAKEHOLDER_PASSWORD=<Stakeholder's password for api authentication.>
MYSQL_DATABASE=<data base name. Ex: db>
MYSQL_ROOT_PASSWORD=<Password for root user.>
DATABASE_URL=<URL for connecting sqlalchemy with database. Ex: mysql+pymysql://root:admin@{mysql-container-name}:3306/db>
FIND_HISTORIC_SCHED=<Weather to schedule or not the search of historic csv files. The search will be done every five minutes. Ex: True | False>
DB_BACKUP_SCHED=<Weather to schedule or not the backup generation. The backup will be created every day at 6a.m (from Monday to Friday) . Ex: True | False>
``` 

The Admin users can interact with all endpoints.
The "stakeholder" is only allowed to interact with the metrics endpoints (see Swagger doc).

When the REST API turns on, three tables in the Database will be created: `employees`, `departments` and `jobs`.

The api container will create two volumes: `historic` and `backup`. Inside the `historic` volume
must be the csv files, that the user want to migrate. In the `backup` volume, backup avro files will be created.

### Historic data migration to Database

Each csv file with historic data has to be named like:

* `hired_employees.csv ---> employees table`
* `departments.csv ---> departments table`
* `jobs.csv ---> jobs table`

A worker will look inside the volume and if it finds a csv named as mentioned before, it will grab the data and insert it
in the correspondent table according the filename.

### Database Backup

If the environment variable `DB_BACKUP_SCHED` is set to `True`, a scheduler will build a backup from the three tables 
every day at 6 a.m. (from Mon-Fri). The backup files will be named `employees.avro`, `departments.avro` and `jobs.avro`.

You can use the `/restore/<table>` endpoint in the REST API to restore a table. The API will use the correspondent avro file for 
each table that you want to restore.

### API REST Docs
See the swagger spec. URL: `http://<host>:5000/swagger`

### Tag creation 
The repository has a github workflow for tag creation when merging to master.
When you make a PR to master, include one of the following flags in the commit message string.

* MAJOR CHANGE: `#major`
* MINOR CHANGE: `#minor`
* PATCH: `#patch `
* NONE: `#none`

For example if initial version is v0.0.0, commit message 
`ADD - certain feature #minor` will lead to `v0.1.0`. 
Then, if I make another PR to master with commit `FIX - bug in certain feature #patch`
will lead to `v0.1.1`

The workflow will build the new tag and publish it in the repository.

