# curl -s https://get.nextflow.io | bash
# sudo mv nextflow /usr/local/bin/
nextflow -version

pip install -r requirements.txt
mkdir ${3}/result/
mkdir ${3}/result/KG
mkdir ${3}/result/KG/MSI
mkdir '../nextflow-work'

nextflow run ./workflows/all-process-KG.nf \
-work-dir '../nextflow-work' \
--input_file ${2} \
--runKG_output_dir ${3}/result/KG/MSI/ \
--main_kg_file ${1} \
--file_type msi
