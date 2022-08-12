from fastapi import HTTPException, status

ServerErrorException = HTTPException(
    status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error del servidor"
)


DatabaseErrorException = HTTPException(
    status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error en la base de datos"
)


class CustomDatabaseError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
