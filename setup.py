from setuptools import setup, find_packages

setup(
    name="bike-builder-checklist",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit==1.24.0",
        "pandas==2.0.3",
    ],
)
