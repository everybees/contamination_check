import csv
import os

LOG_PATH = "logs/evaluations.csv"
os.makedirs("logs", exist_ok=True)

def log_to_csv(task_id, system_version, base_code, user_prompt, result):
    header = [
        "task_id", "system_version", "prompt", "base_code",
        "contaminated", "contamination_link",
        "ambiguous_unfair", "problem_description",
        "suggested_fix", "confidence_rating", "judge_response"
    ]

    row = [
        task_id, system_version, user_prompt, base_code,
        result.contaminated, result.contamination_link,
        result.ambiguous_unfair, result.problem_description,
        result.suggested_fix, result.confidence_rating,
        result.judge_response
    ]

    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)