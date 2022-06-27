from datetime import datetime, timezone

from pydantic import BaseModel, root_validator


class BaseModelCustom(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def empty_string_to_none(cls, values):
        for key, value in values.items():
            if isinstance(value, str) and value == "":
                values[key] = None
        return values

    @root_validator(pre=True)
    def datetime_to_utc(cls, values):
        for key, value in values.items():
            if isinstance(value, datetime):
                values[key] = value.astimezone(timezone.utc)
        return values
