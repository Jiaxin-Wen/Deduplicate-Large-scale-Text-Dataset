SHELL_SCRIPT_DIR="$( dirname "$0"  )"
WORKING_DIR=$SHELL_SCRIPT_DIR/../..

DATA_DIR=${WORKING_DIR}/data/pipeline
LANG=zh

echo "language: ${LANG}"


echo "=================================step1: deduplicate based on exact match==============================="
IN_FILE=${DATA_DIR}/ori.txt 
OUTPUT_DIR=${DATA_DIR}
python deduplicate_exact.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR


echo "=================================step2: deduplicate based on MinHashlSH================================="
IN_FILE=${DATA_DIR}/deduplicate_exact.txt
OUTPUT_DIR=${DATA_DIR}
K=2
THRESHOLD=0.5
NUM_PERM=128
python deduplicate_minhashlsh.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD \
    --num_perm $NUM_PERM


echo "=================================step3: postprocessing to recall false positives================================="
IN_FILE=${DATA_DIR}/deduplicate_minhashlsh_filtered.json
OUTPUT_DIR=${DATA_DIR}
K=2
THRESHOLD=0.5
SHORT_LENGTH_BOUND=8

python deduplicate_postprocess.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD \
    --short_length_bound $SHORT_LENGTH_BOUND