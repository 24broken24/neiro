import numpy as np
import pandas as pd
import os
from openpyxl import Workbook

EXCEL_FILE = "simulation_results.xlsx"

def load_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден. Проверьте путь и имя файла.")

    idle_data = pd.read_excel(filename, sheet_name="Idle_Times")
    return idle_data

def analyze_idle_time(idle_data, group_by):
    if idle_data.empty:
        print("Загруженный лист Idle_Times пуст!")
        return pd.DataFrame()

    stats = idle_data.groupby(group_by, as_index=False).agg({"Mean Idle Time": "mean"})
    return stats

def save_analysis_with_chart(stats, param, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Idle_Time_Stats_{param}"

    ws.append([param, "Mean Idle Time"])
    for _, row in stats.iterrows():
        ws.append([row[param], row["Mean Idle Time"]])


    wb.save(output_file)
    print(f"Результаты анализа сохранены в '{output_file}'.")

if __name__ == "__main__":
    try:
        idle_data = load_data(EXCEL_FILE)
        stats_m = analyze_idle_time(idle_data, "Task Count (m)")
        if stats_m.empty:
            print("Статистика по времени простоя пуста! Проверьте исходные данные.")
        else:
            save_analysis_with_chart(stats_m, "Task Count (m)", "idle_time_analysis_m.xlsx")
    except FileNotFoundError as e:
        print(e)
