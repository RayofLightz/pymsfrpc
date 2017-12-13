from setuptools import setup

setup(
        name="pymsfrpc",
        version="1",
        packages=["pymsfrpc"],
        install_requires=[
            'msgpack-python'
        ],
        author="Tristan Messner",
        description="A python implementation of the metasploit rpc api",
        license="GNU",
        keywords="metasploit, msfrpc",
        python_requires=">=3"
    )
