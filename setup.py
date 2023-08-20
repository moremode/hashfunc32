from setuptools import setup

setup(
    name="hashfunc32",
    version="0.0.2",
    description="Find hashes in WinAPI",
    packages=['hashfunc32'],
    install_requires=['click'],
    entry_points = {
        'console_scripts': ['winhash=hashfunc32.commands:winhash'],
    },
    package_data={'': [
            'System32.json'
        ]
    },
    include_package_data=True
)