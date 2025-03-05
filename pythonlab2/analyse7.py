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

def analyze_idle_time(idle_data):
    stats = idle_data.groupby("Processor Count (n)").agg(
        Mean_Idle_Time=("Mean Idle Time", "mean")
    ).reset_index()
    return stats

def save_analysis_with_chart(stats, output_file="idle_time_analysis_n.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Idle_Time_Stats_N"

    ws.append(["Processor Count (n)", "Mean Idle Time"])
    for row in stats.itertuples(index=False):
        ws.append(list(row))

    wb.save(output_file)
    print(f"Результаты анализа сохранены в '{output_file}'.")

if __name__ == "__main__":
    try:
        idle_data = load_data(EXCEL_FILE)
        stats = analyze_idle_time(idle_data)
        save_analysis_with_chart(stats)
    except FileNotFoundError as e:
        print(e)
