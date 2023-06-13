nextflow.enable.dsl=2
baseDir = file('.')
runKG_output_folder = "${baseDir}/${params.runKG_output_folder}"
merge_output_path = "${baseDir}/${params.merge_output_path}"
script_dir = "${baseDir}/${params.script_dir}"
copy_output_path = "${baseDir}/${params.copy_output_path}"



process mergeKG {
  label 'cleanup_enabled'
  input:
  val runKG_output_folder 
  val merge_script_file
  
  output:
  val "${merge_output_path}"
  
  script:
  """
    input_files=""
    while IFS= read -r -d '' file; do
      if [[ "\$file" == *"full"* ]]; then
        # Add file to the input_files variable
        input_files+="\"\$file\" "
      fi
    done < <(find $runKG_output_folder -type f -print0)
    python3 $merge_script_file --input \$input_files --output "${merge_output_path}"
  """
}

process copyFile {
  label 'cleanup_enabled'
  input: 
  val kgResultfile
  val fileName
  
  script:
  """
    cp ${kgResultfile} ${fileName}
  """
}


workflow {
  kg = runKG_output_folder
  merge_script_file = "$script_dir/Merge-KG.py"
  mergeResult = mergeKG(kg, merge_script_file)
  copyFile(mergeResult, copy_output_path)
}