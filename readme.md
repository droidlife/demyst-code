# Demyst Code

[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)  

Demyst code is the solution to the following [Problem Statement](https://github.com/DemystData/code-kata/tree/data-eng?tab=readme-ov-file#problem-2)

In this readme
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Testing](#testing)
- [Makefile Commands](#makefile-commands)
- [Future Improvements](#future-improvements)

## Project Structure

```
src/
├── __init__.py
└── models/
│   ├── __init__.py
│   ├── model.py
└── datasource/
│   ├── __init__.py
│   ├── datasource.py
└── configs/
│   ├── __init__.py
│   ├── config.py
└── libs/
│   ├── __init__.py
│   ├── libs.py
│   ├── base/
└── jobs/
│   ├── __init__.py
│   ├── jobs.py
tests/
├── conftest.py
└── mocks/
└── stubbing/
└── test_example.py
...
run.py
setup.py
```

### Directory and File Descriptions

*   **src/**: The main application directory where all the core logic of the project resides.
    
    *   **jobs/**: Contains all the jobs 
            
    *   **config/**: Houses configuration files for different environments.
        
        *   **default.py**: The base configuration with default settings.
            
    *   **datasource/**: Contains datasources i.e data readers
            
    *   **libs/**: Utility functions and helpers.
                    
*   **tests/**: Contains all the test cases for the application.
    
    *   **conftest.py**: Configuration for pytest, including fixtures.
        
    *   **test\_example.py**: An example test case to demonstrate testing structure.
                
*   **run.py**: The main entry point of the application.
    
*   **setup.py**: The setup script for installing the src as a package, managing dependencies, and more.


## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/droidlife/demyst-code
cd demyst-code
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
make install-dev
```

### 4. Set up [pre-commit hooks](https://pre-commit.com/)
```bash
pre-commit install
```
This repository is configured to enforce code quality and style consistency using pre-commit hooks. The following tools are integrated into the pre-commit configuration:

- **Black**: A code formatter that ensures Python code is styled consistently.
- **isort**: A Python utility that sorts imports.
- **Pylint**: A tool that checks for code errors, enforces coding standards, and looks for code smells.
- **Typos**: A tool to find and fix typos in your codebase.

### 5. Set Up Environment Variables

Create a `.env` file in the project root or export the environment variables directly:

```bash
export ENVIRONMENT=local
```

### 6. Run the job

```bash
make generate_and_mask_csv_file
```

## Testing

### Setting Up for Testing

Testing is handled using `pytest`. The tests are configured to create a spark-session, mocks and stubs

### Running Tests

To run tests, simply execute:

```bash
make test
```

### Example Test Case

```python
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
```

## Makefile Commands

This project uses a `Makefile` to simplify common development tasks. Below is a list of the available commands along with their descriptions.

### Available Commands

| Command             | Description                                                                                   |
|---------------------|-----------------------------------------------------------------------------------------------|
| `help`              | Display this help message                                                                     |
| `install`           | Install pip requirements needed to run the server                                             |
| `install-dev`       | Install pip requirements for local development                                                |
| `format`            | Format code using `black`                                                                     |
| `lint`              | Lint the code using `pylint`                                                                  |
| `test`              | Run tests using `pytest`                                                                      |
| `run-coverage-test` | Run tests and generate a test coverage report; fails if coverage is below the threshold (80%) |
| `build`             | Build the Docker container for deployment                                                     |
| `run`               | Run docker container                                                                          |

### Usage Examples

- **Install dependencies**: 
  ```sh
  make install
  ```

- **Format the code**:
  ```sh
  make format
  ```

- **Run tests**:
  ```sh
  make test
  ```

- **Build Docker image**:
  ```sh
  make build
  ```

- **Run the job**:
  ```sh
  make run
  ```

### Arguments

You can customize the behavior of some commands using the following arguments:

- `NAME`: The name of the Docker image (default: `demyst`)
- `COVERAGE_THRESHOLD`: Minimum coverage percentage for tests (default: `80`)
- `ENVIRONMENT`: Environment (default: `local`)

## Future Improvements
