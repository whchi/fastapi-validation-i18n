.PHONY:install test clean

install:
	uv sync

test:
	uv run pytest

clean:
	find . -name "*.pyc" | xargs rm -rf
	find . -type d -name "*_cache" | xargs rm -rf
