from setuptools import setup

setup(
    name='api-flask',
    packages=['api'],
    python_requires='>=3.9',
    install_package_data=True,
    install_requires=[
        'flask>=1.1.2',
        'selenium>=3.141.0',
        'beautifulsoup4>=4.9.3',
    ],
)
