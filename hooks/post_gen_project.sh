#!/usr/bin/env bash

# Script to create remote repository and install dependencies with poetry and testing DB

read -p "Enter proyect description: " PROYECT_DESCRIPTION

# git
git init

# create remote repository
gh repo create --private --remote origin --source=. --description "$PROYECT_DESCRIPTION"

# install dependencies
/usr/bin/python3 -m venv .venv
poetry init --quiet --no-interaction \
    --author "Cristobal Villanueva <cristobal.villanueva@geovalidata.com>" \
    --description "$PROYECT_DESCRIPTION"
poetry add fastapi sqlalchemy uvicorn gunicorn
poetry add -D mypy black isort autoflake python-dotenv pytest

# install testing DB
sqlite3 -batch db.sqlite3 "CREATE TABLE test (id INTEGER PRIMARY KEY, f TEXT);"

touch .env
echo DB_CONNECTION_URL=sqlite:///db.sqlite3 > .env 
