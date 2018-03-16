from setuptools import setup, find_packages

setup(
    name='Did Resolver',
    version='0.1',
    description='Web Resolver for Did',
    long_description='None...for now',
    author='Stephen Felt, Kyle Den Hartog, Mark Hadley',
    author_email='mark.hadley@evernym.com',
    include_package_data=True,
    packages=find_packages(exclude=['demo', 'tests'])
)