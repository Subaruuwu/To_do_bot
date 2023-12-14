import csv
from datetime import datetime, timedelta
import pandas as pd


def write_task_to_csv(user_data, csv_filename='tasks.csv'):
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for user_id, tasks in user_data.items():
            for task_name, task_details in tasks.items():
                for date, details in task_details.items():
                    if isinstance(details, dict):
                        start_time = details.get('start', '')
                        end_time = details.get('end', '')
                    elif isinstance(details, str):
                        start_time = end_time = details
                    else:
                        continue

                    # Преобразование времени в формат ISO
                    start_iso = (
                        datetime.fromisoformat(start_time).isoformat()
                        if start_time and start_time not in ['дедлайн от пользователя', 'в процессе']
                        else ''
                    )
                    end_iso = (
                        datetime.fromisoformat(end_time).isoformat()
                        if end_time and end_time not in ['дедлайн от пользователя', 'в процессе']
                        else ''
                    )

                    # Запись в CSV файл
                    writer.writerow([user_id, task_name, date, start_iso, end_iso])

# Пример использования:
user_data = {
    'id': {
        'zadacha_1': {
            '20.11.2023': {'start': '2023-11-20T12:00:00', 'end': '2023-11-21T12:00:00'},
            '21.11.2023': {'start': '2023-11-21T12:00:00', 'end': '2023-11-22T12:00:00'}
        },
        'zadacha_2': {
            '20.11.2024': {'start': '2023-11-20T15:00:00', 'end': '2023-11-21T12:10:00'},
            '21.11.2025': {'start': '2023-11-21T11:00:00', 'end': '2023-11-22T12:00:00'}
        }
    }
}

#write_task_to_csv(user_data)


import pandas as pd
from datetime import datetime


def update_last_task_end_date(user_id, task_name, csv_filename='tasks.csv'):
    try:
        # Чтение CSV файла в DataFrame
        df = pd.read_csv(csv_filename)

        # Убедимся, что имена столбцов не содержат пробелов
        df.columns = df.columns.str.strip()

        # Фильтрация данных для конкретного пользователя и задачи
        filtered_df = df[(df['user_id'] == user_id) & (df['task_name'] == task_name) & (df['end_iso'] == '0')]

        # Если есть запись с временем окончания равным 0, то обновляем ее
        if not filtered_df.empty:
            # Поиск индекса записи с временем окончания равным 0
            zero_end_time_index = filtered_df.index[0]

            # Получение текущей даты в формате ISO без миллисекунд
            current_date_iso = datetime.utcnow().replace(microsecond=0).isoformat()

            # Обновление значения даты окончания в DataFrame
            df.at[zero_end_time_index, 'end_iso'] = current_date_iso

            # Запись обновленного DataFrame обратно в CSV файл
            df.to_csv(csv_filename, index=False, encoding='utf-8')

            print(f"Дата окончания для пользователя {user_id}, задачи {task_name} обновлена успешно.")
        else:
            print(f"Запись с временем окончания равным 0 для пользователя {user_id}, задачи {task_name} не найдена.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


#update_last_task_end_date('id', 'zadacha_2')


def generate_user_summary(user_id, csv_filename='tasks.csv'):
    try:
        # Чтение CSV файла в DataFrame
        df = pd.read_csv(csv_filename)

        # Убедимся, что имена столбцов не содержат пробелов
        df.columns = df.columns.str.strip()

        # Фильтрация данных для конкретного пользователя и задач
        user_df = df[(df['user_id'] == user_id) & (df['end_iso'] != '0')]

        # Инициализация переменных для подсчета
        total_tasks_completed = 0
        total_execution_time = timedelta()
        task_count = {}

        # Подсчет количества выполненных задач и общего времени выполнения
        for index, row in user_df.iterrows():
            total_tasks_completed += 1
            start_time = datetime.fromisoformat(row['start_iso'])
            end_time = datetime.fromisoformat(row['end_iso'])
            execution_time = end_time - start_time
            total_execution_time += execution_time

            # Подсчет количества выполнений каждой задачи
            task_name = row['task_name']
            task_count[task_name] = task_count.get(task_name, 0) + 1

        # Вычисление среднего времени выполнения задачи
        average_execution_time = total_execution_time / total_tasks_completed if total_tasks_completed > 0 else timedelta()

        # Вывод результатов
        print(f"Сводка для пользователя {user_id}:")
        print(f"Выполнено задач: {total_tasks_completed}")
        print(f"Среднее время выполнения задачи: {str(average_execution_time)}")
        print("Количество выполнений каждой задачи:")
        for task, count in task_count.items():
            print(f"{task}: {count} раз")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Пример использования:
generate_user_summary('id')

def create_task_record(user_id, task_name, date, start_time, end_time):
    task_record = {
        'user_id': user_id,
        'task_name': task_name,
        'date': date,
        'start_iso': start_time,
        'end_iso': end_time
    }

    # Проверка наличия файла
    try:
        df = pd.read_csv('tasks.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['user_id', 'task_name', 'date', 'start_iso', 'end_iso'])

    # Добавление новой записи в DataFrame
    df = pd.concat([df, pd.DataFrame([task_record])], ignore_index=True)

    # Запись в CSV файл
    df.to_csv('tasks.csv', index=False, encoding='utf-8')

# Пример использования
create_task_record('id', 'zadacha_3', '21.11.2025', '2023-11-21T11:00:00', '2023-12-13T23:54:04')