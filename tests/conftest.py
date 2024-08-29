# pylint: disable=redefined-outer-name, wildcard-import, unused-wildcard-import
import logging

import pytest
from pyspark.sql import SparkSession

from tests.mocks.data_sources import *
from tests.stubbing.data_sources import *


def quiet_py4j():
    """Suppress spark logging for the test context."""

    logger = logging.getLogger("py4j")
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    spark_session = (
        SparkSession.builder.master("local[*]")
        .config("spark.default.parallelism", 1)
        .config("spark.sql.shuffle.partitions", 1)
        .appName("spark-local-unit-tests")
        .getOrCreate()
    )

    quiet_py4j()
    return spark_session


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
