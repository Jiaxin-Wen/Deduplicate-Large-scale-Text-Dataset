'''
deduplicate based on exact match
'''
from tqdm import tqdm
import os
from arguments import get_args


def main(args):
    text_set = set()

    cnt = 0
    duplicate = []
    with open(args.in_file, 'r') as f:
        for i in tqdm(f):
            text = i.strip()
            cnt += 1
            text_set.add(text)

    print("ori size = ", cnt)
    print('exact filtered size = ', len(text_set))

    with open(f"{args.output_dir}/deduplicate_exact.txt", 'w') as f:
        for i in text_set:
            f.write(i)
            f.write('\n')

if __name__ == "__main__":
    args = get_args()
    main(args)