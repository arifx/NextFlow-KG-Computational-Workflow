git pull

nextflow run ./processes/ProcessKG.nf --input_path ./processes/ENOSE.xlsx --file_name KG.json --project_dir ./processes/ --output_path ./processes 
#nextflow run ./processes/ProcessKG.nf --input_path ./processes/ENOSE.xlsx --file_name KG.json --project_dir ./processes/ --output_path ./processes  -with-docker snheffer/nextflow:kg-latest

cat processes/KG.json
