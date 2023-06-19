nextflow.enable.dsl=2
input_path = params.input_path
query_output_dir = params.query_output_dir

process runQueryProcess {
  label 'cleanup_enabled'
  publishDir "${query_output_dir}", mode: 'copy'
  input:
  path inputPath
  output:
  path 'temp/output'

  script:
    """
    echo 'script executing...'
    echo \$(pwd)
    mkdir --parent temp/output
    query.py --input $inputPath --output temp/output
    touch temp/test
    """
}

workflow {
  data = channel.fromPath(input_path)
  runQueryProcess(data)
}