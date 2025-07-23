# !/usr/bin/env python
# encoding: utf-8

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @classmethod
    def strip(cls, data_dict):
        """
        Remove keys from the given data dict that don't match a table column.
        """
        return {k: v for k, v in data_dict.items() if k in cls.__table__.columns}
