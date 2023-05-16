curl -s https://get.nextflow.io | bash
mv nextflow /usr/local/bin/
nextflow -version
pip install rdflib
mkdir result/
mkdir result/KG
mkdir result/KG/FTIR
mkdir result/KG/MSI
mkdir result/KG/MSIF
mkdir result/KG/freshdetect
mkdir result/KG/enose
mkdir result/copy
nextflow run ./KG_script/MSI-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/MSI/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_msi_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy
nextflow run ./KG_script/MSIF-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/MSIF/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_msif_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy
nextflow run ./KG_script/FTIR-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/FTIR/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_ftir_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy
nextflow run ./KG_script/freshdetect-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/freshdetect/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_freshdetect_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy
nextflow run ./KG_script/enose-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/enose/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_enose_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy
nextflow run ./KG_script/Merge-all-KG.nf \
--runKG_output_folder result/ \
--merge_output_path result/full_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy

