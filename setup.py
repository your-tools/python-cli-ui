from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli-ui",
    version="0.17.2",
    author="Dimitri Merejkowsky",
    author_email="dimitri@dmerej.info",
    description="Build Nice User Interfaces In The Terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-tools/python-cli-ui",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.1",
        "tabulate>=0.8.3",
        "unidecode>=1.0.23",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.3",
            "flake8>=5.0",
            "flake8-bugbear>=22.7",
            "flake8-comprehensions>=3.10.0",
            "pep8-naming>=0.13.1",
            "isort>=5.7.0",
            "mypy>=0.960",
        ]
    },
    entry_points={
        "console_scripts": [
            "cli-ui=cli_ui:main",
        ],
    },
)