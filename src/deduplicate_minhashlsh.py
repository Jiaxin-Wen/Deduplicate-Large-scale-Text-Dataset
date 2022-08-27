'''
MinHashLSH
'''

from datasketch import MinHash, MinHashLSH
import random
from tqdm import tqdm
import time
import json
import os


from utils import get_k_shingles
from arguments import get_args

    
def get_minhash(text, k):
    m = MinHash()
    m.update_batch([j.encode('utf8') for j in get_k_shingles(text, k)])
    return m


def main(args):
    data = []
    with open(args.in_file, 'r') as f:
        for i in f:
           data.append(i.strip())
           
    # FIXME: whether we need to sort example by its length before deduplicating

    print('text example = ', data[0])
    size = len(data)
    print('total size = ', size)

    lsh = MinHashLSH(threshold=args.threshold, num_perm=args.num_perm)

    duplicate_data = []
    save_idx = []

    print('[INFO] start deduplicating')
    for i, text in tqdm(enumerate(data)):
        m = get_minhash(text, k=args.k)
        res = lsh.query(m)
        if len(res) == 0:
            save_idx.append(i)
            lsh.insert(i, m)
        else:
            neighbour_set = [data[idx] for idx in res]
            duplicate_data.append((data[i], neighbour_set))
            # 在这里检查太慢了 先跑完一遍粗筛吧
            # flags = []
            # for idx in res:
            #     tmp = response_list[idx]
            #     if recheck(text, tmp, K, threshold):
            #         duplicate_data.append((text,tmp))
            #         flags.append(False)
            #     else: # 是误判, 不算重复
            #         false_data.append((text,tmp))
            #         flags.append(True)
            
            # if not any(flags): # 没有任何重复
            #     save_idx.append(i)
            #     lsh.insert(i, m)
            

    print('deduplicated size = ', len(save_idx))
    print('duplicate size = ', len(duplicate_data))

    with open(f"{args.output_dir}/deduplicate_minhashlsh.txt", 'w') as f:
        for i in save_idx:
            f.write(data[i])
            f.write('\n')
     
    with open(f"{args.output_dir}/deduplicate_minhashlsh_filtered.json", 'w') as f:
        json.dump(duplicate_data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    random.seed(42)
    args = get_args()
    main(args)