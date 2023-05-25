curl -s https://get.nextflow.io | bash
sudo mv nextflow /usr/local/bin/
nextflow -version
pip install rdflib
mkdir result/
mkdir result/KG

mkdir result/KG/MSI

mkdir result/copy
nextflow run ./KG_script/MSI-process-KG.nf \
--input_folder dataset/ \
--runKG_output_folder result/KG/MSI/ \
--main_kg reasoner/ditect-fso-satisfiable.owl \
--merge_output_path result/full_msi_kg.owl \
--script_dir KG_script \
--copy_output_path result/copy


