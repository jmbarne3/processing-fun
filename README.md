# Multiprocessing Fun

Quick example of running multiple python processes - specifically simulating longish running IO processes - while reporting back progress to a single `Value` object which is then used to display output on a separate thread.

## Requirements

* python >= 3.8
* Packages listed in the requirements.txt

## Installation

1. Create a venv: `python3 -m venv multiprocessing-fun`
2. Clone in the code: `cd multiprocessing-fun && git clone git@github.com:jmbarne3/processing-fun.git src`
3. Source the venv: `cd src && source ../bin/activate`
4. Install the requirements: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Enjoy!
