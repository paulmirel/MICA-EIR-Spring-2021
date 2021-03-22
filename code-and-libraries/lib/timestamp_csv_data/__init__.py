# Because we have our module as timestamp_csv_data/timestamp_csv_data.py
# You would normally have to: import timestamp_csv_data && then timestamp_csv_data.timestamp_csv_data.TimeStampCSV
# So, lift them

# Lift TimeStampCSV, and other toplevel functions as if timestamp_csv_data.TimeStampCSV

# so, locally the nested timestamp_csv_data
from .timestamp_csv_data import TimeStampCSV
