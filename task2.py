import os
import json
import zipfile
import shutil
import subprocess
from datetime import datetime

def clone_repository(repo_url):
    """Клонирует репозиторий по указанному URL."""
    print(f"{datetime.now()}: Клонирование репозитория {repo_url}...")
    subprocess.run(["git", "clone", repo_url], check=True)

def remove_unwanted_directories(base_path, keep_dir):
    """Удаляет все директории в корне, кроме указанной."""
    print(f"{datetime.now()}: Удаление ненужных директорий в {base_path}...")
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item != keep_dir:
            shutil.rmtree(item_path)
            print(f"{datetime.now()}: Удалена директория {item_path}")

# def create_version_file(source_code_path, version):
#    """Создает файл version.json."""
#    print(f"{datetime.now()}: Создание файла version.json...")

def create_version_file(source_code_path, version):
    # Определяем путь к файлу
    version_file_path = os.path.join(source_code_path, 'big', 'app', 'version.json')

# Создаем директорию, если она не существует
    os.makedirs(os.path.dirname(version_file_path), exist_ok=True)
    
    # Записываем данные в файл
    with open(version_file_path, 'w') as version_file:
        version_file.write(version)    
    
    # Собираем список файлов с нужными расширениями
    files = []
    for root, _, filenames in os.walk(source_code_path):
        for filename in filenames:
            if filename.endswith(('.py', '.js', '.sh', 'go')):
                files.append(filename)

    version_info = {
        "name": "hello world",
        "version": version,
        "files": files
    }

    version_file_path = os.path.join(source_code_path, 'version.json')
    
    with open(version_file_path, 'w') as version_file:
        json.dump(version_info, version_file, indent=4)
    
    print(f"{datetime.now()}: Файл {version_file_path} создан.")

def create_archive(source_code_path):
    """Создает архив из исходного кода и файла version.json."""
    dir_name = os.path.basename(source_code_path)
    
    # Получаем текущую дату в формате ДДММГГГГ
    current_date = datetime.now().strftime("%d%m%Y")
    
    archive_name = f"{dir_name}{current_date}.zip"
    
    with zipfile.ZipFile(archive_name, 'w') as archive:
        for root, _, files in os.walk(source_code_path):
            for file in files:
                file_path = os.path.join(root, file)
                archive.write(file_path, os.path.relpath(file_path, source_code_path))
    
    print(f"{datetime.now()}: Архив {archive_name} создан.")

def main(repo_url, source_code_rel_path, version):
    """Основная функция скрипта."""
    
    # Клонируем репозиторий
    clone_repository(repo_url)

    # Получаем имя клонированного репозитория (последняя часть URL)
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    # Путь до исходного кода
    source_code_path = os.path.join(repo_name, source_code_rel_path)

    # Удаляем ненужные директории
    remove_unwanted_directories(repo_name, source_code_rel_path.split('/')[-1])

    # Создаем файл version.json
    create_version_file(source_code_path, version)

    # Создаем архив
    create_archive(source_code_path)

if __name__ == "__main__":
    repository_url = "https://github.com/LukachMach/big.git"
    relative_source_code_path = "app"
    product_version = "1.01"

    main(repository_url, relative_source_code_path, product_version)
