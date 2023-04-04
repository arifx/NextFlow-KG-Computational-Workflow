build_docker:
	docker build ./ --tag snheffer/nextflow-process-kg:$(VERSION)
	