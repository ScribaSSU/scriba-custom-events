import requests

def get_departments_list():
    departments = {}

    link = "https://scribabot.ml/api/v1.0/departments"
    for department in requests.get(link).json()["departmentsList"]:
        departments[department["url"]] = (department["fullName"], department["shortName"])

    return departments

def get_schedule(department, group_number):
    link = "https://scribabot.ml/api/v1.0/schedule/full/" + \
           f"{department}/{group_number}"
    return requests.get(link).json()["lessons"]