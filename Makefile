help:
	@echo ""
	@echo "Help"
	@echo "Commands:"
	@echo "- test"
	@echo "- init"
	@echo "- coverage"
	@echo "- package"
	@echo ""



test:
	py.test testing

init:
	pip install -r requirements.txt

coverage:
	py.test --cov fitsiochunked.py --cov-report html testing

package:
	@-rm dist/* 2>/dev/null
	python setup.py sdist bdist_wheel
	for file in dist/*; do gpg --detach-sign -a $$file; done
