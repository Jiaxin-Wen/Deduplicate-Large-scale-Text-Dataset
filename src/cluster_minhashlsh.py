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


from utils import get_minhash, pairwise_search
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

    # build MinHash
    # TODO: parallel一下吧
    hash_list = []
    for text in tqdm(text_list):
        hash_list.append(get_minhash(text, args.k))

    threshold = args.threshold

    # calculate similarity based on MinHash
    start = time.time()
    similarity = pairwise_search(hash_list, threshold=threshold)
    end = time.time()
    print('calculate similarity time cost = ', end - start)


    # cluster
    start = time.time()
    ds = DisjointSet()
    for i in range(total_size):
        ds.find(i)

    score_res = []
    for item in tqdm(similarity):
        id1, id2, score = item
        text1 = data[id1].split('\t')[-1]
        text2 = data[id2].split('\t')[-1]
        score_res.append([text1 + "|||" + text2, score])
        ds.union(id1, id2)
    end = time.time()
    print("cluster time cost = ", end - start)


    cluster_data = []
    for similar_set in tqdm(ds.itersets()):
        if len(similar_set) > 1:
            cluster = []
            for i in similar_set:
                cluster.append(data[i])
            cluster_data.append(cluster)

    with open(f"{args.output_dir}/cluster_{threshold}.json", 'w') as f:
        json.dump(cluster_data, f, indent=2, ensure_ascii=False)

    with open(f'{args.output_dir}/score_{threshold}.json', 'w') as f:
        json.dump(score_res, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    random.seed(42)
    args = get_args()
    main(args)
