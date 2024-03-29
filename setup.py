from setuptools import setup

setup(
    name='api-flask',
    packages=['api'],
    python_requires='>=3.9',
    install_package_data=True,
    install_requires=[
        'flask>=1.1.2',
        'flask-sqlalchemy>=2.4.4',
        'flask-migrate>=2.7.0',
        'flask-restful>=0.3.8',
        'flask-marshmallow>=0.14.0',
        'marshmallow-sqlalchemy>=0.24.2',
        'selenium>=3.141.0',
        'beautifulsoup4>=4.9.3',
    ],
)
