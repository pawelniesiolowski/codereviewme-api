Code Review Me
==============
### *Experience is the name everyone gives to their mistakes.* – Oscar Wilde

### This is the main API for the *Code Review Me* application that helps novice programmers find experienced mentors.

# Technologies
- Python
- Flask
- Postgress
- SQLAlchemy
- JWT
- REST

# Deployment
## Locally
- clone github repository
- create virtual environment: `python3 -m venv codereviewme-api`
- install requirements: `pip install -r requirements.txt`
- create Postgres codereviewme database: `createdb codereviewme`
- run migration script: `python manage.py db upgrade`
- run `setup.sh` to set environment variables and then run Flask app: `export $(cat setup.sh | xargs) && flask run`
### Run tests suite
- create Postgres codereviewme_test database: `createdb codereviewme_test`
- run tests: `pytest`

## On Heroku
- create account on Heroku: https://signup.heroku.com/
- install Heroku CLI: `sudo snap install --classic heroku`
- login to Heroku CLI: `heroku login`
- create Heroku app: `heroku create codereviewme-api` and copy outputed git url
- add git remote Heroku to local repository: `git remote add heroku https://git.heroku.com/codereviewme-api.git`
- create Heroku addon to create database and connect it to application: `heroku addons:create heroku-postgresql:hobby-dev --app codereviewme-api`
- to check configuration variables: `heroku config --app codereviewme-api`
- create additional config vars on Heroku dashboard: https://dashboard.heroku.com/
- push application to Heroku: `git push heroku master`
- run database migration on Heroku: `heroku run python manage.py db upgrade --app codereviewme-api`

# Api url
https://codereviewme-api.herokuapp.com/

# Api documentation
[Code Review Me API](./app/code_review/README.md)

# License
Copyright © 2019 Paweł Niesiołowski. MIT license.
