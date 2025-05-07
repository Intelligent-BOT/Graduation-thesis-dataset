import os
import sys
import re

def clean_tex_content(content):
    """
    清除LaTeX格式并返回纯文本
    处理步骤：
    1. 删除注释
    2. 删除LaTeX命令
    3. 删除数学公式
    4. 删除环境内容
    5. 清理多余空格
    """
    # 删除单行注释（保留行末注释后的内容）
    content = re.sub(r'\\%.*', '', content)
    
    # 删除多行注释（verbatim环境）
    content = re.sub(r'\\begin\{verbatim\}.*?\\end\{verbatim\}', '', content, flags=re.DOTALL)
    
    # 删除所有LaTeX命令（包括带参数的命令）
    content = re.sub(r'\\([a-zA-Z]+|\*|\[|\]|{|}|_|\^|~|`|,|\.|\||=|\'|"|-)', '', content)
    
    # 删除带参数的命令（例如 \command{...} 或 \command[...]{...}）
    content = re.sub(r'\\[a-zA-Z]+\*?(?:\[.*?\]){0,2}(?:{.*?}){0,2}', '', content)
    
    # 删除数学公式（行内和行间）
    content = re.sub(r'\$.*?\$', '', content, flags=re.DOTALL)
    content = re.sub(r'\\\[.*?\\\]', '', content, flags=re.DOTALL)
    
    # 删除环境内容（保留环境内的文本）
    content = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '', content, flags=re.DOTALL)
    
    # 清理特殊字符
    content = content.replace('\\', ' ')  # 处理转义字符
    content = re.sub(r'[{}]', ' ', content)  # 删除花括号
    
    # 合并连续空格和空行
    content = re.sub(r'\n\s*\n', '\n\n', content)  # 保留段落间距
    content = re.sub(r'[ \t]+', ' ', content)  # 合并连续空格
    
    # 删除首尾空白
    content = content.strip()
    
    return content

def convert_tex_to_plaintext(input_dir, output_dir):
    """
    转换指定目录中的所有.tex文件为纯文本，并将结果保存到另一个目录
    """
    count = 0
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.tex'):
            continue
        
        tex_path = os.path.join(input_dir, filename)
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(output_dir, txt_filename)

        try:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)

            # 读取文件内容（自动检测编码）
            with open(tex_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # 清洗内容
            cleaned = clean_tex_content(content)
            
            # 写入新文件
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            print(f"✓ 转换成功: {filename}")
            count += 1
        
        except Exception as e:
            print(f"✕ 转换失败: {filename} - {str(e)}")
    
    return count

if __name__ == "__main__":
    # 获取输入和输出目录
    if len(sys.argv) < 3:
        print("用法: python script.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # 验证目录有效性
    if not os.path.isdir(input_dir):
        print(f"错误：无效输入目录 - {input_dir}")
        sys.exit(1)

    print("开始转换...\n" + "-"*40)
    success_count = convert_tex_to_plaintext(input_dir, output_dir)
    print("-"*40 + f"\n完成！成功转换 {success_count} 个文件")
    print("注意事项：")
    print("- 数学公式和表格等内容已被移除")
    print("- 复杂的LaTeX结构可能需要手动调整")
    print("- 建议检查转换后的文本格式")