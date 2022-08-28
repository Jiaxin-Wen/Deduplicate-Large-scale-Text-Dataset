SHELL_SCRIPT_DIR="$( dirname "$0"  )"
WORKING_DIR=$SHELL_SCRIPT_DIR/../..

LANG=zh
IN_FILE=${WORKING_DIR}/data/test/deduplicate_exact.txt
OUTPUT_DIR=${WORKING_DIR}/data/test
K=2
THRESHOLD=0.5

python cluster_minhashlsh.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD