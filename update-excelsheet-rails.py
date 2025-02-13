import base64
import json

import pandas as pd

import requests


project_id = "50"
test_rail_instance = "https://trail.paloaltonetworks.local/index.php?/api/v2"
get_section_data = f'{test_rail_instance}/get_sections'
get_test_case_url = f'{test_rail_instance}/get_section'
update_case = f'{test_rail_instance}/update_case'
get_case = f'{test_rail_instance}/get_case'
add_case = f'{test_rail_instance}/add_case'
username = "sahkumar@paloaltonetworks.com"
api_key = "AUYcvqeZfzBHaepgLVyS-8tQflvk1CPz3XaCLGzW/"
credentials = base64.b64encode(f"{username}:{api_key}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {credentials}"
}
sections_url = f"{test_rail_instance}/index.php?/api/v2/get_sections/{project_id}"

test_type = {
"Sanity": 21,
 "Regression": 9,
    "Customer Issues": 26
}

test_priority = {
    "Critical": 4,
    "Medium": 2
}

test_sheet = "/Users/sahkumar/Downloads/output.xlsx"

def get_sections_id():
    url = f"{get_section_data}/{project_id}"
    result_response = requests.get(
        url,
        headers=headers
    )
    tests_mapping = {}
    # Check if the status get was successful
    if result_response.status_code == 200:
        print(f"Successfully fetched sections.")
    else:
        print(
            f"Failed to fetch sections. Status code: {result_response.status_code}, "
            f"Message: {result_response.text}")

    for sections in result_response.json():
        tests_mapping[sections['name']] = sections['id']

    return tests_mapping


def fetch_test_cases(test_id):
    # Make the GET request to fetch the test case
    url = f"{get_case}/{test_id}"
    result_response = requests.get(
        url,
        headers=headers
    )

    # Check if the status get was successful
    if result_response.status_code == 200:
        print(f"Successfully fetched test case ID {test_id}.")
    else:
        print(
            f"Failed to update test case ID {test_id}. Status code: {result_response.status_code}, "
            f"Message: {result_response.text}")
    return result_response.json()


def update_test_data(row, section):
    # data = {
    #     "title": "Verify AWS S3 connector onboarding.",
    #     "section_id": 127643,
    #     "priority_id": 4,
    #     "display_order": 1,
    #     "type_id": 21,
    #     "custom_objective": "Verify AWS S3 connector onboarding and enable scanning.",
    #     "custom_steps": "Onboard a AWS S3 connector in SCM Data Security UI",
    #     "custom_expected": "AWS S3 connector should be onboarded successfully",
    # }
    data = {}
    test_id = row.ID.replace('C', '')
    response = fetch_test_cases(test_id)
    if not pd.isnull(row.Title):
        data['title'] = str(row.Title)
    if not pd.isnull(row.Steps):
        data['custom_steps'] = str(row.Steps)
    if not pd.isnull(row["Expected Result"]):
        data['custom_expected'] = str(row["Expected Result"])
    if not pd.isnull(row["Priority"]):
        data['priority_id'] = test_priority[str(row["Priority"])]
    if not pd.isnull(row["Type"]):
        data['type_id'] = test_type[str(row["Type"])]
    url = f"{update_case}/{test_id}"
    print(f"updating test data {data}")
    result_response = requests.post(url, headers=headers, data=json.dumps(data))
    # Check if the status get was successful
    if result_response.status_code == 200:
        print(f"Successfully updated test case ID {test_id}.")
    else:
        print(
            f"Failed to update test case ID {test_id}. Status code: {result_response.status_code}, "
            f"Message: {result_response.text}")


def create_test_case(row, section):
    data = {
        "title": str(row.Title),
        "section_id": section,
        "type_id": test_type[str(row['Type'])],
        "priority_id": test_priority[str(row["Priority"])],
        "custom_steps":  str(row.Steps),
        "custom_expected": str(row["Expected Result"]),
        "custom_objective": str(row.Title),
    }
    print(f"creating test data {data}")
    url = f"{add_case}/{section}"
    result_response = requests.post(url, headers=headers, data=json.dumps(data))
    # Check if the status get was successful
    if result_response.status_code == 200:
        print(f"Successfully updated test case ID {result_response.json()['id']}.")
    else:
        print(
            f"Failed to create test case. Status code: {result_response.status_code}, "
            f"Message: {result_response.text}")



def fetch_data(row, section):
    print(row["Title"])
    if not pd.isnull(row.ID):
        update_test_data(row, section)
    else:
        create_test_case(row, section)


def read_test_sheet(test_mapping):
    excel_file = pd.ExcelFile(test_sheet)
    sheet_names = ["citrix share file"]
    # Iterate over each sheet in the Excel file
    # for sheet_name in excel_file.sheet_names:
    for sheet_name in sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Print the sheet name
        print(f"Sheet name: {sheet_name}")

        # Print the first few rows of the DataFrame
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            fetch_data(row, test_mapping[sheet_name])

        # You can also save the DataFrame to a CSV file if needed
        # df.to_csv(f'{sheet_name}.csv', index=False)

        # Add any additional processing logic here


test_mapping = get_sections_id()

read_test_sheet(test_mapping)