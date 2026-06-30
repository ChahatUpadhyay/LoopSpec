from setuptools import setup, find_packages

setup(
    name="loopspec",
    version="2.0.0",
    description="Self-correcting, context-aware AI development protocol",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ChahatUpadhyay",
    url="https://github.com/ChahatUpadhyay/LoopSpec",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "loopspec=loopspec.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
    ],
)