from src.libs.base.job import BaseJob


class GenerateAndMaskCSVFile(BaseJob):
    def run(self):
        self.log.info(self.config.BASE_DIR)
        print("running")
