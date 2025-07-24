# !/usr/bin/env python
# encoding: utf-8


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(config):
    """
    Helper for creating a SQLAlchemy engine using the configured database settings.
    """
    return create_engine(config.db_url)


def get_sessionmaker(config):
    """
    Helper for creating a sessionmaker using the configured database settings.
    """
    return sessionmaker(get_engine(config))
