from utils.db import get_connection
from utils.excel_reader import read_excel
import pandas as pd
import numpy as np

def import_excel(file_id, file_path, db_session=None):
    """Import Excel contents into DB.

    Prefers using a raw connection for efficient bulk inserts, but keeps the
    signature compatible with the Flask caller which passes a session.
    """
    events, data = read_excel(file_path)
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Insert Events
        for _, row in events.iterrows():
            if pd.notna(row["Time"]):
                time_val = row["Time"].to_pydatetime() if hasattr(row["Time"], "to_pydatetime") else row["Time"]
                type_val = row["Type"] if not isinstance(row["Type"], (pd.Series, np.ndarray)) else str(row["Type"]) 
                cur.execute(
                    """
                    INSERT INTO events (file_id, time, type) VALUES (%s, %s, %s)
                    """,
                    (int(file_id), time_val, type_val),
                )

        # Insert Data
        # Build a normalized mapping from possible header variations to DB columns
        header_map = {h.strip().lower(): h for h in data.columns if isinstance(h, str)}
        def get_col(*candidates):
            for cand in candidates:
                key = cand.strip().lower()
                if key in header_map:
                    return header_map[key]
            return None

        col_time = get_col("time")
        col_cond = get_col("conductivity", "specific conductivity", "specific_conductivity")
        col_temp = get_col("temperature")
        col_pressure = get_col("pressure")
        col_sea_pressure = get_col("sea pressure", "sea_pressure")
        col_do_sat = get_col("dissolved o2 saturation", "dissolved_o2_saturation")
        col_chl = get_col("chlorophyll-a", "chlorophyll_a")
        col_fdom = get_col("fdom")
        col_turb = get_col("turbidity")
        col_depth = get_col("depth")
        col_sal = get_col("salinity")
        col_sos = get_col("speed of sound", "speed_of_sound")
        col_spec = get_col("specific conductivity", "specific_conductivity", "conductivity specific")
        col_density = get_col("density anomaly", "density_anomaly")
        col_do_conc = get_col("dissolved o2 concentration", "dissolved_o2_concentration")

        for _, row in data.iterrows():
            if not col_time:
                continue
            time_val = row.get(col_time)
            if pd.notna(time_val):
                time_val = time_val.to_pydatetime() if hasattr(time_val, "to_pydatetime") else time_val

                def to_scalar(x):
                    if isinstance(x, (pd.Series, np.ndarray)):
                        return x.item() if hasattr(x, "item") else (x.tolist()[0] if len(x) else None)
                    if pd.isna(x):
                        return None
                    # Convert numpy types to Python scalars
                    if isinstance(x, (np.generic,)):
                        return x.item()
                    return x

                cur.execute(
                    """
                    INSERT INTO data 
                    (file_id, time, conductivity, temperature, pressure, sea_pressure,
                    dissolved_o2_saturation, chlorophyll_a, fdom, turbidity, 
                    depth, salinity, speed_of_sound, specific_conductivity, density_anomaly,
                    dissolved_o2_concentration)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(file_id),
                        time_val,
                        to_scalar(row.get(col_cond)) if col_cond else None,
                        to_scalar(row.get(col_temp)) if col_temp else None,
                        to_scalar(row.get(col_pressure)) if col_pressure else None,
                        to_scalar(row.get(col_sea_pressure)) if col_sea_pressure else None,
                        to_scalar(row.get(col_do_sat)) if col_do_sat else None,
                        to_scalar(row.get(col_chl)) if col_chl else None,
                        to_scalar(row.get(col_fdom)) if col_fdom else None,
                        to_scalar(row.get(col_turb)) if col_turb else None,
                        to_scalar(row.get(col_depth)) if col_depth else None,
                        to_scalar(row.get(col_sal)) if col_sal else None,
                        to_scalar(row.get(col_sos)) if col_sos else None,
                        to_scalar(row.get(col_spec)) if col_spec else None,
                        to_scalar(row.get(col_density)) if col_density else None,
                        to_scalar(row.get(col_do_conc)) if col_do_conc else None,
                    ),
                )

        conn.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()
