nextflow.enable.dsl=2

input_path = params.input_path
//publishTo = params.publish_to
output_directory = params.output_path
file_name = params.file_name
project_dir = params.project_dir

process runKGProcess {
  label 'cleanup_enabled'
  input:
  val inputPath
  val scriptFile

  output:
  val "${output_directory}/msi_kg.owl"

  script:
    """
      echo 'script executing...'
      echo \$(pwd)
      python3 $scriptFile --input "${inputPath}" --output "${output_directory}/msi_kg.owl"
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
  data = input_path
  script_file = "$project_dir/MSI-process-KG.py"
  kgResultfile = runKGProcess(data, script_file) 
  copyFile(kgResultfile, file_name)
}