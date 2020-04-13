all: SHELL:=/bin/bash
all: dependencies

dependencies: SHELL:=/bin/bash
dependencies:
	@(                                                                          \
                                                                                \
		## Install all requirements                                             \
		pip3 install -r requirements.txt;                                       \
	)

clean:
	@find . -name "*.pyc" -type f
	@find . -name "*.py~" -type f
	@find . -name "*.pyc" -type f -delete
	@find . -name "*.py~" -type f -delete
