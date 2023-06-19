pip install -r requirements.txt
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
mkdir ${1}/result/
mkdir ${1}/result/KG
mkdir ${2}/result/query
pwd

$parent_path/shell/local_scripts/query.py \
--input ${1} \
--output ${2}/result/query \


