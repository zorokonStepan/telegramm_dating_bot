from typing import List

import sqlalchemy as sa
from sqlalchemy import Column, DateTime

from create_bot import db


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(), server_default=db.func.now())
    updated_at = Column(DateTime(),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())
