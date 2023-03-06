from setuptools import setup
from master import VERSION

setup(
    name="masterpass",
    version=VERSION,
    description="Deterministic passwords for everyone",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="jpedro",
    author_email="jpedro.barbosa@gmail.com",
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
    # install_requires=[
    #     "click",
    # ],
    entry_points={
        "console_scripts": [
            "master=master.cli:main",
        ],
    },
)
