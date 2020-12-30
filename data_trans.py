#! -*- coding:utf-8 -*-


import json
from tqdm import tqdm
import codecs


all_50_schemas = set()


with open('./raw_data/all_50_schemas','r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        all_50_schemas.add(a['predicate'])


id2predicate = {i:j for i,j in enumerate(all_50_schemas)}
predicate2id = {j:i for i,j in id2predicate.items()}


with codecs.open('./datasets/all_50_schemas_me.json', 'w', encoding='utf-8') as f:
    json.dump([id2predicate, predicate2id], f, indent=4, ensure_ascii=False)


chars = {}
min_count = 2


train_data = []


with open('./raw_data/train_data.json','r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        if not a['spo_list']:
            continue
        train_data.append(
            {
                'text': a['text'],
                'spo_list': [(i['subject'], i['predicate'], i['object']) for i in a['spo_list']]
            }
        )
        for c in a['text']:
            chars[c] = chars.get(c, 0) + 1


with codecs.open('./datasets/train_data_me.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=4, ensure_ascii=False)


dev_data = []


with open('./raw_data/dev_data.json','r', encoding='utf-8') as f:
    for l in tqdm(f):
        a = json.loads(l)
        dev_data.append(
            {
                'text': a['text'],
                'spo_list': [(i['subject'], i['predicate'], i['object']) for i in a['spo_list']]
            }
        )
        for c in a['text']:
            chars[c] = chars.get(c, 0) + 1


with codecs.open('./datasets/dev_data_me.json', 'w', encoding='utf-8') as f:
    json.dump(dev_data, f, indent=4, ensure_ascii=False)


total_data = []

for obj in train_data:
    total_data.append(obj)

for obj in dev_data:
    total_data.append(obj)

with codecs.open('./datasets/train_data_vote_me.json', 'w', encoding='utf-8') as f:
    json.dump(total_data, f, indent=4, ensure_ascii=False)


with codecs.open('./datasets/all_chars_me.json', 'w', encoding='utf-8') as f:
    chars = {i:j for i,j in chars.items() if j >= min_count}
    id2char = {i+2:j for i,j in enumerate(chars)} # padding: 0, unk: 1
    char2id = {j:i for i,j in id2char.items()}
    json.dump([id2char, char2id], f, indent=4, ensure_ascii=False)
