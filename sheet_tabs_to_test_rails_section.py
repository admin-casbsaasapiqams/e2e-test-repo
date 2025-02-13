import requests
import base64
import json
import openpyxl


test_rail_instance = "https://trail.paloaltonetworks.local/index.php?/api/v2/"
username = "sahkumar@paloaltonetworks.com"
api_key = "AUYcvqeZfzBHaepgLVyS-8tQflvk1CPz3XaCLGzW/"
project_id = "50"
section_id = "127642"
g_sheet_file_path = "/Users/sahkumar/Documents/Region-parity/Connector Sanity Tests.xlsx"
def add_section():
    credentials = base64.b64encode(f"{username}:{api_key}".encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials}"
    }
    endpoint = f"{test_rail_instance}add_section/{project_id}"
    workbook = openpyxl.load_workbook(g_sheet_file_path)
    # Define the cell range
    # cell_range = sheet[f'{g_sheet_data_start_cell}:{g_sheet_data_end_cell}']
    for sheet_name in workbook.sheetnames:
        # for cell in row:
        if sheet_name and sheet_name.lower() not in ['count', 'efforts', 'target services and use cases',
                                                     'tests count', 'sheet8']:
                print(sheet_name)
                payload = {
                    "name": sheet_name,
                    # "parent_id": section_id
                }

                response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    test_case = response.json()
                    print(f"Test Case created successfully: {test_case}")
                else:
                    print(f"Error: {response.status_code}")
                    print(response.json())



add_section()