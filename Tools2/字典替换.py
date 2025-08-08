# coding: utf-8
import json
import os
import argparse
from rapidfuzz import process, fuzz
from tqdm import tqdm
import re

def load_dictionary(file_path):
    """
    从JSON文件加载字典。
    :param file_path: JSON文件的路径。
    :return: 字典。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[错误] 字典文件未找到: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"[错误] 字典文件格式不正确: {file_path}")
        return None

def detect_file_format(file_path, check_lines=10):
    """
    检测文件格式是BGI还是普通文本。
    通过检查文件前几行是否包含BGI特有的 "<...>" 标签来判断。
    
    :param file_path: 文件路径。
    :param check_lines: 检查的行数。
    :return: 'bgi' 或 'plain'。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [file.readline() for _ in range(check_lines)]
            bgi_pattern = re.compile(r'^<(\d+),(\d+),(\d+)>')
            bgi_line_count = sum(1 for line in lines if line and bgi_pattern.match(line))
            
            # 如果超过20%的行符合BGI格式，则认为是BGI文件
            if lines and bgi_line_count / len(lines) > 0.2:
                return 'bgi'
            return 'plain'
    except Exception:
        return 'plain'

def replace_text(text, dictionary, mode='exact', threshold=90):
    """
    根据指定模式替换文本。
    
    :param text: 要处理的原始文本。
    :param dictionary: 替换用的字典。
    :param mode: 'exact' (精确匹配) 或 'fuzzy' (模糊匹配)。
    :param threshold: 模糊匹配的相似度阈值。
    :return: (替换后的文本, 使用过的字典键列表)。
    """
    used_keys = []
    
    if mode == 'exact':
        # 为了避免长词替换掉短词的问题（例如 "公主" vs "公主的"），按键的长度降序排序
        sorted_keys = sorted(dictionary.keys(), key=len, reverse=True)
        for key in sorted_keys:
            if key in text:
                text = text.replace(key, dictionary[key])
                used_keys.append(key)
        return text, used_keys
        
    elif mode == 'fuzzy':
        # 模糊匹配通常用于修正整个句子或短语
        if not text.strip() or not dictionary:
            return text, []
            
        match = process.extractOne(text.strip(), dictionary.keys(), scorer=fuzz.ratio)
        if match and match[1] >= threshold:
            key = match[0]
            # 替换时保留原文的前后空格
            text = text.replace(text.strip(), dictionary[key])
            used_keys.append(key)
        return text, used_keys
        
    return text, []

def process_file(file_path, dictionary, mode, threshold, file_format):
    """
    处理单个文件，进行文本替换。
    
    :param file_path: 要处理的文件路径。
    :param dictionary: 替换用的字典。
    :param mode: 'exact' 或 'fuzzy'。
    :param threshold: 模糊匹配阈值。
    :param file_format: 'bgi' 或 'plain'。
    :return: 使用过的字典键的集合。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    keys_used_in_file = set()

    for line in lines:
        processed_line = line
        if file_format == 'bgi':
            bgi_pattern = re.compile(r'^(<(\d+),(\d+),(\d+)>)(.*)')
            match = bgi_pattern.match(line)
            if match:
                tag, text_content = match.group(1), match.group(5)
                # 对BGI行的文本内容进行替换
                new_text, used_keys = replace_text(text_content, dictionary, mode, threshold)
                if used_keys:
                    processed_line = tag + new_text
                    keys_used_in_file.update(used_keys)
        else: # plain format
            # 对普通文本行进行替换
            new_text, used_keys = replace_text(line, dictionary, mode, threshold)
            if used_keys:
                processed_line = new_text
                keys_used_in_file.update(used_keys)
        
        new_lines.append(processed_line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    
    return keys_used_in_file

def main():
    parser = argparse.ArgumentParser(description="使用字典替换TXT文件中的文本，智能识别BGI格式。")
    parser.add_argument("input_dir", help="包含待处理TXT文件的目录。")
    parser.add_argument("--dict", default="game.json", help="用于翻译的JSON字典文件路径。")
    args = parser.parse_args()

    input_dir = args.input_dir
    dict_path = args.dict

    if not os.path.isdir(input_dir):
        print(f"[错误] 目录不存在: {input_dir}")
        return

    full_dictionary = load_dictionary(dict_path)
    if full_dictionary is None:
        return
        
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    if not txt_files:
        print(f"在目录 '{input_dir}' 中没有找到.txt文件。")
        return

    # 检测所有文件的格式
    file_formats = {f: detect_file_format(os.path.join(input_dir, f)) for f in txt_files}
    
    used_keys_total = set()
    
    # --- 阶段 1: 精确匹配 ---
    print("--- 阶段 1: 正在进行精确匹配替换 ---")
    remaining_dict = full_dictionary
    for filename in tqdm(txt_files, desc="精确匹配"):
        file_path = os.path.join(input_dir, filename)
        used_in_file = process_file(file_path, remaining_dict, 'exact', 100, file_formats[filename])
        used_keys_total.update(used_in_file)

    # --- 阶段 2 & 3: 模糊匹配 ---
    fuzzy_thresholds = [90, 80]
    for threshold in fuzzy_thresholds:
        # 更新剩余字典
        remaining_dict = {k: v for k, v in full_dictionary.items() if k not in used_keys_total}
        if not remaining_dict:
            print(f"所有字典条目均已使用，跳过 {threshold}% 模糊匹配。")
            break
            
        print(f"\n--- 阶段 {2 + (90-threshold)//10}: 正在进行 {threshold}% 相似度模糊匹配 ---")
        for filename in tqdm(txt_files, desc=f"模糊匹配 (阈值{threshold}%)"):
            file_path = os.path.join(input_dir, filename)
            used_in_file = process_file(file_path, remaining_dict, 'fuzzy', threshold, file_formats[filename])
            used_keys_total.update(used_in_file)

    # --- 结束: 保存未使用条目 ---
    final_remaining_dict = {k: v for k, v in full_dictionary.items() if k not in used_keys_total}
    output_path = 'without_use.json'
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(final_remaining_dict, file, indent=4, ensure_ascii=False)
        
    print(f"\n处理完成！\n总共使用了 {len(used_keys_total)} 个字典条目。")
    print(f"剩余 {len(final_remaining_dict)} 个未使用的条目已保存到 {output_path}。")


if __name__ == '__main__':
    main()