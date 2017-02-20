RUNTEST=python -m unittest discover -p "*_test.py"

test: .PHONY
	$(RUNTEST) lib

clean:
	rm -rf *.pyc .DS_Store

tidy:
	find . -name *.py -exec pythontidy {} {} \;

lint:
	pylint lib/*.py bin/*.py

.PHONY:
