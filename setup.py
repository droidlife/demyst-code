from setuptools import find_packages, setup


# Read the requirements from a file (usually requirements.txt)
with open("requirements.txt", encoding="utf-8") as f:
    required = f.read().splitlines()

with open("README.md", encoding="utf-8") as f:
    description = f.read()

setup(
    name="Demyst Code",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    author="Ankur Jain",
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
)
