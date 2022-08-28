SHELL_SCRIPT_DIR="$( dirname "$0"  )"
WORKING_DIR=$SHELL_SCRIPT_DIR/../..

IN_FILE=${WORKING_DIR}/data/test/ori.txt
OUTPUT_DIR=${WORKING_DIR}/data/test/

python deduplicate_exact.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR