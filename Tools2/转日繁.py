import json
import os

def load_and_sort_dict(file_path):
    """
    从给定的JSON文件中加载字典，并按键排序。
    :param file_path: JSON文件的路径。
    :return: 排序后的字典。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        dict_data = json.load(file)
    return dict(sorted(dict_data.items()))

def replace_in_files(directory, dictionary):
    """
    遍历指定目录中的所有txt文件，并使用提供的字典替换其中的文本。
    :param directory: 要遍历的目录。
    :param dictionary: 包含替换规则的字典。
    """
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            for key, value in dictionary.items():
                content = content.replace(key, value)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

def main():
    dict_path = 'shift-jis.json'
    input_dir = 'TransZone'
    dictionary = load_and_sort_dict(dict_path)
    replace_in_files(input_dir, dictionary)

if __name__ == '__main__':
    main()
