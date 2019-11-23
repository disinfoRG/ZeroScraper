.PHONY: lock
lock:
	pipenv sync
	pipenv lock --requirements > requirements.txt
