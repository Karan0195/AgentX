import pandas as pd


class DataAgent:
    def __init__(self):
        self.name = "Data Agent"

    def get_status(self):
        return "Data Agent is ready."

    def load_data(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as error:
            print("Error loading dataset:", error)
            return None

    def get_data_info(self, data):
        return {
            "rows": data.shape[0],
            "columns": data.shape[1],
            "column_names": list(data.columns)
        }
    def check_missing_values(self, data):
        missing = data.isnull().sum()
        return missing.to_dict()

    def check_duplicates(self, data):
        duplicates = data.duplicated().sum()
        return int(duplicates)  

    def get_numeric_statistics(self, data):
        return data.describe().to_dict()   

    def generate_summary(self, data):
        return {
            "rows": data.shape[0],
            "columns": data.shape[1],
            "missing_values": int(data.isnull().sum().sum()),
            "duplicate_rows": int(data.duplicated().sum()),
            "numeric_columns": list(
                data.select_dtypes(include="number").columns
            )
        }       


if __name__ == "__main__":
    agent = DataAgent()
    print(agent.get_status())