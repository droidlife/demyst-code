from abc import abstractmethod

from pyspark.sql import DataFrame

from .spark import SparkMixin


class BaseDataSource(SparkMixin):
    @abstractmethod
    def get_df(self) -> DataFrame:
        pass
