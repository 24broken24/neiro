import numpy as np
import pandas as pd
import os
from openpyxl import Workbook

EXCEL_FILE = "simulation_results.xlsx"

def load_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден. Проверьте путь и имя файла.")
    task_data = pd.read_excel(filename, sheet_name="Task_Data")
    return task_data

def analyze_execution_time(task_data):
    stats = task_data.groupby("Context Time").agg(
        Mean_Ti=("Total Execution Time", "mean"),
        Std_Ti=("Total Execution Time", "std")
    ).reset_index()
    return stats

def save_analysis_with_chart(stats, output_file="execution_time_analysis_tau.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Execution_Time_Stats_Tau"

    ws.append(["Context Time", "Mean Ti", "Std Ti"])
    for row in stats.itertuples(index=False):
        ws.append(list(row))

    wb.save(output_file)
    print(f"Результаты анализа сохранены в '{output_file}'.")

if __name__ == "__main__":
    try:
        task_data = load_data(EXCEL_FILE)
        stats = analyze_execution_time(task_data)
        save_analysis_with_chart(stats)
    except FileNotFoundError as e:
        print(e)
