import os
import pandas as pd
import numpy as np
from datetime import datetime

class AICustomerSegmentationAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.rfm_df = None

    def load_data(self):
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == '.csv':
            self.df = pd.read_csv(self.file_path, encoding='latin1')
        elif ext in ['.xls', '.xlsx']:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file format. Please upload a .csv or .xlsx file.")
        
        # Clean column names and remove duplicates
        self.df.columns = [str(c).strip() for c in self.df.columns]
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]
        
        # Smart column auto-detection
        cust_col, order_col, date_col, amount_col = None, None, None, None
        
        for col in self.df.columns:
            col_lower = col.lower()
            if not cust_col and any(k in col_lower for k in ['customer', 'client', 'userid', 'member', 'user']):
                cust_col = col
            elif not order_col and any(k in col_lower for k in ['invoice', 'order', 'transaction', 'id', 'no']):
                order_col = col
            elif not date_col and any(k in col_lower for k in ['date', 'time', 'timestamp', 'created']):
                date_col = col
            elif not amount_col and any(k in col_lower for k in ['amount', 'price', 'sales', 'revenue', 'total', 'monetary', 'fare', 'unit', 'cost', 'qty', 'quantity']):
                amount_col = col

        clean_df = pd.DataFrame()
        clean_df['CustomerID'] = self.df[cust_col] if cust_col else self.df.iloc[:, 0]
        clean_df['OrderID'] = self.df[order_col] if order_col else pd.Series(range(1, len(self.df) + 1))
        
        if date_col:
            clean_df['OrderDate'] = pd.to_datetime(self.df[date_col], errors='coerce').fillna(pd.Timestamp('2026-01-01'))
        else:
            clean_df['OrderDate'] = pd.Timestamp('2026-01-01')

        if amount_col:
            clean_df['Amount'] = pd.to_numeric(self.df[amount_col], errors='coerce').fillna(100.0)
        else:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            clean_df['Amount'] = pd.to_numeric(self.df[numeric_cols[0]], errors='coerce').fillna(100.0) if len(numeric_cols) > 0 else 100.0

        for col in clean_df.columns:
            if isinstance(clean_df[col], pd.DataFrame):
                clean_df[col] = clean_df[col].iloc[:, 0]

        self.df = clean_df.drop_duplicates()
        return self.df

    def calculate_rfm(self):
        snapshot_date = self.df['OrderDate'].max() + pd.Timedelta(days=1)
        rfm = self.df.groupby('CustomerID', as_index=False).agg({
            'OrderDate': lambda x: (snapshot_date - x.max()).days,
            'OrderID': 'count',
            'Amount': 'sum'
        })
        rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        q_bins = min(4, len(rfm))
        if q_bins < 2:
            rfm['R_Score'] = 1
            rfm['F_Score'] = 1
            rfm['M_Score'] = 1
        else:
            labels = list(range(q_bins, 0, -1))
            rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), q=q_bins, labels=labels, duplicates='drop').astype(int)
            labels_asc = list(range(1, q_bins + 1))
            rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=q_bins, labels=labels_asc, duplicates='drop').astype(int)
            rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=q_bins, labels=labels_asc, duplicates='drop').astype(int)
        
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        
        def assign_segment(row):
            r, f = row['R_Score'], row['F_Score']
            if r >= 3 and f >= 3:
                return 'Champions'
            elif r >= 2 and f >= 2:
                return 'Loyal'
            elif r <= 2 and f >= 3:
                return 'At Risk'
            elif r >= 3 and f == 1:
                return 'New Customers'
            else:
                return 'Dormant'

        rfm['Segment'] = rfm.apply(assign_segment, axis=1)
        self.rfm_df = rfm
        return self.rfm_df

    def generate_personalized_campaigns(self):
        def create_message(row):
            segment = row['Segment']
            cust_id = row['CustomerID']
            if segment == 'Champions':
                discount = 0
                message = f"Hi #{cust_id}, enjoy exclusive VIP early access to our new arrivals and special member perks!"
            elif segment == 'Loyal':
                discount = 5
                message = f"Hi #{cust_id}, thank you for your ongoing support! Here is a special 5% bundle discount on your favorite products."
            elif segment == 'At Risk':
                discount = 12
                message = f"We miss you, #{cust_id}! Come back and enjoy 12% off your next purchase with code WELCOME12."
            elif segment == 'New Customers':
                discount = 10
                message = f"Welcome aboard, #{cust_id}! Enjoy 10% off your second order to explore more of our collection."
            else:
                discount = 5
                message = f"Hello #{cust_id}, discover what's new in store with an exclusive 5% welcome-back offer."
            return pd.Series([discount, message])

        self.rfm_df[['Assigned_Discount_%', 'Automated_Message']] = self.rfm_df.apply(create_message, axis=1)
        return self.rfm_df

    def run_pipeline(self, output_path="campaign_output.csv"):
        self.load_data()
        self.calculate_rfm()
        self.generate_personalized_campaigns()
        self.rfm_df.to_csv(output_path, index=False)
        return self.rfm_df