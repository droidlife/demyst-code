import logging
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from src.configs import config_by_name
from src.configs.default import Config

from .spark import SparkMixin


logging.basicConfig(level=logging.INFO)


load_dotenv(override=True)


class BaseJob(SparkMixin, ABC):
    config: Config = config_by_name[os.environ["ENVIRONMENT"]]
    log = logging.getLogger(__name__)

    @abstractmethod
    def run(self):
        pass
