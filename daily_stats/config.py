# !/usr/bin/env python
# encoding: utf-8

import os

from dotenv import load_dotenv
from sqlalchemy import URL


class Config:
    def __init__(self):
        load_dotenv()
        self.alma_token = os.environ.get('ALMA_TOKEN')
        self._db_url = os.environ.get('DB_URL')
        self.db_driver = os.environ.get('DB_DRIVER', 'mysql+pymysql')
        self.db_host = os.environ.get('DB_HOST', 'localhost')
        self.db_port = os.environ.get('DB_PORT', 3306)
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_database = os.environ.get('DB_DATABASE')
        self.ssl_ca_path = os.environ.get('SSL_CA_PATH')
        self.ssl_key_path = os.environ.get('SSL_KEY_PATH')
        self.ssl_cert_path = os.environ.get('SSL_CERT_PATH')
        self.log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
        self.log_dir = os.environ.get('LOG_DIR', '/var/log/daily-stats')

        # unset defaults if db_url is set
        if self._db_url:
            self.db_driver = self._db_url.split(':')[0]
            self.db_host = None
            self.db_port = None

    @property
    def db_url(self):
        if self._db_url:
            return self._db_url
        else:
            return URL.create(
                self.db_driver,
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                database=self.db_database,
                port=self.db_port,
            ).render_as_string(hide_password=False)

    @property
    def use_ssl(self):
        return all(
            [
                ssl_path is not None
                for ssl_path in [
                    self.ssl_ca_path,
                    self.ssl_key_path,
                    self.ssl_cert_path,
                ]
            ]
        )

    @property
    def ssl_args(self):
        if self.use_ssl:
            return {
                'ssl_ca': self.ssl_ca_path,
                'ssl_key': self.ssl_key_path,
                'ssl_cert': self.ssl_cert_path,
            }
        else:
            return {}

    def as_dict(self):
        return {
            'alma_token': self.alma_token,
            'db_url': self.db_url,
            'db_driver': self.db_driver,
            'db_host': self.db_host,
            'db_port': self.db_port,
            'db_user': self.db_user,
            'db_password': self.db_password,
            'db_database': self.db_database,
            'use_ssl': self.use_ssl,
            'ssl_ca_path': self.ssl_ca_path,
            'ssl_key_path': self.ssl_key_path,
            'ssl_cert_path': self.ssl_cert_path,
        }
