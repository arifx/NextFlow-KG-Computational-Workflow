mkdir result/query
nextflow run ./KG_script/query.nf \
--input_folder result/full_msi_kg.owl \
--query_output_folder result/query \
--script_dir KG_script/query.py \
--copy_output_path result/copy/query
