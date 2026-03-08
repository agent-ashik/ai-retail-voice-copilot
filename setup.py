"""
Setup configuration for AI Retail Voice Copilot.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voice-copilot",
    version="1.0.0",
    author="VaniCommerce Team",
    author_email="team@vanicommerce.ai",
    description="AI Retail Voice Operations Copilot - Multilingual voice-enabled inventory assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agent-ashik/ai-retail-voice-copilot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "sqlalchemy>=2.0.25",
        "boto3>=1.34.34",
        "prophet>=1.1.5",
        "redis>=5.0.1",
        "pyjwt>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "pytest-cov>=4.1.0",
            "hypothesis>=6.98.3",
            "black>=24.1.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
)
