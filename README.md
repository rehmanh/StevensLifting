# Stevens Lifting

#### Requirements
- python 3 (version 3.9+)
- pip
- django version 4.1

#### Installation
1. Clone project
2. Install Python 3.9+
3. Install django version 4.1 `pip install django==4.1` in project directory
4. Setup Virtual Environment. For UNIX/macOS `source lifting/bin/activate`. To deactivate, just run `deactivate` (Windows users just google it)
5. Verify that Django is running and setup correctly by running `django-admin` from CLI

#### Launching Application Locally
1. Make sure virtual environment is launched
2. From project root, `cd stevenslifting`
3. Run `python3 manage.py runserver`
4. Navigate to http://127.0.0.1:8000/ to see it in action


*****
#### Some useful Django commands (UNIX):

- To launch an environment: `source lifting/bin/activate`
- To deactivate launched environment: `deactivate`
- To run app server: `python3 manage.py runserver`
- To generate migration files (after model object changes are made): `python3 manage.py makemigrations`
- To run migration command (after makemigrations): `python3 manage.py migrate`
- To launch the Django shell: `python3 manage.py shell`, and make sure to `from base.models import <ModelName>` to access rows

#### Troubleshooting:
If for some reason a change is made to a Model object that results in a broken migration (for example, a foreign key added AFTER migrating a table), then 
you might want to wipe out the db and migration files and start fresh:
1. delete `db.sqlite3` file
2. delete all migration files
3. run `python3 manage.py makemigrations` to re-generate migration files and sqlite file
4. finally `python3 manage.py migrate`. the `db.sqlite3` file should be automatically regenerated

