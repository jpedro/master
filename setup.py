from setuptools import setup
from master import VERSION

readme = open("README.md", "r").read()

setup(
    name="master",
    version=VERSION,
    description="Generates deterministic passwords for services",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="ptdorf",
    author_email="ptdorf@gmail.com",
    url="https://github.com/jpedro/master",
    download_url="https://github.com/jpedro/master/tarball/master",
    keywords="deterministic password",
    license="MIT",
    python_requires='>=3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=[
        "master",
    ],
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "master=master.cli:cli",
        ],
    },
)
