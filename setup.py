import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-maxautolint-ngoodger",
    version="0.0.1",
    author="Nikolaj Goodger",
    author_email="ngoodger@protonmail.com",
    description="Fast parallel runner for python code tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngoodger/python_max_autolint",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
