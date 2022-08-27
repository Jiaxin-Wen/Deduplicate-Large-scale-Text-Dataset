'''
deduplicate based on MinHashLSH
'''

from datasketch import MinHash, MinHashLSH
from tqdm import tqdm
import time
import json
import random
import os

from utils import get_minhash
from arguments import get_args



def inner_check_duplicate(item, args):
    '''
    double-check similarity with neighbors based on MinHash
    '''
    query, candidates = item

    length_bound = args.short_length_bound # use K=1 to calculate minhash for short texts
    
    query_short_hash = get_minhash(query, k=1)
    query_hash = get_minhash(query, args.k)
        
    for i in candidates:
        if len(i) < length_bound and len(query) <= length_bound:
            tmp = get_minhash(i, k=1)
            score = query_short_hash.jaccard(tmp)
        else:
            tmp = get_minhash(i, args.k)
            score = query_hash.jaccard(tmp)
            
        if score >= args.threshold:
            return True
    return False


def postprocess(args):
    '''
    recall false positive after deduplicating with MinHashLSH
    '''

    with open(args.in_file, 'r') as f:
        data = json.load(f)

    print('total size = ', len(data))
    print('exmaple = ', data[0])
    
    false_positives = []
    duplicate = []
    for i, item in tqdm(enumerate(data)):
        if not inner_check_duplicate(item, args): # find false positive
            false_positives.append(item)
        else:
            duplicate.append(item)
    print('number of recalled false positives: ', len(false_positives))
    print('example of false positive: ', false_positives[0])

    with open(f"{args.output_dir}/deduplicate_minhashlsh_falsepositives.json", 'w') as f:
        json.dump(false_positives, f, indent=2, ensure_ascii=False)
    with open(f"{args.output_dir}/duplicate_final.json", 'w') as f:
        json.dump(duplicate, f, indent=2, ensure_ascii=False)
        

def merge(args):
    with open(f"{args.output_dir}/deduplicate_minhashlsh.txt", 'r') as f:
        data = [i.strip() for i in f.readlines()]

    with open(f"{args.output_dir}/deduplicate_minhashlsh_falsepositives.json", 'r') as f:
        false_positive = [i[0] for i in json.load(f)]

    merge = data + false_positive
    print(f'ori size = {len(data)}, number of false positives = {len(false_positive)}, new size = {len(merge)}')
    with open(f"{args.output_dir}/deduplicate_final.txt", 'w') as f: 
        for i in merge:
            f.write(i)
            f.write('\n')


def main(args):
    # recall false negatives
    postprocess(args)
    
    # merge the recalled data
    merge(args)


if __name__ == "__main__":
    random.seed(42)
    args = get_args()
    main(args)