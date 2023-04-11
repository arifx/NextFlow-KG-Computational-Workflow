nextflow.enable.dsl=2

input_path = params.input_path
//publishTo = params.publish_to
projectDir = params.project_dir
output_directory = params.output_path
file_name = params.file_name
kg_name = params.kg_name



process runKGProcess {
  containerOptions "--user root -v /home/appuser/NextFlow-KG-Computational-Workflow/processes:/processes"
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
      echo 'NF script executing...'
      echo \$(pwd)
      python3 /home/appuser/NextFlow-KG-Computational-Workflow/processes/ProcessENOSE2KG.py $inputPath 'FoodSafetyMonitoringKG.json'
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

  script_file = channel.fromPath("${projectDir}ProcessENOSE2KG.py")
    //script_file = channel.fromPath("${projectDir}KG-process.py")
  kgResultfile = runKGProcess(data, script_file) 
  copyFile(kgResultfile, file_name)
}