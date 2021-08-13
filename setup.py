from setuptools import setup, find_packages
from pathlib import Path

deps = """dataclasses
path==15
python_dateutil==2.8.1
PyYAML==5.3.1
rich
tenacity""".split('\n')
setup(
    name='auto-background',
    version='1.0',
    install_requires=deps,
    packages=find_packages(),
    url='https://github.com/Michedev/daynight-theme-gnome',
    entry_points={
        'console_scripts': [
            'daynight-theme = daynight_theme:main',
            'daynight-theme-config = daynight_theme.daynight_theme_config:main'
        ]
    },
    license='MIT',
    author='mikedev',
    author_email='mik3dev@gmail.com',
    description='Set automatic Gnome theme during day and night '
)
