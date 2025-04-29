import json
import re
import sys
from itertools import product

def generate_versions(template):
    parts = template.split('.')
    wildcards = [i for i, part in enumerate(parts) if part == '*']
    
    # Генерируем все возможные комбинации для символа *
    combinations = []
    for wildcard in wildcards:
        # Заменяем * на 0 и 1 для генерации двух вариантов
        new_parts = parts[:]
        new_parts[wildcard] = '0'
        combinations.append('.'.join(new_parts))
        
        new_parts[wildcard] = '1'
        combinations.append('.'.join(new_parts))
    
    return combinations

def main(version_to_compare, config_file):
    with open(config_file) as f:
        templates = json.load(f)

    all_versions = set()

    for key, template in templates.items():
        generated_versions = generate_versions(template)
        all_versions.update(generated_versions)

    # Сортируем версии
    sorted_versions = sorted(all_versions, key=lambda x: list(map(int, x.split('.'))))

    print("Все сгенерированные версии:")
    print(sorted_versions)

    # Фильтруем версии меньше заданной
    filtered_versions = [v for v in sorted_versions if list(map(int, v.split('.'))) < list(map(int, version_to_compare.split('.')))]
    
    print("\nВерсии меньше заданной:")
    print(filtered_versions)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python version_generator.py <номер_версии> <конфигурационный_файл>")
        sys.exit(1)

    version_input = sys.argv[1]
    config_filename = sys.argv[2]

    main(version_input, config_filename)
