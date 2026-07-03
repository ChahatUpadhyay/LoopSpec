from setuptools import setup, find_packages

setup(
    name="limit-order-book-simulator",
    version="0.1.0",
    description="A realistic limit order book market simulator",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "pytest>=7.0.0",
        "flask>=2.0.0",
    ],
    extras_require={
        "performance": ["numpy>=1.24.0", "pandas>=2.0.0"],
    },
)
