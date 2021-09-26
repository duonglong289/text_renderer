import json
if __name__=='__main__':
    new_corpus = {}

    with open('example_data/text/box_corpus.json', 'r') as f:
        corpus = json.load(f)
        for first_layer_key in corpus.keys():
            for second_layer_key in corpus[first_layer_key].keys():
                new_corpus[first_layer_key+'_'+second_layer_key] = \
                     corpus[first_layer_key][second_layer_key]
    
    with open('processed_box_corpus.json', 'w', encoding='utf-8') as f:
        json.dump(new_corpus, f, ensure_ascii=False, indent=4)