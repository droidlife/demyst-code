ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.9.8

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

COPY . /code
WORKDIR /code

ARG PYSPARK_VERSION=3.2.0
RUN pip --no-cache-dir install pyspark==${PYSPARK_VERSION}

# Some of the dependencies needed for the env to be updated
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

RUN make install

CMD ["python", "run.py", "-job", "generate_and_mask_csv_file"]
