import logging
import re
from typing import List

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError

from app.config import APP_PORT, APP_TIMEZONE_LOCAL
from app.utils import get_local_now_datetime

app = FastAPI(
    title="API Title",
    description=f"Last deployment: {get_local_now_datetime(APP_TIMEZONE_LOCAL).strftime('%Y-%m-%d %H:%M:%S')}",
    redoc_url=None,
    dependencies=[],
)


# SECTION: Middleware
# wraps all server errors in detail json response for frontend
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            {"detail": "Error del servidor"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# SECTION: Exception handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error({"Validation error with body": exc.body})

    error_columns: List[str] = []
    for error_dict in exc.errors():
        for column in error_dict["loc"]:
            if column != "body":
                error_columns.append(column)

    failed_cols_unique = list(set(error_columns))  # remove duplicates
    failed_cols_str = ", ".join(failed_cols_unique)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": f"Valores no validos para la(s) columna(s): '{failed_cols_str}'",
                "body": exc.body,
            }
        ),
    )


@app.exception_handler(DatabaseError)
async def database_error_exception_handler(request: Request, exc: DatabaseError):
    logger.error({"Database error": str(exc)})

    if "SEVERITY: 16" in str(exc):
        logger.error("Custom error detected")
        error_msg = re.search(
            r"##ERROR:\s(.*?)\s\|", exc.orig.args[1]
        )  # parse error msg ERROR: [CUSTOMERRORMSG] | (SEVERITY) | (CODE)
        if error_msg:
            error_msg = error_msg.group(1)
        else:
            logger.error("Can't parse custom database error message")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=jsonable_encoder(
                    {
                        "detail": "Error en el servidor",
                    }
                ),
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                {
                    "detail": error_msg,
                }
            ),
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "detail": "Error en la base de datos",
            }
        ),
    )


# SECTION: first endpoint
@app.get("/")
async def root():
    return {"msg": "Hello"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=APP_PORT,
        reload=True,
    )
else:
    # set logging when running from gunicorn
    gunicorn_logger = logging.getLogger("gunicorn.warning")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
