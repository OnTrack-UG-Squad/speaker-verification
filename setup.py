import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="speaker-verification",
    version="0.1.3",
    author="OnTrack UG Squad",
    author_email="hurleyjos@deakin.edu.au",
    description="A small example package",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/OnTrack-UG-Squad/speaker-verification",
    project_urls={
        "Bug Tracker": "https://github.com/OnTrack-UG-Squad/speaker-verification/issues",
        "Pull Requests": "https://github.com/OnTrack-UG-Squad/speaker-verification/pulls"
    },
    classifiers = [
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires = ">=3.7, <3.9",
    zip_safe = True,
    include_package_data = True,
    install_requires = [
        "audioread ==2.1.9",
        "Keras ==2.3.1",
        "librosa ==0.7.2",
        "numba ==0.48.0",
        "numpy ==1.18.5",
        "python-speech-features ==0.6",
        "tensorflow==2.3.0",
        "pytest",
        "noisereduce~=1.1.0",
        "scipy<1.6.0"
    ]
)