from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="secure-ciphertext",
    version="0.1.0",
    author="Secure Ciphertext Contributors",
    author_email="your.email@example.com",
    description="A flexible text encryption and decryption library with custom character mapping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/secure-ciphertext",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        # 列出项目依赖
    ],
    test_suite="tests",
)
