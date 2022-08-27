'''
calculate similarity with MinHash

You can conduct case study on the examples from your datasets, and determine the value of `k` and `threshold`.
'''

from utils import get_minhash


def main(a, b, k):
    hash_a = get_minhash(a, k)
    hash_b = get_minhash(b, k)
    print(f'{a} ||| {b}, score = {hash_a.jaccard(hash_b)}')


if __name__ == '__main__':
    # LANG=zh, chinese
    # a = 'MinHash是一种用于估计数据相似度的数据结构'
    # b = 'MinHash是一种数据结构，可以用来计算数据相似度'
    
    # LANG=en, english
    a = 'MinHash is a probabilistic data structure for estimating the similarity between datasets'
    b = 'MinHash is a data structure, which can estimate the similarity between datasets'
    main(a, b, k=1)