from pathlib import Path
import json
import os
import tqdm
import multiprocessing as mp

def convert_from_text_renderer_format(folder_path):
    img_list = list(Path(folder_path).glob('**/*.jpg'))
    img_list.sort()
    labels = json.load(open(os.path.join(folder_path, 'labels.json')))
    src = open(f'{folder_path}/src.txt', 'w')
    tgt = open(f'{folder_path}/tgt.txt', 'w')

    for idx, img in tqdm.tqdm(enumerate(img_list), total=len(img_list)):
        img_name = str(img_list[idx]).split('/')[-1].split('.')[0]
        label = labels['labels'][img_name]

        # Check duplicate samples
        if idx < len(img_list)-1:
            next_img_name = str(img_list[idx+1]).split('/')[-1].split('.')[0]
            if label == labels['labels'][next_img_name]:
                continue
        
        if isinstance(label, dict):
            if 'key' in label:
                text = label['key'] + ': ' + label['value']
        else:
            text = label

        onmt_space_text = text.replace(' ', ' \\; ')
        splitted_text = onmt_space_text.split()
        list_list_char = [list(word) if word != '\\;' else [word] for word in splitted_text]
        list_char = sum(list_list_char, [])
        onmt_text = ' '.join(list_char)

        src.write(img_name+'.jpg'+'\n')
        tgt.write(onmt_text+'\n')

    src.close()
    tgt.close()

if __name__=='__main__':
    output = ['output_boxes', 'output_checkmarks', 'output_dots']
    Pool = mp.Pool(processes=mp.cpu_count())
    Pool.map(convert_from_text_renderer_format, output)
    Pool.close()