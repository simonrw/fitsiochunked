help:
	@echo ""
	@echo "Help"
	@echo "Commands:"
	@echo "- test"
	@echo "- init"
	@echo "- coverage"
	@echo ""



test:
	py.test testing

init:
	pip install -r requirements.txt

coverage:
	py.test --cov fitsiochunked.py --cov-report html testing
