nextflow.enable.dsl=2
input_dir = params.input_dir
query_output_dir = params.query_output_dir

process runQueryProcess {
  label 'cleanup_enabled'
  input:
  val inputDir

  output:
  val "${query_output_dir}"

  script:
    """
    echo 'script executing...'
    echo \$(pwd)
    query.py --input "${inputDir}" --output "${query_output_dir}"
    """
}


process copyFile {
  label 'cleanup_enabled'
  input:
  val queryResultfile
  val fileName

  script:
  """
    cp -r ${queryResultfile}/. ${fileName}/.
  """
}

workflow {
  data = input_folder
  script_file = script_dir
  result = runQueryProcess(data, script_file)
  copyFile(result, copy_output_path)
}