# Deduplicate Large-scale Text Dataset


## Introduction

Training on repeated data would impair the performance of language models as they tend to be easily memorized and consume a large fraction of model's capacity ([1][2]). 
However, large-scale web-crawled dataset often contain a significant number of duplicate texts.

Therefore, we aim to implement an efficient and easy-to-use system for deduplicating large-scale text dataset based on Python. Here are several highlights of this project:
- [x] support efficient deduplicating based on MinHashLSH, which achieves a sub-linear query cost
- [ ] speedup the load/save of large files based on datasets
- [ ] support multiprocessing

We also support several interesting features including: 
- Cluster: automatically cluster your dataset based on text similarity. Based on the clustering results, you can quickly identify the potential text patterns in your dataset

## Installing

`pip install -r requirements.txt`


## Usage

### 0. Preparation

#### Data Format

txt file, one sentence per line

#### Determine the hyperparameter settings for your own dataset

We provide a toy script `test_minhash.py` for users to conduct case study on your own dataset

`LANG=zh python test_minhash.py`

### 1. Deduplicate

#### Pipeline

You can directly run the whole deduplication pipeline with 

```none
bash scripts/deduplicate_pipeline.sh

main arguments:
- LANG: the language of your dataset which determines the tokenization method, we currently support ['zh', 'en'] 
- DATA_DIR: ${DATA_DIR}/ori.txt is the dataset file to be deduplicated
- K: int, K-shingles, used for calculating similarity
- THRESHOLD: float in range(0,1), lower bound on similarity for determining duplication  
```

#### Step-by-Step

For interested users, the entire deduplication pipeline has the following three steps. 

- step1: deduplicate based on exact match

`bash scripts/dueplicate_exact.sh`

- step2: deduplicate based on MinHashLSH

`bash scripts/deduplicate_minhashlsh.sh`

- step3: recall false positives caused by the approximation of MinHashLSH

`bash scripts/deduplicate_postprocess.sh`

### 2. Cluster


```none
bash scripts/cluster.sh

main arguments:
- LANG: the language of your dataset which determines the tokenization method, we currently support ['zh', 'en'] 
- IN_FILE: dataset path
- K: int, K-shingles, used for calculating similarity
- THRESHOLD: float in range(0,1), lower bound on similarity for determining duplication  
```

### References

- [1] [Scaling Laws and Interpretability of Learning from Repeated Data](https://arxiv.org/pdf/2205.10487.pdf)

- [2] [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/pdf/2107.06499.pdf)
