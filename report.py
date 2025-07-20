# backend/report.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report():
    try:
        if not os.path.exists('data/focus_log.csv'):
            print("⚠️ focus_log.csv not found")
            return None

        df = pd.read_csv('data/focus_log.csv')
        if df.empty:
            print("⚠️ focus_log.csv is empty")
            return None

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Day'] = df['Timestamp'].dt.date

        summary = df.groupby(['Day', 'Status']).size().unstack(fill_value=0)

        plt.figure(figsize=(10, 5))
        summary.plot(kind='bar', stacked=True, color=['red', 'green', 'yellow', 'cyan'])
        plt.title("Focus vs Distraction - Daily Summary")
        plt.xlabel("Day")
        plt.ylabel("Entries")
        plt.tight_layout()

        os.makedirs('static', exist_ok=True)
        plt.savefig('static/report.png')
        plt.close()
        return 'static/report.png'

    except Exception as e:
        print(f"❌ Error in generate_report: {e}")
        return None

