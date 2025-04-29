#!/bin/bash

# Получаем список юнитов, начинающихся на "foobar-"
units=$(systemctl list-units --type=service --all | grep 'foobar-' | awk '{print $1}')

# Проверяем, есть ли юниты для обработки
if [ -z "$units" ]; then
    echo "Нет зарегистрированных юнитов с именем 'foobar-'"
    exit 0
fi

# Проходим по каждому юниту
for unit in $units; do
    service_name=${unit##*-}  # Извлекаем название сервиса из имени юнита

    echo "Обработка юнита: $unit"

    # Останавливаем сервис
    systemctl stop "$unit"

    # Получаем рабочую директорию и команду запуска
    working_directory=$(systemctl show "$unit" -p WorkingDirectory | cut -d'=' -f2)
    exec_start=$(systemctl show "$unit" -p ExecStart | cut -d'=' -f2)

    echo "Рабочая директория: $working_directory"
    echo "Команда запуска: $exec_start"

    # Переносим файлы в новую директорию
    new_directory="/srv/data/$service_name"
    
    mkdir -p "$new_directory"  # Создаем новую директорию, если она не существует
    mv "$working_directory/"* "$new_directory/"  # Переносим файлы

    # Обновляем пути в конфигурации юнита
    new_working_directory="WorkingDirectory=$new_directory"
    
    # Изменяем ExecStart, заменяя старую рабочую директорию на новую
    new_exec_start=$(echo "$exec_start" | sed "s|$working_directory|$new_directory|")

    # Создаем временный файл для изменения конфигурации
    temp_file=$(mktemp)

    # Считываем текущую конфигурацию и изменяем необходимые параметры
    systemctl cat "$unit" > "$temp_file"
    
    sed -i "s|^WorkingDirectory=.*|$new_working_directory|" "$temp_file"
    sed -i "s|^ExecStart=.*|$new_exec_start|" "$temp_file"

    # Перезаписываем конфигурацию юнита (необходимо с правами суперпользователя)
    sudo cp "$temp_file" "/etc/systemd/system/$unit"

    # Удаляем временный файл
    rm "$temp_file"

    # Запускаем сервис снова
    systemctl start "$unit"

    echo "Сервис $unit успешно перезапущен."
done

echo "Все сервисы обработаны."
