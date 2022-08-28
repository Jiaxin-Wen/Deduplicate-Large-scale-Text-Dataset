'''
Cluster based on MinHash (not MinHashLSH)
'''

from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
import time
import json
from disjoint_set import DisjointSet
import random
import os
import argparse


from utils import get_minhash, pairwise_search, pairwise_search_lsh
from arguments import get_args


def main(args):
    # TODO: caching with huggingface-datasets
    data = []
    with open(args.in_file, 'r') as f:
        for i in f:
           data.append(i.strip())
           
    data = data[:5000]
    total_size = len(data)
    
    text_list = [i.split('\t')[-1] for i in data]

    print('text example = ', text_list[0])
    print('total size = ', total_size)

    threshold = args.threshold

    # search based on MinHash
    start = time.time()
    if args.lsh:
        search_res = pairwise_search_lsh(text_list, args)
    else:
        search_res = pairwise_search(text_list, args)
    end = time.time()
    print('find neighbor, time cost = ', end - start)

    # cluster
    start = time.time()
    ds = DisjointSet()
    for i in range(total_size):
        ds.find(i)

    for item in tqdm(search_res):
        id1, id2 = item
        ds.union(id1, id2)
    end = time.time()
    print("cluster time cost = ", end - start)

    cluster_data = []
    for cluster_set in tqdm(ds.itersets()):
        if len(cluster_set) > 1:
            cluster = []
            for i in cluster_set:
                cluster.append(data[i])
            cluster_data.append(cluster)
    
    cluster_data.sort(key=lambda x: len(x), reverse=True)

    with open(f"{args.output_dir}/cluster_threshold{threshold}_lsh{args.lsh}.json", 'w') as f:
        json.dump(cluster_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    random.seed(42)
    args = get_args()
    main(args)
