from setuptools import setup, find_namespace_packages

setup(
    name="image_organizer",
    version="0.0.1",
    author="Choudhury Noor",
    description='Image Organizer',
    packages=find_namespace_packages(where='src'),
    package_dir={'':'src'},
    python_requires='>=3.7',
    install_requires=[
        'sqlalchemy'
    ],
    extras_require={
        'rest_api': [
            "flask",
            "flask-restx",
        ],
        'dev': [
            'coverage',
            'pytest',
            'pytest-sugar',
            'pylint',
            'black',
            'mypy',
            'sqlalchemy-stubs',
        ],
    },
)
