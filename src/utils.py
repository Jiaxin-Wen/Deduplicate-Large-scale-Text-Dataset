from tqdm import tqdm
from datasketch import MinHash
import os

LANGUAGE = os.environ.get("LANG", "en")

def get_k_shingles(text, k):
    if LANGUAGE == 'en':
        text = text.split()
    elif LANGUAGE == 'zh':
        pass
    else:
        raise Exception(f"unimplement language: {LANGUAGE}")
    
    res = []
    for i in range(len(text) - k + 1):
        shingle = text[i: i + k]
        shingle = ''.join(shingle)
        res.append(shingle)
    # print('text = ', text)
    # print('shingles = ', res)
    return res


def get_minhash(text, k):
    m = MinHash()
    m.update_batch([j.encode('utf8') for j in get_k_shingles(text, k)])
    return m


def pairwise_search(data, threshold):
    # TODO: support parallel
    size = len(data)

    res = []

    for i in tqdm(range(size)):
        for j in range(i+1, size):
            score = data[i].jaccard(data[j])
            if score >= threshold:
                res.append((i,j,score))
    print('similar size = ', len(res))
    return res