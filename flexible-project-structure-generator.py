import os
import json
import yaml
import re
import traceback

def parse_directory_tree(text):
    """
    解析目录树文本格式
    规则：
    1. 没有文件扩展名的路径被视为目录
    2. 有文件扩展名的路径被视为文件
    3. 需要删除路径中的装饰字符（如 ├─）
    """
    print("开始解析目录树文本...")
    
    def is_file(name):
        """判断是否为文件（通过检查是否有扩展名）"""
        return '.' in name and not name.endswith('/')
    
    def clean_name(name):
        """清理路径名称，移除装饰字符和末尾的斜杠"""
        name = name.strip()
        if name.endswith('/'):
            name = name[:-1]
        return name
    
    # 初始化结构
    structure = {}
    
    # 移除空行并分割成行
    lines = [line for line in text.split('\n') if line.strip()]
    
    # 跟踪当前的路径和层级
    path_stack = []
    prev_level = -1
    
    for line in lines:
        # 去除注释
        line = line.split('//')[0].strip()
        if not line:
            continue
        
        # 计算缩进级别
        indent_match = re.match(r'^[│├└─\s]*', line)
        indent = len(indent_match.group(0)) if indent_match else 0
        level = indent // 2  # 每两个缩进字符算一级
        
        # 提取并清理路径名称
        name = line[indent:].strip()
        name = clean_name(name)
        
        # 根据缩进级别调整路径栈
        if level > prev_level:
            # 进入更深层级
            pass
        elif level == prev_level:
            # 同级，弹出最后一个
            if path_stack:
                path_stack.pop()
        else:
            # 返回上级，弹出多个
            while len(path_stack) > level:
                path_stack.pop()
            if path_stack:
                path_stack.pop()
        
        # 更新路径栈
        path_stack.append(name)
        prev_level = level
        
        # 在结构中创建路径
        current = structure
        for i, path_part in enumerate(path_stack[:-1]):  # 除了最后一个部分
            if path_part not in current:
                current[path_part] = {}
            current = current[path_part]
        
        # 处理最后一个部分
        last_part = path_stack[-1]
        if is_file(last_part):
            # 是文件
            current[last_part] = ""
        else:
            # 是目录
            if last_part not in current:
                current[last_part] = {}
    
    print(f"解析结果: {json.dumps(structure, indent=2)}")
    return structure

def tree_to_json(text):
    """
    将目录树文本格式转换为JSON格式
    """
    print("\n=== 开始目录树转换过程 ===")
    print("输入的目录树文本:")
    print(text)
    
    def is_file(name):
        """判断是否为文件（通过检查是否有扩展名）"""
        result = '.' in name and not name.endswith('/')
        print(f"检查是否为文件: {name} -> {result}")
        return result
    
    def clean_name(name):
        """清理路径名称，移除装饰字符和末尾的斜杠"""
        original = name
        name = name.strip()
        if name.endswith('/'):
            name = name[:-1]
        print(f"清理名称: '{original}' -> '{name}'")
        return name
    
    def get_indent_level(line):
        """获取行的缩进级别"""
        # 计算前导符号的数量
        indent = 0
        for char in line:
            if char in '│├└─ \t':
                indent += 1
            else:
                break
        level = indent // 2
        print(f"计算缩进级别: '{line}' -> {level} (缩进字符数: {indent})")
        return level
    
    # 初始化JSON结构
    json_structure = {}
    
    # 移除空行并分割成行
    lines = [line for line in text.split('\n') if line.strip()]
    
    # 存储每个级别的最后一个目录
    level_dirs = {}
    
    for i, line in enumerate(lines, 1):
        print(f"\n处理第 {i} 行: '{line}'")
        
        # 去除注释
        line = line.split('//')[0].strip()
        if not line:
            continue
        
        # 获取原始行的缩进级别
        level = get_indent_level(line)
        
        # 提取名称
        name = re.sub(r'^[│├└─\s]+', '', line).strip()
        name = clean_name(name)
        
        # 确定当前项目的父目录
        current = json_structure
        for l in range(level):
            if l in level_dirs:
                current = current[level_dirs[l]]
        
        if is_file(name):
            # 是文件
            print(f"添加文件 {name} 到级别 {level}")
            current[name] = ""
        else:
            # 是目录
            print(f"添加目录 {name} 到级别 {level}")
            current[name] = {}
            level_dirs[level] = name
        
        print(f"当前JSON结构: {json.dumps(json_structure, indent=2)}")
    
    print("\n=== 转换完成 ===")
    print("最终JSON结构:")
    print(json.dumps(json_structure, indent=2))
    return json_structure

