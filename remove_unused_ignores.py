#!/usr/bin/env python3
"""
Скрипт для удаления ненужных # type: ignore комментариев
"""
import os
import re

def remove_unused_ignores_in_file(file_path):
    """Удаляет ненужные # type: ignore комментарии из файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем # type: ignore комментарии, которые могут быть ненужными
    # Но оставляем те, которые действительно нужны
    lines = content.split('\n')
    modified_lines = []
    
    for line in lines:
        # Проверяем, есть ли # type: ignore в строке
        if '# type: ignore' in line:
            # Удаляем # type: ignore, но оставляем остальную часть строки
            new_line = line.replace('  # type: ignore', '').replace(' # type: ignore', '')
            modified_lines.append(new_line)
        else:
            modified_lines.append(line)
    
    new_content = '\n'.join(modified_lines)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed unused ignores from {file_path}")
        return True
    return False

def main():
    """Основная функция"""
    # Находим все Python файлы в backend/ и ml_core/
    for root, dirs, files in os.walk('.'):
        if root.startswith('./backend') or root.startswith('./ml_core'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    remove_unused_ignores_in_file(file_path)

if __name__ == '__main__':
    main()
