#!/usr/bin/env sh

# Script to create remote repository and install dependencies with poetry

read -p "Enter the name of the remote repository: " PROYECT_DESCRIPTION

# create remote repository
gh repo create --private --remote origin --source=. --description $PROYECT_DESCRIPTION

# install dependencies
poetry init \ 
    --author "Cristobal Villanueva <cristobal.villanueva@geovalidata.com>" \
    --description $PROYECT_DESCRIPTION \
    --no-interaction
poetry add fastapi sqlalchemy
poetry add -D mypy black isort autoflake python-dotenv pytest
