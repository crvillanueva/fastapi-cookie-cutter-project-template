#!/bin/bash
poetry init --author "Cristobal Villanueva" --no-interaction
poetry add fastapi sqlalchemy
poetry add -D black isort autoflake python-dotenv pytest mypy
