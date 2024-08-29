import pytest
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, StructField, StructType

from src.libs.column_names import ColumnNames as CN


@pytest.fixture(scope="session")
def mock_faker_member_data(spark_session) -> DataFrame:
    faker_member_df = spark_session.createDataFrame(
        [
            ("Hans", "Camacho", "726 Earl Circle", "2022-03-02"),
            ("Twanda", "Bradley", "1381 Amador Path", "2023-03-10"),
        ],
        StructType(
            [
                StructField(CN.first_name, StringType(), False),
                StructField(CN.last_name, StringType(), False),
                StructField(CN.address, StringType(), False),
                StructField(CN.date_of_birth, StringType(), False),
            ]
        ),
    )

    return faker_member_df
