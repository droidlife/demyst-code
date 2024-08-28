# pylint: disable=invalid-name
from enum import Enum

from src.jobs.data_processing.generate_and_mask_csv_file import GenerateAndMaskCSVFile


class JobSource(Enum):
    generate_and_mask_csv_file = GenerateAndMaskCSVFile
