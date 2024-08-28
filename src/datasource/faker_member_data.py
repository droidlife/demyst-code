import csv
import os
import shutil

from mimesis import Address, Datetime, Person
from pyspark.sql import DataFrame

from src.libs.base.datasource import BaseDataSource
from src.libs.column_names import ColumnNames as CN


class FakerMemberData(BaseDataSource):

    file_name: str = "faker_member_data.csv"

    def __init__(self, base_dir: str):
        self.base_dir: str = base_dir
        super().__init__()

    def get_df(self: str) -> DataFrame:
        file_path = f"{self.base_dir}/{self.file_name}"
        df = (
            self.spark.read.option("header", "true")
            .option("inferschema", "true")
            .csv(file_path)
        )
        return df

    def generate_csv_file(self: str, size_in_mb: int):

        mimesis_person = Person()
        mimesis_address = Address()
        mimesis_datetime = Datetime()

        size_in_bytes = size_in_mb * 1024 * 1024  # Convert MB to bytes
        file_path = f"{self.base_dir}/{self.file_name}"

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        with open(file_path, "w", encoding="utf-8") as file:
            csvfile = csv.writer(file)
            headers = [CN.first_name, CN.last_name, CN.address, CN.date_of_birth]
            csvfile.writerow(headers)

            while True:
                address = mimesis_address.address().replace("\n", "").replace(",", "")
                data = [
                    mimesis_person.first_name(),
                    mimesis_person.last_name(),
                    address,
                    mimesis_datetime.date(),
                ]
                csvfile.writerow(data)
                if file.tell() > size_in_bytes:
                    break

    def clean_up(self):
        shutil.rmtree(self.base_dir)
