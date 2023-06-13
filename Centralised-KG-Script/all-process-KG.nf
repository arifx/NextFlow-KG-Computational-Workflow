nextflow.enable.dsl=2
input_file = params.input_file
runKG_output_dir = params.runKG_output_dir
file_type = params.file_type
main_kg_file = params.main_kg_file

process runMsiKGProcess {
  // label 'cleanup_enabled'
  input:
  path input_file

  output:
  path 'intermediate_KG.owl'

  script:
    """
      echo 'script executing...'
      echo \$(pwd)
      head -n1 $input_file
      touch intermediate_KG.owl
      MSI-process-KG.py --input $input_file --output intermediate_KG.owl

      #header=head -n1 intermediate_KG.owl
      #echo \$header 1>&2
    """
}

process mergeKG {
  // label 'cleanup_enabled'
  publishDir "${runKG_output_dir}", mode: 'copy'
  input:
  path 'intermediate_KG.owl' 
  path main_kg_file
  output:
  path 'MSI_merged_KG.owl'
  
  script:
  """
    head -n1 'intermediate_KG.owl'
    head -n1 $main_kg_file
    Merge-KG.py --input  $main_kg_file 'intermediate_KG.owl' --output ./MSI_merged_KG.owl
  """
}


workflow {
  data = channel.fromPath(input_file)
  main_kg = channel.fromPath(main_kg_file)
  if (file_type == 'msi'){
    intermediate_kg = runMsiKGProcess(data) 
    mergeResult = mergeKG(intermediate_kg, main_kg)
  }
}