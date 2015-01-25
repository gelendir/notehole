from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f]

setup(
        name='notehole',
        version = '0.1',
        description='Fold space and time with music',
        author='Gregory Eric Sanderson',
        author_email='gregory.eric.sanderson@gmail.com',
        packages = find_packages(),
        install_requires=requirements
)
