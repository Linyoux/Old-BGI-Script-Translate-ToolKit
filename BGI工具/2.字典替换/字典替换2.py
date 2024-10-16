import json
import os
from rapidfuzz import process, fuzz
#需要安装rapidfuzz库

def load_and_sort_dict(file_path):
    """
    从给定的JSON文件中加载字典，并按键排序。
    :param file_path: JSON文件的路径。
    :return: 排序后的字典。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        # 加载JSON数据并将其转换为字典
        dict_data = json.load(file)
        # 按字典的键进行排序
        sorted_dict = dict(sorted(dict_data.items()))
    return sorted_dict

def replace_in_files(directory, dictionary, used_dict):
    """
    遍历指定目录中的所有txt文件，并使用提供的字典替换其中的文本。
    同时记录已经使用过的键值对，并将其写入新的JSON文件。
    :param directory: 要遍历的目录。
    :param dictionary: 包含替换规则的字典。
    :param used_dict: 记录已经使用过的键值对的字典。
    """
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # 构建完整的文件路径
            file_path = os.path.join(directory, filename)
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 使用字典替换文件中的文本
            for key, value in list(dictionary.items()):
                # 处理每行的内容，忽略行首的三位数字戳
                lines = content.splitlines()
                new_lines = []
                for line in lines:
                    if line.startswith('<') and '>' in line:
                        prefix, text = line.split('>', 1)
                        # 模糊匹配忽略前缀
                        match = process.extractOne(text, [key], scorer=fuzz.ratio)
                        if match and match[1] > 80:  # 设置匹配阈值为80
                            text = text.replace(key, value, 1)  # 替换一次
                            used_dict[key] = value  # 记录使用过的键值对
                        new_lines.append(f"{prefix}>{text}")
                    else:
                        new_lines.append(line)
                content = '\n'.join(new_lines)
            
            # 将修改后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

def main():
    # ！！！字典文件路径 ！！！
    dict_path = 'without_use.json'
    #  ！！输入文件夹路径！！
    input_dir = 'TransZone'

    # 加载并排序字典
    dictionary = load_and_sort_dict(dict_path)
    
    # 初始化记录使用过的键值对的字典
    used_dict = {}
    
    # 对TransZone文件夹内所有txt文件进行替换
    replace_in_files(input_dir, dictionary, used_dict)
    
    # 将未使用的键值对写入新的JSON文件
    without_use_data = {k: v for k, v in dictionary.items() if k not in used_dict}
    with open('without_use2.json', 'w', encoding='utf-8') as file:
        json.dump(without_use_data, file, indent=4, ensure_ascii=False)  # 设置ensure_ascii=False以正确处理中文字符

if __name__ == '__main__':
    main()
