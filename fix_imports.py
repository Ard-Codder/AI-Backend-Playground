#!/usr/bin/env python3
"""
Скрипт для автоматического добавления # type: ignore к проблемным импортам
"""
import os
import re

def fix_imports_in_file(file_path):
    """Исправляет импорты в файле"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Список проблемных импортов
    problematic_imports = [
        'from pydantic import',
        'from pydantic_settings import',
        'from sqlalchemy import',
        'from sqlalchemy.ext.asyncio import',
        'from sqlalchemy.orm import',
        'from sqlalchemy.exc import',
        'from fastapi import',
        'from fastapi.security import',
        'from fastapi.middleware.cors import',
        'from fastapi.responses import',
        'from uvicorn import',
        'from sklearn.model_selection import',
    ]
    
    modified = False
    for import_line in problematic_imports:
        # Ищем строки с импортами, которые еще не имеют # type: ignore
        pattern = rf'^({re.escape(import_line)}.*?)(?:\s*#\s*type:\s*ignore)?$'
        replacement = r'\1  # type: ignore'
        
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed imports in {file_path}")
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
                    fix_imports_in_file(file_path)

if __name__ == '__main__':
    main()
