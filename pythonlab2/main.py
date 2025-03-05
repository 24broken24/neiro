import numpy as np
import pandas as pd
import heapq
from openpyxl import Workbook

n_range = range(2, 6)
m_range = range(5, 21, 5)

lambda_1 = 1
sigma = 0.2
tau = 0.1


def simulate(n, m, lambdas, sigma_value, sigma_type, tau):

    interarrival_times = np.random.exponential(1 / np.array(lambdas))
    arrival_times = np.cumsum(interarrival_times)

    required_times = np.random.exponential(1 / np.array(lambdas))

    tasks = {}
    for i in range(m):
        tasks[i] = {
            "Task Index": i,
            "Arrival Time": arrival_times[i],
            "Required Time": required_times[i],
            "Remaining Time": required_times[i],
            "Waiting Time": 0.0,
            "Context Time": 0.0,
            "Service Time": 0.0,
            "Completion Time": None,
            "Last Queue Entry": arrival_times[i]
        }

    events = []
    for i in range(m):
        heapq.heappush(events, (tasks[i]["Arrival Time"], "arrival", i))

    processor_free_times = [0.0] * n
    processor_idle_times = [0.0] * n

    queue = []
    tasks_completed = 0
    current_time = 0.0

    while tasks_completed < m:
        if events:
            event = heapq.heappop(events)
            if event[1] == "arrival":
                event_time, _, task_id = event
                current_time = event_time
                queue.append(task_id)
                tasks[task_id]["Last Queue Entry"] = current_time
            elif event[1] == "finish":
                event_time, _, task_id, proc_idx = event
                current_time = event_time
                if tasks[task_id]["Remaining Time"] > 0:
                    queue.append(task_id)
                    tasks[task_id]["Last Queue Entry"] = current_time
                else:
                    tasks[task_id]["Completion Time"] = current_time
                    tasks_completed += 1
        else:
            break

        available_processors = [j for j in range(n) if processor_free_times[j] <= current_time]
        while queue and available_processors:
            current_task_id = queue.pop(0)
            proc_idx = available_processors.pop(0)

            idle_gap = current_time - processor_free_times[proc_idx]
            if idle_gap > 0:
                processor_idle_times[proc_idx] += idle_gap

            tasks[current_task_id]["Waiting Time"] += current_time - tasks[current_task_id]["Last Queue Entry"]

            if sigma_type in ["constant", "controlled"]:
                allocated_time = sigma_value
            elif sigma_type == "uniform":
                allocated_time = np.random.uniform(0.5 * sigma_value, 1.5 * sigma_value)
            else:
                allocated_time = sigma_value

            slice_time = min(allocated_time, tasks[current_task_id]["Remaining Time"])
            tasks[current_task_id]["Context Time"] += tau
            tasks[current_task_id]["Service Time"] += slice_time
            tasks[current_task_id]["Remaining Time"] -= slice_time

            finish_time = current_time + tau + slice_time
            processor_free_times[proc_idx] = finish_time

            heapq.heappush(events, (finish_time, "finish", current_task_id, proc_idx))

    mean_idle_time = np.mean(processor_idle_times)

    task_records = []
    for i in range(m):
        task = tasks[i]
        total_execution_time = task["Completion Time"] - task["Arrival Time"] if task[
                                                                                     "Completion Time"] is not None else None
        task_records.append({
            "Processor Count (n)": n,
            "Task Count (m)": m,
            "Task Index": task["Task Index"],
            "Lambda": lambdas[i],
            "Arrival Time": task["Arrival Time"],
            "Waiting Time": task["Waiting Time"],
            "Context Time": task["Context Time"],
            "Service Time": task["Service Time"],
            "Total Execution Time": total_execution_time,
            "Required Time": task["Required Time"]
        })

    return task_records, mean_idle_time


def collect_data():
    global all_task_records, idle_times_summary
    all_task_records = []
    idle_times_summary = []

    for n in n_range:
        for m in m_range:
            lambdas_variant_1 = [lambda_1] * m
            lambdas_variant_2 = [2 * lambda_1 / (i + 1) for i in range(m)]

            for sigma_type in ["constant", "uniform", "controlled"]:
                for lambdas, variant in zip([lambdas_variant_1, lambdas_variant_2],
                                            ["Вариант 1", "Вариант 2"]):
                    task_records, mean_idle_time = simulate(n, m, lambdas, sigma, sigma_type, tau)
                    for record in task_records:
                        record["Lambda Variant"] = variant
                        record["Sigma Type"] = sigma_type
                    all_task_records.extend(task_records)

                    idle_times_summary.append({
                        "Processor Count (n)": n,
                        "Task Count (m)": m,
                        "Sigma Type": sigma_type,
                        "Lambda Variant": variant,
                        "Mean Idle Time": mean_idle_time
                    })


def save_to_excel():
    task_records_df = pd.DataFrame(all_task_records)
    idle_times_df = pd.DataFrame(idle_times_summary)

    with pd.ExcelWriter("simulation_results.xlsx", engine='openpyxl') as writer:
        task_records_df.to_excel(writer, sheet_name="Task_Data", index=False)
        idle_times_df.to_excel(writer, sheet_name="Idle_Times", index=False)

    print("Данные сохранены в 'simulation_results.xlsx' для дальнейшего построения графиков.")


if __name__ == "__main__":
    collect_data()
    save_to_excel()
