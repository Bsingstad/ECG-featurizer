import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ECG-featurizer", # Replace with your own username
    version="0.0.3",
    author="Bjørn-Jostein Singstad",
    author_email="bjorn_sing@hotmail.com",
    description="This Python package recognize patterns in an ECG and derives features",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ECG-featurizer/ECG-featurizer",
    install_requires = [
        'neurokit2 >= 0.0.41',
        'numpy >= 1.19.0',
        'wfdb >= 3.1.1'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)