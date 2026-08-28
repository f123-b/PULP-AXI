.PHONY: test fetch-upstream

test:
	python3 -m pytest -q

fetch-upstream:
	bash scripts/fetch_upstream.sh
