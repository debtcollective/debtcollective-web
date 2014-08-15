# -*- coding: utf-8 -*-
import os, unittest

from url_config import base
from url_config.django import database as django_database
from url_config import pymongo
from url_config import redis
from url_config import paypalrestsdk
from url_config.django import cache as django_cache

class TestBase(unittest.TestCase):
    pass

class TestDjangoDatabase(TestBase):
    def test_postgres_from_url(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        config = django_database.from_url(url)

        assert config['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert config['NAME'] == 'd8r82722r2kuvn'
        assert config['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert config['USER'] == 'uf07k1i6d8ia0v'
        assert config['PASSWORD'] == 'wegauwhgeuioweg'
        assert config['PORT'] == 5431

    def test_to_url(self):
        actual = django_database.to_url({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'hostname',
            'NAME': 'database',
            'PASSWORD': 'password',
            'PORT': '999',
            'USER': 'username'
        })

        self.assertEquals(actual, "postgres://username:password@hostname:999/database")

    def test_external_engine(self):
        actual = django_database.to_url({
            'ENGINE': 'some.backend',
            'HOST': 'hostname',
            'NAME': 'database',
            'PASSWORD': 'password',
            'PORT': '999',
            'USER': 'username'
        })
        self.assertEquals(actual, "external://username:password@hostname:999/database?external_engine=some.backend")

    def test_round_trip(self):
        value = "postgres://username:password@hostname:999/database"
        self.assertEquals(django_database.to_url(django_database.from_url(value)), value)

    def test_external_engine_round_trip(self):
        value = "external://username:password@hostname:999/database?external_engine=some.backend&param=1"
        self.assertEquals(django_database.to_url(django_database.from_url(value)), value)

    def test_params_as_options(self):
        actual = django_database.to_url({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'hostname',
            'NAME': 'database',
            'PASSWORD': 'password',
            'PORT': '999',
            'USER': 'username',
            'OPTIONS': {
                'param': '1',
            }
        })

        self.assertEquals(actual, "postgres://username:password@hostname:999/database?param=1")

    # The remainder of this class was taken from dj-database-url 0.3.0, slightly adapted for API compat.
    def test_postgres_parsing(self):
        url = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_postgis_parsing(self):
        url = 'postgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.postgis'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_mysql_gis_parsing(self):
        url = 'mysqlgis://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.contrib.gis.db.backends.mysql'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_cleardb_parsing(self):
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.db.backends.mysql'
        assert url['NAME'] == 'heroku_97681db3eff7580'
        assert url['HOST'] == 'us-cdbr-east.cleardb.com'
        assert url['USER'] == 'bea6eb025ca0d8'
        assert url['PASSWORD'] == '69772142'
        assert url['PORT'] is ''

    def test_database_url(self):
        try:
            del os.environ['DATABASE_URL']
        except KeyError:
            pass

        a = django_database.parse()
        assert not a

        os.environ['DATABASE_URL'] = 'postgres://uf07k1i6d8ia0v:wegauwhgeuioweg@ec2-107-21-253-135.compute-1.amazonaws.com:5431/d8r82722r2kuvn'

        url = django_database.parse()

        assert url['ENGINE'] == 'django.db.backends.postgresql_psycopg2'
        assert url['NAME'] == 'd8r82722r2kuvn'
        assert url['HOST'] == 'ec2-107-21-253-135.compute-1.amazonaws.com'
        assert url['USER'] == 'uf07k1i6d8ia0v'
        assert url['PASSWORD'] == 'wegauwhgeuioweg'
        assert url['PORT'] == 5431

    def test_empty_sqlite_url(self):
        url = 'sqlite://'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_memory_sqlite_url(self):
        url = 'sqlite://:memory:'
        url = django_database.from_url(url)

        assert url['ENGINE'] == 'django.db.backends.sqlite3'
        assert url['NAME'] == ':memory:'

    def test_parse_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        url = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = django_database.from_url(url, engine)

        assert url['ENGINE'] == engine

    def test_config_engine_setting(self):
        engine = 'django_mysqlpool.backends.mysqlpool'
        os.environ['DATABASE_URL'] = 'mysql://bea6eb025ca0d8:69772142@us-cdbr-east.cleardb.com/heroku_97681db3eff7580?reconnect=true'
        url = django_database.parse(engine=engine)

        assert url['ENGINE'] == engine

class TestMongo(unittest.TestCase):
    def test_round_trip(self):
        value = "mongodb://username:password@hostname:999/database"
        self.assertEquals(pymongo.to_url(pymongo.from_url(value)), value)

    def test_returns_minimal(self):
        value = "mongodb://hostname/database"
        expected = {
            'NAME': 'database',
            'HOST': 'hostname',
            'PORT': None
        }
        self.assertEquals(pymongo.from_url(value), expected)


class TestRedis(unittest.TestCase):
    def test_no_password(self):
        value = "redis://hostname:999/0"
        expected =  {
            'db': 0,
            'host': 'hostname',
            'port': 999,
        }
        self.assertEquals(redis.from_url(value), expected)

    def test_round_trip(self):
        value = "redis://password@hostname:999/0?socket_timeout=1"
        self.assertEquals(redis.to_url(redis.from_url(value)), value)

class TestPaypalRESTSDK(unittest.TestCase):
    def test_round_trip(self):
        value = "paypalrest://username:password@hostname"
        self.assertEquals(paypalrestsdk.to_url(paypalrestsdk.from_url(value)), value)

    def test_returns_minimal(self):
        value = "paypalrest://username:password@hostname"
        expected = {
            'mode': 'hostname',
            'client_id': 'username',
            'client_secret': 'password'
        }
        self.assertEquals(paypalrestsdk.from_url(value), expected)

class TestCache(unittest.TestCase):
    def test_round_trip(self):
        value = "pylibmc://username:password@hostname1:100;hostname2:101/?key_prefix=test&timeout=10"
        self.assertEquals(django_cache.to_url(django_cache.from_url(value)), value)

    def test_multiple_hosts(self):
        value = "pylibmc://username:password@hostname1:100;hostname2:101/?key_prefix=test&timeout=10"
        self.assertEqual(django_cache.from_url(value)['LOCATION'], ['hostname1:100', 'hostname2:101'])

    def test_returns_minimal(self):
        value = "pylibmc://hostname1/"
        expected = {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'LOCATION': 'hostname1'
        }
        self.assertEquals(django_cache.from_url(value), expected)

    def test_to_url_string_location(self):
        config = {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'LOCATION': 'hostname1'
        }
        self.assertEquals(django_cache.to_url(config), 'pylibmc://hostname1/')

    def test_locmem(self):
        actual = django_cache.to_url({
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test',
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        })
        self.assertEquals(actual, "locmem://test/?options=MAX_ENTRIES%3D1000")

    def test_locmem_from(self):
        actual = django_cache.from_url('locmem://test/?options=MAX_ENTRIES%3D1000')

        self.assertEquals(actual, {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'test',
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        })

    def test_external_engine(self):
        actual = django_cache.to_url({
            'BACKEND': 'some.backend',
            'LOCATION': 'hostname',
            'PASSWORD': 'password',
            'USERNAME': 'username'
        })
        self.assertEquals(actual, "external://username:password@hostname/?external_backend=some.backend")


if __name__ == '__main__':
    unittest.main()
