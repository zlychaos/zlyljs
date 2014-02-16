all: run
run: rocchio.py keyword_order.py search.py
	python search.py
