pip install -r requirements.txt
mkdir ${1}/result/
mkdir ${1}/result/KG
mkdir ${2}/result/query
 
nextflow run ./workflows/query.nf \
--input_path ${1} \
--query_output_dir ${2}/result/query \
