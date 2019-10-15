from setuptools import setup, find_packages

requirements = [
    "numpy",
    "scikit-image",
    "tifffile",
    "pynrrd",
    "nibabel",
    "tqdm",
    "natsort",
    "psutil",
    "slurmio",
    "nibabel >= 2.1.0",
]

setup(
    name="brainio",
    version="0.0.1",
    description="Loading and saving of brain imaging data.",
    install_requires=requirements,
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/adamltyson/branio",
    author="Adam Tyson, Charly Rousseau",
    author_email="adam.tyson@ucl.ac.uk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    zip_safe=False,
)

