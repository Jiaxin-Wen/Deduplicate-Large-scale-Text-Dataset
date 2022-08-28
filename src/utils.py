from tqdm import tqdm
from datasketch import MinHash, MinHashLSH
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


def search(text_list, args):
    '''
    search similar text
    '''
    # TODO: support parallel
    # build MinHash
    data = []
    for text in tqdm(text_list):
        data.append(get_minhash(text, args.k))

    size = len(data)
    res = []
    for i in tqdm(range(size)):
        for j in range(i+1, size):
            score = data[i].jaccard(data[j])
            if score >= args.threshold:
                res.append((i,j))
    return res


def search_lsh(data, args):
    '''
    search similar text with lsh
    '''
    res = []
    
    lsh = MinHashLSH(threshold=args.threshold, num_perm=args.num_perm)
    
    for i, text in tqdm(enumerate(data)):
        m = get_minhash(text, k=args.k)
        neighbor_ids = lsh.query(m)
        lsh.insert(i, m)
        if any(neighbor_ids):
            for j in neighbor_ids:
                res.append((i, j))

    return res