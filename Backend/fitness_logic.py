
import os
import pandas as pd

def get_fitness_plan():
    # Expect dataset/Weekly_Workouts.csv at project root
    project_root = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(project_root, "dataset", "Weekly_Workouts.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)
    df = pd.read_csv(csv_path)
    # Normalize column names if needed
    df.columns = [c.strip().title() for c in df.columns]
    return df.to_dict(orient="records")
