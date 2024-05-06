.PHONY:install test clean

install:
	poetry install

test:
	poetry run pytest

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -type d -name "*_cache" | xargs rm -rf
