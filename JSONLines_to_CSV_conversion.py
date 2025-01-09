import pandas as pd
import json
file_path = r"<path>/<filename>.jsonl"

def tabulate_dataframe(df):
    columns_to_process = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (list, dict))).any()]
    for col in columns_to_process:
        df = df.explode(col, ignore_index=True)
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            normalized = pd.json_normalize(df[col]).add_prefix(f"{col}_")
            df = pd.concat([df.drop(columns=[col]), normalized], axis=1)
    return df.fillna("")

def normalize_the_json(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict))).any():
                normalized = pd.json_normalize(df[col])
                normalized.columns = [f"{col}_{subcol}" for subcol in normalized.columns]  
                df = pd.concat([df.drop(columns=[col]).reset_index(drop=True), normalized.reset_index(drop=True)], axis=1)
    return df

df = pd.read_json(file_path, lines=True)
print("just tabulated and not normalized")
print(df)
df.to_csv("not_normalized_jsontocsv.csv", index=False)

normalized_df = normalize_the_json(df)
print("half_normalized")
print(normalized_df)
normalized_df.to_csv("half_normalized.csv", index=False)

normalized_df = tabulate_dataframe(normalized_df)
print("full normalized")
print(normalized_df)
normalized_df.to_csv("full_normalized.csv", index=False)


