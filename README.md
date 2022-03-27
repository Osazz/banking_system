# banking_system
Implement an object-oriented banking system using Python 3 that will track accounts, balances and exchange rates and add tests for your solution.

## Component of the project
- src/AceBank.py: This is where the bank class is all the functioned for it to work
- tests/functional_tests: We have our functional Test in this file
- tests/unit_test: Unit testing the functions in AceBank.py
- script.py: These runs and integration simulation of the Bank
- .github/workflows/unit_test.yml: GitHub action that runs our unit test on python versions: 3.7, 3.8 and 3.9
- .github/workflows/functional_test.yml: GitHub action that runs our functional test on python version 3.8
- .github/workflows/build_docker.yml: GitHub action that packages our code into docker image and push to defined docker repo
- .github/workflows/remote_execution.yml: GitHub action that brings down our docker image, create a container from it and  run our script.py

## How to Run Code
```shell
 pip install -r requirements.txt # this install the needed packages for code to run
```
### Script.py
```shell
python script.py
```
### unit test
```shell
pytest <project home directory>/tests/unit_test -s -vvv
```
### Functional test
```shell
pytest <project home directory>/functional/unit_test -s -vvv
```
