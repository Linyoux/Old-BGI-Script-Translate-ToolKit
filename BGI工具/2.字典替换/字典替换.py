import json
import os
from rapidfuzz import process, fuzz
from tqdm import tqdm

def load_and_sort_dict(file_path):
    """
    Load and sort a dictionary from a JSON file by keys.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return dict(sorted(json.load(file).items()))

def replace_in_files_exact(directory, dictionary, used_dict):
    """
    Traverse all txt files in a directory and replace text using a dictionary with exact matches.
    Record used key-value pairs in a separate dictionary.
    """
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for filename in tqdm(txt_files, desc="Processing files with exact match"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for key, value in dictionary.items():
            if key in content:
                content = content.replace(key, value, 1)
                used_dict[key] = value

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

def replace_in_files_fuzzy(directory, dictionary, used_dict, threshold):
    """
    Traverse all txt files in a directory and replace text using a dictionary with fuzzy matches.
    Record used key-value pairs in a separate dictionary.
    """
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for filename in tqdm(txt_files, desc=f"Processing files with threshold {threshold}"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        new_content = []
        for line in content:
            if line.startswith('<') and '>' in line:
                prefix, text = line.split('>', 1)
                match = process.extractOne(text.strip(), dictionary.keys(), scorer=fuzz.ratio)
                if match and match[1] >= threshold:
                    key = match[0]
                    text = text.replace(key, dictionary[key], 1)
                    used_dict[key] = dictionary[key]
                new_content.append(f"{prefix}>{text}")
            else:
                new_content.append(line)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_content)

def main():
    dict_path = 'game.json'
    input_dir = 'TransZone'

    dictionary = load_and_sort_dict(dict_path)
    used_dict = {}

    # 完全匹配替换
    replace_in_files_exact(input_dir, dictionary, used_dict)

    # 更新未使用的字典项
    remaining_dict = {k: v for k, v in dictionary.items() if k not in used_dict}

    # 按90%准确度匹配替换
    replace_in_files_fuzzy(input_dir, remaining_dict, used_dict, threshold=90)

    # 更新未使用的字典项
    remaining_dict = {k: v for k, v in remaining_dict.items() if k not in used_dict}

    # 按80%准确度匹配替换
    replace_in_files_fuzzy(input_dir, remaining_dict, used_dict, threshold=80)

    # 更新未使用的字典项
    without_use_data = {k: v for k, v in remaining_dict.items() if k not in used_dict}
    with open('without_use.json', 'w', encoding='utf-8') as file:
        json.dump(without_use_data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
