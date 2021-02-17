from setuptools import setup, find_packages

setup(
    name='auto-background',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/Michedev/daynight-theme-gnome',
    entry_points={
        'console_scripts': [
            'daynight-theme = daynight_theme:main',
            'daynight-theme-config = daynight_theme_config:main'
        ]
    },
    license='MIT',
    author='mikedev',
    author_email='mik3dev@gmail.com',
    description='Set automatic Gnome theme during day and night '
)
