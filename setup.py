from setuptools import setup

setup(
    name='DarkWorld',
    version='1.0.0.0',
    packages=['darkworld', 'darkworld.view', 'darkworld.model', 'darkworld.controller'],
    url='https://github.com/kwoolter/DarkWorld',
    license='',
    author='kwoolter',
    author_email='kwoolter@gmail.com',
    description='Dark World Game',
    install_requires=['pygame','numpy'],
)
