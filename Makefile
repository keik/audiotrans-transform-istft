TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"
SELF="audiotrans_transform_istft"
DEV_DEPS="requirements-dev.txt"

test: init
	@echo $(TAG)$@$(END)
	flake8
	py.test tests/tests.py --cov $(SELF) --verbose

test-all: uninstall-all test
	@echo

init: uninstall-self
	@echo $(TAG)$@$(END)
	pip install --upgrade -r $(DEV_DEPS)
	pip install --upgrade --editable .

uninstall-all: uninstall-self
	@echo $(TAG)$@$(END)
	- pip uninstall --yes -r $(DEV_DEPS) 2>/dev/null

uninstall-self:
	@echo $(TAG)$@$(END)
	- pip uninstall --yes $(SELF) 2>/dev/null
