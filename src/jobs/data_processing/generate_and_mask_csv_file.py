import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import DataFrame

from src.datasource.faker_member_data import FakerMemberData
from src.libs.base.job import BaseJob
from src.libs.column_names import ColumnNames as CN
from src.libs.mask import mask_value


class GenerateAndMaskCSVFile(BaseJob):
    def mask_dataframe(self, df: DataFrame) -> DataFrame:
        mask_value_udf = F.udf(mask_value, T.StringType())
        masked_df = (
            df.withColumn(CN.first_name, mask_value_udf(F.col(CN.first_name)))
            .withColumn(CN.last_name, mask_value_udf(F.col(CN.last_name)))
            .withColumn(CN.address, mask_value_udf(F.col(CN.address)))
        )
        return masked_df

    def clean_up(self):
        FakerMemberData(base_dir=self.config.BASE_DIR).clean_up()

    def get_faker_member_data_df(self, file_size_in_mb: int = 1) -> DataFrame:
        file_size_in_mb = float(file_size_in_mb)
        faker_member_data = FakerMemberData(base_dir=self.config.BASE_DIR)

        self.log.info("Generating file of %s mb", file_size_in_mb)
        faker_member_data.generate_csv_file(size_in_mb=file_size_in_mb)

        df = faker_member_data.get_df()

        return df

    def run(self, file_size_in_mb: int = 1) -> DataFrame:
        file_size_in_mb = float(file_size_in_mb)
        df = self.get_faker_member_data_df(file_size_in_mb=file_size_in_mb)

        self.log.info("Dataframe before masking")
        self.log.info(df.show(10, truncate=False))

        masked_df = self.mask_dataframe(df=df)

        self.log.info("Dataframe after masking")
        self.log.info(masked_df.show(10, truncate=False))

        self.clean_up()

        return masked_df
