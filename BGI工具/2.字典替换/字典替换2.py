import json
import os
from rapidfuzz import process, fuzz
#请先安装rapidfuzz库

def load_and_sort_dict(file_path):
    """
    Load and sort a dictionary from a JSON file by keys.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return dict(sorted(json.load(file).items()))

def replace_in_files(directory, dictionary, used_dict):
    """
    Traverse all txt files in a directory and replace text using a dictionary.
    Record used key-value pairs in a separate dictionary.
    """
    for filename in os.listdir(directory):
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        new_content = []
        for line in content:
            if line.startswith('<') and '>' in line:
                prefix, text = line.split('>', 1)
                match = process.extractOne(text.strip(), dictionary.keys(), scorer=fuzz.ratio)
                if match and match[1] > 80:
                    key = match[0]
                    text = text.replace(key, dictionary[key], 1)
                    used_dict[key] = dictionary[key]
                new_content.append(f"{prefix}>{text}")
            else:
                new_content.append(line)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_content)

def main():
    dict_path = 'without_use.json'
    input_dir = 'TransZone'

    dictionary = load_and_sort_dict(dict_path)
    used_dict = {}

    replace_in_files(input_dir, dictionary, used_dict)

    without_use_data = {k: v for k, v in dictionary.items() if k not in used_dict}
    with open('without_use2.json', 'w', encoding='utf-8') as file:
        json.dump(without_use_data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
