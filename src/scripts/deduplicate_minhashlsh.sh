SHELL_SCRIPT_DIR="$( dirname "$0"  )"
WORKING_DIR=$SHELL_SCRIPT_DIR/../..

IN_FILE=${WORKING_DIR}/data/eva_10w/deduplicate_exact.txt
OUTPUT_DIR=${WORKING_DIR}/data/eva_10w/

K=2
THRESHOLD=0.5
NUM_PERM=128

python deduplicate_minhashlsh.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD \
    --num_perm $NUM_PERM