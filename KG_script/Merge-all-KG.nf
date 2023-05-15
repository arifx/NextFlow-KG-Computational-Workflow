nextflow.enable.dsl=2
baseDir = file('.')
runKG_output_folder = "${baseDir}/${params.runKG_output_folder}"
merge_output_path = "${baseDir}/${params.merge_output_path}"
script_dir = "${baseDir}/${params.script_dir}"
copy_output_path = "${baseDir}/${params.copy_output_path}"


process mergeKG {
  label 'cleanup_enabled'
  input: 
  val merge_script_file
  
  output:
  val "${merge_output_path}"
  
  script:
  """
    input_files=""
    find "$runKG_output_folder" -type f | while read -r file; do
      if [[ "\$file" == *"full"* ]]; then  
        input_files+=" \"\$file\" "
      fi
    done
    python3 $merge_script_file --input \$input_files--output "${merge_output_path}"
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
  merge_script_file = "$script_dir/Merge-KG.py"
  mergeResult = mergeKG(merge_script_file)
  copyFile(mergeResult, copy_output_path)
}