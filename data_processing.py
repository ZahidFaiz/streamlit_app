# data_processing.py
import pandas as pd


class data_prep:
    def __init__(self, file_path) -> None:
        self.df = self.load_data(file_path)

    def load_data(self, file_path):
        return pd.read_csv(file_path)

    def apply_filters(self, filters):
        mask = pd.Series([True] * len(self.df), index=self.df.index)

        for column, selected_categories in filters.items():
            if pd.api.types.is_numeric_dtype(self.df[column]):
                mask &= (self.df[column] >= selected_categories[0]) & (self.df[column] <= selected_categories[1])
            else:
                mask &= self.df[column].isin(selected_categories)

        self.filter_df = self.df[mask]
        return self.filter_df 

    def bar_chart1_df(self):
        return self.filter_df.groupby(['Product Name', 'Time Period']).agg({
            "Patient Count" : "sum", 
            "Claims volume" : "sum"
        }).reset_index()
    
    def bar_chart2_df(self):
        return self.filter_df.groupby(['Geography Location']).agg({
            "Patient Count" : "sum", 
        }).reset_index().sort_values("Patient Count", ascending=False)
    
    def bar_chart3_df(self):
        return self.filter_df.groupby(['Patient Age']).agg({
            "Patient Count" : "sum", 
        }).reset_index().sort_values("Patient Count", ascending=False)
    
    

    def pie_chart3_df(self):
        return self.filter_df.groupby(['Patient Gender']).agg({
            "Patient Count" : "sum", 
        }).reset_index().sort_values("Patient Count", ascending=False)
    
    def st_bar_chart1_df(self):
        m1 =  self.filter_df.groupby(['Time Period', 'Product Name']).agg({
            "Claims volume" : "sum", 
        }).reset_index().sort_values("Time Period", ascending=False)

        m2 =  self.filter_df.groupby(['Time Period']).agg({
            "Claims volume" : "sum", 
        }).reset_index().sort_values("Time Period", ascending=False)
        m2.columns = ["Time Period", "tot_claims"]

        mr = m1.merge(m2, on = ["Time Period"], how='left')
        mr["%"] = mr["Claims volume"]/mr["tot_claims"]

        mr = mr.pivot_table(index=["Time Period"], columns=["Product Name"], values=["%"])
        mr.columns = ['_'.join(map(str, col)) for col in mr.columns]
        mr = mr.reset_index()
        return mr
    
    def st_bar_chart2_df(self):
        m1 =  self.filter_df.groupby(['Time Period', 'Product Name']).agg({
            "Patient Count" : "sum", 
        }).reset_index().sort_values("Time Period", ascending=False)

        m2 =  self.filter_df.groupby(['Time Period']).agg({
            "Patient Count" : "sum", 
        }).reset_index().sort_values("Time Period", ascending=False)
        m2.columns = ["Time Period", "tot_claims"]

        mr = m1.merge(m2, on = ["Time Period"], how='left')
        mr["%"] = mr["Patient Count"]/mr["tot_claims"]

        mr = mr.pivot_table(index=["Time Period"], columns=["Product Name"], values=["%"])
        mr.columns = ['_'.join(map(str, col)) for col in mr.columns]
        mr = mr.reset_index()
        return mr