import pandas as pd

class FileManager:
    
    @staticmethod
    def load_csv(csv_path):
        return pd.read_csv(csv_path)

    @staticmethod
    def load_excel(excel_path, sheet_name=None):
        return pd.read_excel(excel_path, sheet_name=sheet_name)

    @staticmethod
    def save_to_csv(df, file_path):
        df.to_csv(file_path, index=False)

    @staticmethod
    def save_to_excel(df, file_path, sheet_name="Sheet1"):
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
