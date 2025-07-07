from setuptools import setup, find_packages

setup(
    name="aysekai-international",
    version="0.1.0",
    author="Aysekai International",
    description="Islamic meditation CLI using the 99 Beautiful Names of Allah",
    packages=find_packages(exclude=['tests*', 'scripts*']),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "python-bidi>=0.4.2",
        "pyfiglet>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "asma=asma_al_husna_cli.main:app",
        ],
    },
)