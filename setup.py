from setuptools import setup

setup(
    name="hashfunc32",
    version="0.0.1",
    description="Find hashes in WinAPI",
    packages=['hashfunc32'],
    package_data={'': [
            'System32.json'
        ]
    },
    include_package_data=True
)