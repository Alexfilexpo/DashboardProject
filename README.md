# DashboardProject

Test dashboard project with charts and PostgreSQL db in the GCP (GoogleCloudPlatform)

# Tools

- **DjangoRestFramework 3.11.1** - API creation. API used as relation of backend and frontend of main application with PostgreSQL DB.
- **Django 3.1.1** - Main web application.
- **matplotlib 3.3.1** - Library for creating charts.
- **requests 2.24.0** - Library for requests handling.

# Install 

```
git clone https://github.com/Alexfilexpo/DashboardProject  # Clone repo

python3 -m venv venv  # Create virtualenvironment

. venv/bin/activate  # Activate virtualenv

pip install -i requirements.txt  # Install required tools and frameworks
```

# Configuration

It's very important to create environmental variables used for valid cooperation with PostgreSQL instance on GCP;
```
'DB_NAME_DJANGO'  # Name of postgresql db for data
'DB_USER_DJANGO'  # User to access the db
'PASSWORD'  # User password to access the db
'CLOUD_SQL_INSTANCE_IP'  # IP of PostgreSQL instance inside GCP
```
Also very important to remember - for running migrations in terminal, assure that variables can be accessed from terminal.

Create first superuser

```
python manage.py createsuperuser
```

# Run

```
python manage.py runserver

Open 0.0.0.0:8000 in web browser
```