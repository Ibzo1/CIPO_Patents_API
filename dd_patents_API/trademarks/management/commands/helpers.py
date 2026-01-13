# import logging
# from datetime import datetime

# # Helper function to handle 'Unknown' or empty values
# def process_row(row):
#     processed_row = []
#     for value in row:
#         if value == 'Unknown' or value == '':
#             processed_row.append(None)
#         else:
#             processed_row.append(value)
#     return processed_row

# # Helper function to validate and process date fields
# def validate_and_process_date(date_str):
#     if date_str == '' or date_str == 'Unknown':
#         return None
#     try:
#         # Ensure the date format is correct
#         return datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         logging.warning(f"Invalid date format for value: {date_str}. Setting as None.")
#         return None

import datetime

def validate_and_process_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def process_row(row):
    processed_row = []
    for value in row:
        if value in ['Unknown', '']:
            processed_row.append(None)
        elif isinstance(value, str) and len(value) > 2 and '_code' in value:
            processed_row.append(value[:2])
        else:
            processed_row.append(value)
    return processed_row
