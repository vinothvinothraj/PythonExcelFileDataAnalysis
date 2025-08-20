import pandas as pd
from sqlalchemy import text
from config import engine
import os

def export_samples(file_id, output_folder, db_session=None):
    # Use SQLAlchemy connection to avoid pandas DBAPI warnings
    with engine.connect() as conn:
        events = pd.read_sql(
            text("SELECT * FROM events WHERE file_id = :file_id ORDER BY time"),
            conn,
            params={"file_id": int(file_id)},
        )
        data = pd.read_sql(
            text("SELECT * FROM data WHERE file_id = :file_id ORDER BY time"),
            conn,
            params={"file_id": int(file_id)},
        )

    # Extract sample periods
    # Normalize event type strings by trimming and lowercasing for robust matching
    normalized_type = events["type"].astype(str).str.strip().str.lower()
    starts = events.loc[normalized_type == "twist detected - sampling (re-)started", "time"].tolist()
    ends = events.loc[normalized_type == "twist detected - sampling paused", "time"].tolist()
    periods = list(zip(starts, ends))

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"processed_file_{file_id}.xlsx")
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for i, (start, end) in enumerate(periods, start=1):
            sample = data[(data["time"] >= start) & (data["time"] <= end)].copy()
            sample.insert(0, "Sample_ID", i)
            sample.insert(1, "Period_From", start)
            sample.insert(2, "Period_To", end)
            sample.to_excel(writer, sheet_name=f"Sample_{i}", index=False)

    return output_file
