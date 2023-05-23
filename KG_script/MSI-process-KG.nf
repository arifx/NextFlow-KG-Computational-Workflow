nextflow.enable.dsl=2
baseDir = file('.')
input_folder = "${baseDir}/${params.input_folder}"
runKG_output_folder = "${baseDir}/${params.runKG_output_folder}"
main_kg = "${baseDir}/${params.main_kg}"
merge_output_path = "${baseDir}/${params.merge_output_path}"
script_dir = "${baseDir}/${params.script_dir}"
copy_output_path = "${baseDir}/${params.copy_output_path}"

process runKGProcess {
  label 'cleanup_enabled'
  input:
  val input_folder
  val scriptFile

  output:
  val "${runKG_output_folder}"

  script:
    """
      echo 'script executing...'
      echo \$(pwd)
      find "$input_folder" -type f | while read -r file; do
        if [[ "\$file" == *"MSI"* ]]&&[[ "\$file" != *"MSIF"* ]]; then
          python3 $scriptFile --input "\$file" --output "${runKG_output_folder}"
        fi
      done
    """
}

process mergeKG {
  label 'cleanup_enabled'
  input:
  val runKG_output_folder 
  val merge_script_file
  val main_kg
  
  output:
  val "${merge_output_path}"
  
  script:
  """
    input_files=""
    while IFS= read -r -d '' file; do
      if [[ "\$file" == *"MSI"* ]]&&[[ "\$file" != *"MSIF"* ]]; then
        # Add file to the input_files variable
        input_files+="\"\$file\" "
      fi
    done < <(find $runKG_output_folder -type f -print0)
    python3 $merge_script_file --input \$input_files "$main_kg" --output "${merge_output_path}"
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
  data = input_folder
  script_file = "$script_dir/MSI-process-KG.py"
  merge_script_file = "$script_dir/Merge-KG.py"
  kg = runKGProcess(data, script_file) 
  mergeResult = mergeKG(kg, merge_script_file, main_kg)
  copyFile(mergeResult, copy_output_path)
}