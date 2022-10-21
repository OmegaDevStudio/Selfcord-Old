from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="Selfcord",
        packages=find_packages(include=['selfcord', 'selfcord.api', 'selfcord.utils', 'selfcord.models']),
        version="0.0.2",
        description="A Discord API wrapper designed for selfbots!",
        author="Shell of OMEGA",
        license="MIT",
        install_requires=["aiohttp==3.7.4.post0","aioconsole==0.3.3", "websockets==10.1"],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        test_suite='tests',
    )