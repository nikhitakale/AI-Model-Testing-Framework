from setuptools import setup, find_packages

setup(
    name="ai-model-testing-framework",
    version="1.0.0",
    description="Comprehensive AI/ML Model Testing Framework for QAs",
    author="Nikhita Kale",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pytest>=7.4.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "rouge-score>=0.1.2",
        "nltk>=3.8.1",
        "fairlearn>=0.9.0",
        "locust>=2.15.0",
        "memory-profiler>=0.61.0",
        "matplotlib>=3.7.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.1.0",
            "pytest-html>=3.2.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aitest=cli.main:main",
        ],
    },
)
