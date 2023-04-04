nextflow.enable.dsl=2

inputPath = params.xlsx_path
kgScriptPath = params.kg_script
outputDir = params.output_dir
outputName = params.output_name


process runKGProcess {
  input:
  path inputPath
  path scriptFile

  output:
  path 'FoodSafetyMonitoringKG.json'

  debug true  
  script:
    """
      echo 'script executing...'
      echo \$(pwd)
      python3 $scriptFile $inputPath 'FoodSafetyMonitoringKG.json'
    """
}

process copyFile {
  label 'cleanup_enabled'
  publishDir "${outputDir}", mode: 'move'
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
  data = channel.fromPath(inputPath)
  scriptFile = channel.fromPath(kgScriptPath)
  kgResultfile = runKGProcess(data, scriptFile) 
  copyFile(kgResultfile, outputName)
}