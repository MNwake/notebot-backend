from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator

class BasePydanticModel(BaseModel):
    @field_validator('date', mode='before', check_fields=False)
    def ensure_utc(cls, value):
        """
        Ensures the 'date' field is always in UTC, regardless of input type (str or datetime).
        """
        if isinstance(value, str):
            parsed_date = datetime.fromisoformat(value)
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
            else:
                parsed_date = parsed_date.astimezone(timezone.utc)
            return parsed_date
        elif isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            else:
                value = value.astimezone(timezone.utc)
            return value
        return value
