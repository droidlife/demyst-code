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
parser.add_argument(
    "-args",
    "--arguments",
    dest="arguments",
    action="append",
    nargs="+",
    help="select the job name to run",
    metavar="FILE",
)

args = parser.parse_args()

job_name = args.job_name

kwargs = {}
if args.arguments:
    kwargs = {
        argument[0].split("=")[0]: argument[0].split("=")[1]
        for argument in args.arguments
    }

if __name__ == "__main__":
    if job_name is None:
        raise ValueError(
            "No Job name found. Please specify job name by --job_name=<name>"
        )
    if job_name not in JobSource.__members__:
        raise ValueError(
            "Invalid job name found. Valid jobs are %s",
            list(JobSource.__members__.keys()),
        )

    JobSource[job_name].value().run(**kwargs)
