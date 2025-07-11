# !/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_engine(config):
    return create_engine(config.db_url)


def get_session(config):
    return Session(get_engine(config))
