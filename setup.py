from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
if __name__ == "__main__":
    this_directory = Path(__file__).parent
    long_description = ( this_directory /"README.md").read_text()
    setup(
        name="selfcord.py",
        packages=find_packages(include=['selfcord', 'selfcord.api', 'selfcord.utils', 'selfcord.models']),
        version="0.0.6",
        description="A Discord API wrapper designed for selfbots!",
        readme="README.md",
        author="Shell of OMEGA",
        license="MIT",
        install_requires=["aiohttp==3.7.4.post0","aioconsole==0.3.3", "websockets==10.1"],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        test_suite='tests',
        long_description=long_description,
        url="https://github.com/Shell1010/Selfcord",
        long_description_content_type="text/markdown",
    )