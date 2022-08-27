

with open("/data/wenjiaxin/dataset/eva/eva_data_60g_subset_10w.txt", 'r') as f:
    data = [i.strip().split('\t')[-1] for i in f]
    
    
with open("/data/wenjiaxin/home/deduplicate-large-scale-text-dataset/data/eva_10w.txt", 'w') as f:
    for i in data:
        f.write(i+'\n')
        f.write(i+'\n')