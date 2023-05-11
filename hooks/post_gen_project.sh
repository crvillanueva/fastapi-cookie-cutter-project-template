#!/usr/bin/env bash

# Script to create remote repository and install dependencies with poetry and testing DB

read -p "Enter proyect description: " PROYECT_DESCRIPTION

# git
git init

# create remote repository
if [[ {{ cookiecutter.work }} = y ]]; then
  repo_name="geovalidata-spa/{{ cookiecutter.project_name }}"
else
  repo_name={{ cookiecutter.project_name }}
fi

gh repo create "$repo_name" --private --remote origin --source=. --description "$PROYECT_DESCRIPTION"

git add .
git commit -m "inicio proyecto $date"
git push -u origin main

# install dependencies
/usr/bin/python3.{{ cookiecutter.python_version }} -m venv .venv
poetry init --quiet --no-interaction \
    --author "Cristobal Villanueva <cristobaljvp@gmail.com>" \
    --description "$PROYECT_DESCRIPTION"
poetry add fastapi sqlalchemy uvicorn gunicorn python-dotenv 
poetry add -D mypy black isort autoflake pytest ipdb

# install testing DB
sqlite3 -batch db.sqlite3 "CREATE TABLE test (id INTEGER PRIMARY KEY, f TEXT);"

touch .env
echo DB_CONNECTION_URL=sqlite:///db.sqlite3 > .env 
