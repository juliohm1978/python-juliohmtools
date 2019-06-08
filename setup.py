import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="juliohmtools",
    version="0.0.4",
    author="Julio H Morimoto",
    author_email="jhm@juliohm.com.br",
    description="A Collection of Python Libraries",
    long_description='''
    For details and documentation, refer to https://github.com/juliohm1978/pyjuliohmtools
    ''',
    long_description_content_type="text/markdown",
    url="https://github.com/juliohm1978/pyjuliohmtools",
    packages=setuptools.find_packages(),
    install_requires=[
          'kubernetes',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)