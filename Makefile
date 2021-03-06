#Ref: https://stackabuse.com/how-to-write-a-makefile-automating-python-setup-compilation-and-testing/

# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3
INSTALL_PY = python3 -m pip install
INIT = sudo apt-get install

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help init setup monitor monitor_ransomware_fast monitor_ransomware_slow all

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = all

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To first init the project type 'make init'"
	@echo "To set up the project type 'make setup'"
	@echo "To run real-time monitoring type 'make monitor'"
	@echo "To run real-time monitoring for fast ransomware type 'make monitor_ransomware_fast'"
	@echo "To run real-time monitoring for slow ransomware type 'make monitor_ransomware_slow'"
	@echo "------------------------------------"

all: init setup monitor

monitor_ransomware_fast:
	${PYTHON} realtime_monitoring_ransomware_fast.py

monitor_ransomware_slow:
	${PYTHON} realtime_monitoring_ransomware_slow.py

monitor:
	${PYTHON} realtime_monitoring.py

setup:
	${INSTALL_PY} -r requirements.txt

init:
	${INIT} powertop dstat python3-pip
