nextflow.enable.dsl=2

input_path = params.input_path
//publishTo = params.publish_to
output_directory = params.output_path
file_name = params.file_name


process runKGProcess {
  label 'cleanup_enabled'
  input:
  path inputPath
  path scriptFile

  output:
  path 'FoodSafetyMonitoringKG.json'

  // output:
  // path output_directory

  debug true  
  script:
    """
      echo 'script executing...'
      pwd
      python3 $scriptFile $inputPath test.xlsx
    """
}

process copyFile {
  label 'cleanup_enabled'
  publishDir "${output_directory}", mode: 'move'
  input: 
  path 'tmp/FoodSafetyMonitoringKG.json'
  val fileName

  output:
  path "${fileName}"
  
  script:
  """
    cp tmp/FoodSafetyMonitoringKG.json ${fileName}
  """
}


workflow {
  data = channel.fromPath(input_path)
  script_file = channel.fromPath("${projectDir}/python/KG-process.py")
  kgResultfile = runKGProcess(data, script_file) 
  copyFile(kgResultfile, file_name)
}