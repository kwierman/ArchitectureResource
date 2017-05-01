
define remove
  @if [[ $(ls $(1)) ]]; then rm $(1) ; fi
  $(call remove,*/$(1))
endef

clean:
	@echo "Cleaning..."
	$(call remove,*.pyc)
	$(call remove,*~)
	$(call remove,*\#)

install: clean
	python setup.py install

all: install
	@echo "Done!"
