SHELL_SCRIPT_DIR="$( dirname "$0"  )"
PROJECT_DIR=$SHELL_SCRIPT_DIR/../..

IN_FILE=/data/wenjiaxin/dataset/eva/eva_data_60g_subset_10w.txt
OUTPUT_DIR=${PROJECT_DIR}/results/debug_cluster
K=2
THRESHOLD=0.5

python cluster_minhashlsh.py \
    --in_file $IN_FILE \
    --output_dir $OUTPUT_DIR \
    --k $K \
    --threshold $THRESHOLD