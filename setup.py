import setuptools

setuptools.setup(
    name="Banking system",
    version="0.0.1",
    author="Ayodeji Osagie",
    author_email="osagieayodeji@gmail.com",
    description="Implement an object-oriented banking system.",
    long_description="Implement an object-oriented banking system using "
                     "Python 3 that will track accounts, balances and "
                     "exchange rates and add tests for your solution.",
    long_description_content_type="text/markdown",
    url="https://github.com/Osazz/banking_system.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
)
