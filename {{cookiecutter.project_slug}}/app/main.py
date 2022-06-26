import logging

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import TIMEZONE_LOCAL
from app.utils import get_local_now_datetime

app = FastAPI(
    title="API Title",
    description=f"Last deployment: {get_local_now_datetime(TIMEZONE_LOCAL).strftime('%Y-%m-%d %H:%M:%S')}",
    redoc_url=None,
    dependencies=[],
)

# wraps all server error in json response for frontend
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            {"detail": "Error del servidor"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    logger.error({"Erro de validacion con body": exc.body})

    failed_cols = []
    for err_dict in exc.errors():
        for col in err_dict["loc"]:
            failed_cols.append(col)

    failed_cols_unique = set(failed_cols)
    try:
        failed_cols_unique.remove("body")
    except KeyError:
        pass
    failed_cols_str = ", ".join(list(failed_cols_unique))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": f"Valores no validos para la(s) columna(s): '{failed_cols_str}'",
                "body": exc.body,
            }
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Hello"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
else:
    # set logging when runned from gunicorn
    gunicorn_logger = logging.getLogger("gunicorn.warning")
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
