import sys
from setuptools import setup, find_packages

if sys.version_info.major < 3:
    sys.exit("Error: Please upgrade to Python3")


def get_long_description():
    with open("README.rst") as fp:
        return fp.read()


setup(name="python-cli-ui",
      version="0.7.0",
      description="Build Nice User Interfaces In The Terminal",
      long_description=get_long_description(),
      url="https://github.com/SuperTanker/python-cli-ui",
      author="Dimitri Merejkowsky",
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        "colorama",
        "tabulate",
        "unidecode",
      ],
      classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
      ],
      entry_points={
        "console_scripts": [
          "tsrc = tsrc.cli.main:main",
         ]
      }
      )
