#!/usr/bin/env python3
"""
Скрипт для удаления всех # type: ignore комментариев
"""
import os
import re

def remove_type_ignores_in_file(file_path):
    """Удаляет все # type: ignore комментарии из файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем все # type: ignore комментарии
    lines = content.split('\n')
    modified_lines = []
    
    for line in lines:
        # Удаляем # type: ignore из конца строки
        new_line = re.sub(r'\s*#\s*type:\s*ignore\s*$', '', line)
        modified_lines.append(new_line)
    
    new_content = '\n'.join(modified_lines)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed type ignores from {file_path}")
        return True
    return False

def main():
    """Основная функция"""
    # Находим все Python файлы в backend/
    for root, dirs, files in os.walk('backend/'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                remove_type_ignores_in_file(file_path)

if __name__ == '__main__':
    main()
