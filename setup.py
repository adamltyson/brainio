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
    "imlib",
    "nibabel >= 2.1.0",
]

setup(
    name="brainio",
    version="0.0.17rc0",
    description="Loading and saving of brain imaging data.",
    install_requires=requirements,
    extras_require={"dev": ["black", "pytest-cov", "pytest", "coverage",]},
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/adamltyson/brainio",
    author="Adam Tyson, Charly Rousseau",
    author_email="adam.tyson@ucl.ac.uk",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    zip_safe=False,
)
