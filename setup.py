from setuptools import find_packages, setup
setup(
    name='neat_py_lollo',
    packages=find_packages(include=['neat_py']),
    version='0.0.3',
    description='Python NEAT implementation',
    author='Racca Lorenzo',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)