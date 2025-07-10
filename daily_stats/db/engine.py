# !/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine


def get_engine(config):
    return create_engine(config.db_url)
