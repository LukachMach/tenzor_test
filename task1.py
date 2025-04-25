import requests
import datetime
import time

def fetch_time_data():
    """Запрашивает данные о времени с API."""
    url = "https://yandex.com/time/sync.json?geo=213"
    response = requests.get(url)
    
    # Проверка статуса ответа
    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе данных: {response.status_code}")
    
    return response.json()

def convert_unix_time(unix_time, offset):
    """Преобразует Unix timestamp в читаемый формат и возвращает временную зону."""
    unix_time_seconds = unix_time / 1000
    current_time_utc = datetime.datetime.fromtimestamp(unix_time_seconds, tz=datetime.timezone.utc)
    
    timezone_offset = datetime.timedelta(seconds=offset)
    current_time_local = current_time_utc + timezone_offset
    
    return current_time_local, current_time_local.tzinfo

def main():
    """Основная функция программы."""
    try:
        # a) Получаем данные о времени
        data = fetch_time_data()
        print("Сырой ответ:", data)

        # Извлекаем Unix timestamp и смещение
        unix_time = data.get('time')
        offset = data.get('offset', 0)  # Используем 0 как значение по умолчанию
        
        if unix_time is not None:
            print("Полученное время (Unix timestamp):", unix_time)
            print("Смещение (offset):", offset)

            # b) Преобразуем время и выводим результат
            current_time_local, timezone_info = convert_unix_time(unix_time, offset)
            print("Текущее время:", current_time_local.strftime("%Y-%m-%d %H:%M:%S"))
            print("Временная зона:", timezone_info)

            # c) Вычисляем дельту времени
            start_time = time.time()  # Время начала выполнения запроса
            delta = abs(start_time - unix_time / 1000)  # Дельта времени в секундах
            print(f"Дельта времени: {delta:.2f} секунд")

            # d) Повторяем замеры 5 раз и вычисляем среднюю дельту
            deltas = []
            for _ in range(5):
                start_request = time.time()
                data = fetch_time_data()  # Повторяем запрос
                unix_time = data.get('time')
                if unix_time is not None:
                    delta = abs(start_request - unix_time / 1000)
                    deltas.append(delta)
                    print(f"Запрос {_+1}: Дельта времени: {delta:.2f} секунд")
                time.sleep(1)  # Задержка между запросами
            
            average_delta = sum(deltas) / len(deltas)
            print(f"Средняя дельта времени за 5 запросов: {average_delta:.2f} секунд")
        
        else:
            print("Ключ 'time' отсутствует в ответе.")
    
    except Exception as e:
        print("Произошла ошибка:", str(e))

if __name__ == "__main__":
    main()
