from setuptools import setup

setup(
    name='txwebretry',
    version='0.1.0',
    description='Retry Twisted web requests',
    long_description='Utilities for retrying requests with twisted.web.client and derivatives.',
    url='https://github.com/wrapp/txwebretry',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    keywords='twisted web retry',
    install_requires=['twisted', 'txretry'],
    py_modules=['txwebretry']
)
