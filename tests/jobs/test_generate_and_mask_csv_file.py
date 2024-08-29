# pylint: disable=duplicate-code, unused-argument
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StringType, StructField, StructType

from src.jobs.data_processing.generate_and_mask_csv_file import GenerateAndMaskCSVFile
from src.libs.column_names import ColumnNames as CN
from tests.utils import assert_df_equality


def test_get_faker_member_data_df(spark_session: SparkSession, stub_data_sources):
    generate_and_mask_csv_file = GenerateAndMaskCSVFile()

    actual_df = generate_and_mask_csv_file.get_faker_member_data_df()

    expected_df = spark_session.createDataFrame(
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
    assert_df_equality(expected_df, actual_df)


def test_mask_dataframe(spark_session: SparkSession):
    generate_and_mask_csv_file = GenerateAndMaskCSVFile()

    df = spark_session.createDataFrame(
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

    actual_df = generate_and_mask_csv_file.mask_dataframe(df=df)

    expected_df = spark_session.createDataFrame(
        [
            ("H**s", "C*****o", "7*************e", "2022-03-02"),
            ("T****a", "B*****y", "1**************h", "2023-03-10"),
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
    assert_df_equality(expected_df, actual_df)
