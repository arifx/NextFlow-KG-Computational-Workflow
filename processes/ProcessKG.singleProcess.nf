nextflow.enable.dsl=2

inputPath = params.xlsx_path
kgScriptPath = params.kg_script
outputDir = params.output_dir
outputName = params.output_name


process runKGProcess {
   containerOptions "--user root -v /home/appuser/NextFlow-KG-Computational-Workflow/processes:/processes"
 
  // label 'cleanup_enabled'
  publishDir "${outputDir}", mode: 'move'

  input:
  path scriptFile
  path inputPath
  val fileName

  output:
  path "${fileName}"

  debug true  
  script:
    """
      echo 'script executing...'
      echo \$(pwd)
      python3 -W ignore $scriptFile $inputPath ${fileName}

    """
}

workflow {
  data = channel.fromPath(inputPath)
  scriptFile = channel.fromPath(kgScriptPath)
  runKGProcess(scriptFile, data, outputName) 
}