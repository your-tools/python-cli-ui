import sys
import setuptools

if sys.version_info.major < 3:
    sys.exit("Error: Please upgrade to Python3")

setuptools.setup()
