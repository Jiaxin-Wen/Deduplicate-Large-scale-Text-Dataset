SHELL_SCRIPT_DIR="$( dirname "$0"  )"
WORKING_DIR=$SHELL_SCRIPT_DIR/../..

IN_FILE=${WORKING_DIR}/data/test/deduplicate_minhashlsh_filtered.json
OUTPUT_DIR=${WORKING_DIR}/data/test/

K=2
THRESHOLD=0.5
SHORT_LENGTH_BOUND=8

python deduplicate_postprocess.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD \
    --short_length_bound $SHORT_LENGTH_BOUND