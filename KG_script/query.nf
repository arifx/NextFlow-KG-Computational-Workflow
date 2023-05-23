nextflow.enable.dsl=2
baseDir = file('.')
input_folder = "${baseDir}/${params.input_folder}"
query_output_folder = "${baseDir}/${params.runKG_output_folder}"
script_dir = "${baseDir}/${params.script_dir}"
copy_output_path = "${baseDir}/${params.copy_output_path}"

process runQueryProcess {
  label 'cleanup_enabled'
  input:
  val input_folder
  val scriptFile

  output:
  val "${query_output_folder}"

  script:
    """
    echo 'script executing...'
    echo \$(pwd)
    python3 $scriptFile --input "${input_folder}" --output "${query_output_folder}"
    """
}

process copyFile {
  label 'cleanup_enabled'
  input: 
  val queryResultfile
  val fileName
  
  script:
  """
    cp ${queryResultfile} ${fileName}
  """
}

workflow {
  data = input_folder
  script_file = $script_dir
  result = runQueryProcess(data, script_file) 
  copyFile(result, copy_output_path)
}