def parse_structure(input_text):
    """
    解析文件结构输入
    支持多种输入格式：目录树文本、JSON、YAML
    返回嵌套字典结构
    """
    print("\n=== 开始解析输入 ===")
    
    # 尝试解析为JSON
    try:
        result = json.loads(input_text)
        print("成功解析为JSON格式")
        return result
    except (json.JSONDecodeError, TypeError):
        print("JSON解析失败，尝试下一种格式")
    
    # 尝试解析为YAML
    try:
        result = yaml.safe_load(input_text)
        if isinstance(result, dict):
            print("成功解析为YAML格式")
            return result
        print("YAML解析结果不是字典")
    except (yaml.YAMLError, TypeError):
        print("YAML解析失败，尝试下一种格式")
    
    # 将目录树文本转换为JSON格式
    print("尝试将目录树文本转换为JSON格式")
    return tree_to_json(input_text)

def create_project_structure(base_path, structure):
    """
    根据给定的文件结构创建文件夹和文件
    
    :param base_path: 项目根目录路径
    :param structure: 描述文件结构的字典
    """
    print(f"开始创建项目结构在: {base_path}")
    print(f"结构类型: {type(structure)}")
    print(f"结构内容: {json.dumps(structure, indent=2)}")
    
    if not isinstance(structure, dict):
        print(f"错误: 结构必须是字典，但得到了 {type(structure)}")
        return
    
    def create_directories(current_path, current_structure):
        """递归创建目录和文件"""
        if not isinstance(current_structure, dict):
            print(f"警告: 预期字典但得到 {type(current_structure)} 在路径 {current_path}")
            return
            
        print(f"处理目录: {current_path}")
        print(f"包含项目: {list(current_structure.keys())}")
            
        for name, content in current_structure.items():
            full_path = os.path.join(current_path, name)
            
            # 如果是目录
            if isinstance(content, dict):
                print(f"创建目录: {full_path}")
                try:
                    os.makedirs(full_path, exist_ok=True)
                    create_directories(full_path, content)
                except Exception as e:
                    print(f"创建目录 {full_path} 时出错: {e}")
            
            # 如果是文件
            elif isinstance(content, str) or content is None:
                print(f"创建文件: {full_path}")
                try:
                    # 确保父目录存在
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content or "")
                except Exception as e:
                    print(f"创建文件 {full_path} 时出错: {e}")
    
    # 创建根目录
    try:
        os.makedirs(base_path, exist_ok=True)
    except Exception as e:
        print(f"创建根目录 {base_path} 时出错: {e}")
        return
    
    # 创建目录和文件
    create_directories(base_path, structure)

def main():
    print("文件结构生成器")
    print("支持的输入格式:")
    print("1. 目录树文本")
    print("2. JSON")
    print("3. YAML")
    print("\n请输入文件结构（输入 'done' 完成）:")

    input_lines = []
    while True:
        line = input()
        if line.lower() == 'done':
            break
        input_lines.append(line)
    
    input_text = '\n'.join(input_lines)
    
    print(f"收到的输入:\n{input_text}")
    
    # 解析输入
    try:
        structure = parse_structure(input_text)
        
        # 询问保存路径
        project_path = input("请输入项目保存路径（默认为当前目录）: ") or '.'
        
        # 创建项目结构
        create_project_structure(project_path, structure)
        
        print(f"项目结构已成功创建在 {os.path.abspath(project_path)}")
    except Exception as e:
        print(f"解析或创建项目结构时出错: {e}")
        traceback.print_exc()  # 打印完整的错误堆栈

if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("未检测到 PyYAML，正在尝试安装...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyyaml'])
        import yaml

    main()