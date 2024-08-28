# pylint: disable=raising-format-tuple
from argparse import ArgumentParser

from src.jobs import JobSource


parser = ArgumentParser()
parser.add_argument(
    "-job",
    "--job_name",
    dest="job_name",
    help="select the job name to run",
    metavar="FILE",
)

args = parser.parse_args()

job_name = args.job_name

if __name__ == "__main__":
    if job_name is None:
        raise ValueError(
            "No Pipeline name found. Please specify pipeline name by --pipeline=<name>"
        )
    if job_name not in JobSource.__members__:
        raise ValueError(
            "Invalid job name found. Valid jobs are %s",
            list(JobSource.__members__.keys()),
        )

    JobSource[job_name].value().run()
