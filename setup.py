from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="modpack_changelogger",
    version="0.4.0-dev",
    packages=find_packages(),
    description="A powerful and customizable Python tool to generate a changelog between two Minecraft modpacks in modrinth.mrpack or curseforge.zip format.",
    author="TheBossMagnus",
    author_email="thebossmagnus@proton.me",
    url="https://github.com/TheBossMagnus/ModpackChangelogger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "aiohttp>=3.9.5",
    ],
    entry_points={
        "console_scripts": [
            "modpack-changelogger=modpack_changelogger:cli_wrapper.wrapper",
        ],
    },
)
