"""
Setup script for the SearchAgent application.
"""
from setuptools import setup, find_packages

setup(
    name="SearchAgent",
    version="0.1.0",
    description="A Flask web application that generates ice breakers based on LinkedIn and Twitter profiles",
    author="SearchAgent Team",
    author_email="info@searchagent.com",
    url="https://github.com/searchagent/ice-breaker",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.1",
        "openai>=1.0.0",
        "gradio>=3.40.0",
        "flask>=2.2.0",
        "numpy>=1.24.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "tweepy>=4.14.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "black>=23.3.0",
            "isort>=5.12.0",
        ],
        "tracking": [
            "wandb>=0.15.0",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "SearchAgent": ["src/templates/*", "src/static/*"],
    },
    entry_points={
        "console_scripts": [
            "searchagent=SearchAgent.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 