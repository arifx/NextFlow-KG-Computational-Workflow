build_docker:
	docker build ./ --tag snheffer/nextflow-process-kg:$(VERSION)

run_docker:
	nextflow run $(NEXTFLOW_SCRIPT) --xlsx_path $(XLSX_PATH) --kg_script $(KG_SCRIPT) --output_dir $(OUTPUT_DIR) --output_name $(OUTPUT_FILE) -with-docker $(DOCKER_IMAGE)

run_native:
	run_docker:
	nextflow run $(NEXTFLOW_SCRIPT) --xlsx_path $(XLSX_PATH) --kg_script $(KG_SCRIPT) --output_dir $(OUTPUT_DIR) --output_name $(OUTPUT_FILE)