import pandas as pd

def _find_sheet_name(xl: pd.ExcelFile, target: str) -> str:
    desired = target.strip().lower()
    for name in xl.sheet_names:
        normalized = str(name).strip().lower()
        if normalized == desired:
            return name
    # try contains match
    for name in xl.sheet_names:
        normalized = str(name).strip().lower()
        if desired in normalized:
            return name
    raise ValueError(f"Worksheet named '{target}' not found")

def read_excel(file_path):
    xl = pd.ExcelFile(file_path)
    events_sheet = _find_sheet_name(xl, "Events")
    data_sheet = _find_sheet_name(xl, "Data")

    events = pd.read_excel(file_path, sheet_name=events_sheet)
    data = pd.read_excel(file_path, sheet_name=data_sheet, header=None)

    # Normalize events columns to exactly ['Time', 'Type'] using first two columns
    if events.shape[1] < 2:
        raise ValueError("'Events' sheet must have at least two columns: Time and Type")
    events = events.iloc[:, :2]
    events.columns = ["Time", "Type"]

    # Detect the header row in the Data sheet by searching for a cell named 'Time'
    header_idx = 0
    search_rows = min(20, len(data))
    for i in range(search_rows):
        row_vals = data.iloc[i].astype(str).str.strip().str.lower().values.tolist()
        if any(val == "time" for val in row_vals):
            header_idx = i
            break
    data.columns = data.iloc[header_idx].astype(str).str.strip()
    data = data.drop(index=list(range(header_idx + 1))).reset_index(drop=True)

    # Drop completely empty columns
    data = data.dropna(axis=1, how="all")

    # Drop duplicate columns in data keeping the first occurrence
    if data.columns.duplicated().any():
        data = data.loc[:, ~data.columns.duplicated(keep="first")]

    # Convert time columns, support milliseconds explicitly
    def parse_time(series: pd.Series) -> pd.Series:
        # Try exact formats first for performance and precision
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            parsed = pd.to_datetime(series, format=fmt, errors="coerce")
            if parsed.notna().any():
                # Combine with a fallback for non-matching rows
                mask = parsed.notna()
                fallback = pd.to_datetime(series[~mask], errors="coerce")
                parsed.loc[~mask] = fallback
                return parsed
        return pd.to_datetime(series, errors="coerce")

    events["Time"] = parse_time(events["Time"])
    if "Time" in data.columns:
        data["Time"] = parse_time(data["Time"])

    return events, data
