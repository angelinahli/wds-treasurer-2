"""
FILENAME: sensitive_info.py
DESC: File containing non-sensitive data needed for my program.
    Imports some data from sensitive_info:
    - get_student_address(unit_box): returns string with address
    
    - SOFC_FUND_NUM
    - PROFITS_FUND_NUM
    
    - FORM_URL: Url for form that needs to be filled in for each reimbursement
    - RMBS_URL: Url for sheet containing all reimbursement details
    - USERS_URL: Url for sheet containing all user information
    - OVERALL_URL: Url for sheet containing overall information about club finances
    
    - EMAIL_LOGIN: Login information for email used to send the user form info
    - EMAIL_PASSWORD: Password for email used to send the user form info
AUTHOR: Angelina Li
DATE: 01/03/18
"""

from sensitive_info import *

reimbursement_sheet = {
    "url": RMBS_URL,
    "start_row": 3,
    "cols": {
        "timestamp": 1,
        "username": 3,
        "date": 4,
        "event_name": 5,
        "purpose": 6,
        "amount": 7,
        "num_attendees": 8,
        "other_students": 9,
        "notes": 11,
        "receipt": 12,
        "is_done": 13,
        "processed_by": 14
    }
}

user_sheet = {
    "url": USERS_URL,
    "start_row": 2,
    "cols": {
        "unit_box": 1,
        "name": 2,
        "banner_id": 3,
        "username": 4
    }
}

# for each potential account lists rmbs purposes associated with this account
# here so this can be changed easily.
ACCOUNT_PURPOSES: {
    "SOFC": ["Senate bus token", "Transportation (not bus token)"],
    "PROFITS": ["Food"]
}

def get_account(rmb_purpose):
    for account_name, purposes in ACCOUNT_PURPOSES.items():
        if rmb_purpose in purposes:
            return account_name
    return "N/A"