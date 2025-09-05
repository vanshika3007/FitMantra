import os
import pandas as pd

def get_fitness_plan():
    # Locate the dataset folder correctly
    project_root = os.path.dirname(os.path.dirname(__file__))
    csv_path = os.path.join(project_root, "dataset", "Weekly_Workouts.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found!")

    # Read the CSV safely
    df = pd.read_csv(csv_path, quotechar='"')


    # Normalize column names (optional but clean)
    df.columns = [c.strip().title() for c in df.columns]

    # Return as JSON-like dict
    return df.to_dict(orient="records")
