.PHONY: activate despesa

download:
	@ckanapi dump datasets --remote https://dados.mg.gov.br/ --datapackages=datasets despesa

run:
	@python main.py

all: download run 
	