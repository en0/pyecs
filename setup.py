from setuptools import setup


with open("README.md", "r") as fp:
    long_description = fp.read()


with open("requirements.txt", "r") as fp:
    install_requires = [l.rstrip("\n") for l in fp.readlines() if l.rstrip("\n")]


setup(
    name="pyecs",
    version="1.0.0",
    description="A pygame framwork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/pyecs",
    packages=["pyecs", "pyecs.services", "pyecs.systems"],
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

