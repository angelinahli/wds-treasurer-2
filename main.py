"""
FILENAME: main.py
DESC: Contains all classes needed to send forms
AUTHOR: Angelina Li
DATE: 01/03/17
"""

import json

import config.user_info as usr
from config.gsheets import client

# --- Main classes --- #

class Reimbursement:
    """
    Represents one reimbursement that has yet to be processed.
    """

    def __init__(self, username, date, event_name, purpose, amount, 
            num_attendees, other_students=None, notes=None, receipt=None):
        self.username = username
        self.date = date
        self.event_name = event_name
        self.purpose = purpose
        self.amount = float(amount)
        self.num_attendees = int(num_attendees)
        self.other_students = other_students
        self.notes = notes
        self.receipt = receipt

        self.account = usr.get_account(self.purpose)
        self.event = self._get_formatted_event()

    @classmethod
    def from_dict(cls, param_dict):
        """
        Create an object of this class using parameters taken from a dictionary.
        Idea from this SO thread: https://stackoverflow.com/questions/30113723/
        creating-class-instance-from-dictionary
        """
        allowed_keys = ["username", "date", "event_name", "purpose", "amount",
            "num_attendees", "other_students", "notes", "receipt"]
        allowed_params = {k: v for k, v in param_dict if k in allowed_keys}
        return cls(**allowed_params)

    def get_additional_notes(self, user_data):
        """
        Will return a string representing any additional notes that should be 
        created for this reimbursement.
        user_data: dct like obj containing all data for all users sorted by 
        username.
        """
        add_notes = []
        if self.num_attendees > 0 and self.other_students:
            add_notes.append(self._get_usernames(user_data))
        if self.notes:
            add_notes.append(self._get_notes())

        if any(add_notes):
            return "NOTES FOR EVENT {header}:\n{body}".format(
                header=self.event, 
                body="\n".join(add_notes))
        else:
            return ""

    def _get_usernames(self, user_data):
        """
        The user __str__ method should return:
        "{username}, class year: {class_year}, banner id: {id}"
        """
        msg = ["The following students were paid for with this reimbursement:"]
        if self.username not in self.other_students:
            msg.append(str(user_data.get(self.username, "USER NOT FOUND")))
        for student in self.other_students:
            msg.append(str(user_data.get(student, "USER NOT FOUND")))
        return "\n".join(msg)

    def _get_notes(self):
        return "Additional notes\n" + self.notes

    def _get_formatted_event(self):
        """
        Return an event formatted the way SOFC wants it:
        event name; date of event; # attendees; amount; fund account
        """
        return "{name}; {date}; {num_attendees}; {amt}; {account}".format(
            name=self.event_name,
            date=self.date,
            num_attendees=self.num_attendees,
            amt=self.amount,
            account=self.account)

class User:
    """
    Represents one member of our club (who could potentially have filed for a 
    reimbursement).
    """

    def __init__(self, username, name, unit_box, banner_id, year):
        self.username = username
        self.name = name
        self.unit_box = unit_box
        self.banner_id = banner_id
        self.year = int(year)

        self.address = usr.get_student_address(self.unit_box)

    def __str__(self):
        return "{username}, class year: {year}, banner id: {id}".format(
            username=self.username,
            year=self.year,
            id=self.banner_id)

    @classmethod
    def from_dict(cls, param_dict):
        allowed_keys = ["username", "unit_box", "banner_id", "year"]
        allowed_params = {k: v for k, v in param_dict if k in allowed_keys}
        return cls(**allowed_params)

class Sheet:
    """
    Represents one google sheet full of data.
    """

    def __init__(self, url, cols, start_row):
        """
        url (string): the URL of a google sheet
        col_indices (dict): a dictionary of the worksheets column names and
        their google sheets column indices
        start_row (int): the google sheets row index where the first line of
        data starts
        """
        self.url = url
        self.col_indices = cols
        self.start_row = start_row

        self.ws = client.open_by_url(self.url).sheet1
        self.data_indices = self._get_data_indices()

    def get_range(self):
        return range(self.start_row, self.ws.row_count)

    def get_cell_data(self, row_num, col_name):
        return self.ws.cell(row_num, self.col_indices[col_name])

    def get_row_data_dict(self, row_num):
        row_data = self._get_row_data(row_num)
        return {var: row_data[i] for var, i in self.data_indices.items()}

    def _get_data_indices(self):
        """
        Returns new dictionary mapping column names to the indices of a list of
        row data instead of google sheets column indices.
        """
        return {col: i - 1 for col, i in self.col_indices.items()}

    def _get_row_data(self, row_num):
        return self.ws.row_values(row_num)

class Form:

    org_name = usr.ORG_NAME
    sofc_num = usr.SOFC_FUND_NUM
    profits_num = usr.PROFITS_FUND_NUM
    clce_amt = 0

    def __init__(self, processed_by, name, banner_id, address, events, purposes, 
            sofc_amt, profits_amt, total_amt, additional_notes):
        self.processed_by = processed_by
        self.name = name
        self.banner_id = banner_id
        self.address = address
        self.sofc_amt = sofc_amt
        self.profits_amt = profits_amt
        self.total_amt = total_amt
        self.events = "\n".join(events)
        self.purposes = ", ".join(purposes)
        self.additional_notes = "\n".join(additional_notes)

    def __str__(self):
        msg = """{decorator}
            Name: {processed_by}
            Organization name: {org_name}
            SOFC fund number: {sofc_num}
            Profits fund number: {profits_num}
            Student or outside vendor? STUDENT
            Name of student or vendor? {name}
            B Number: {banner_id}
            Address: {address}
            
            Events:
            {events}

            Reason for reimbursement: {purposes}
            Amount requesting from SOFC: {sofc_amt}
            Amount requesting from profits: {profits_amt}
            Amount requesting from CLCE: {clce_amt}
            
            Additional notes to add:
            {additional_notes}
            {decorator}""".format(
                decorator="~~~~~~~~~~~~~~~", **vars(self)).replace("  ", "")
        return msg

    @classmethod
    def from_user_reimbursements(cls, processed_by, user, reimbursements, 
            user_data):
        """
        Constructs an instance of this class from a User and a list of all
        Reimbursements associated with this User.
        """
        params = {
            "processed_by": processed_by,
            "name": user.name,
            "banner_id": user.banner_id,
            "address": user.address,
            "events": [],
            "purposes": [],
            "sofc_amt": 0,
            "profits_amt": 0,
            "total_amt": 0,
            "additional_notes": []
        }

        has_missing_account = False
        for rmb in reimbursements:
            params["events"].append(rmb.event)
            params["purposes"].append(rmb.purpose)
            params["additional_notes"].append(
                rmb.get_additional_notes(user_data))

            if rmb.account == "SOFC":
                params["sofc_amt"] += rmb.amount
            elif rmb.account == "PROFITS":
                params["profits_amt"] += rmb.amount
            else:
                has_missing_account = True
            
            params["total_amt"] += rmb.amount
        if has_missing_account:
            warning = "WARNING: SOME ACCOUNT INFO IS MISSING"
            params["additional_notes"].insert(0, warning)
        return cls(**params)

# --- Helper functions --- #

# user data

def get_users_data_from_sheet():
    """
    Generates a dictionary of dictionaries where each key is a username and
    each value is a dictionary of all the information associated with this user
    """
    users_sheet = Sheet(**usr.users_sheet)
    users_dict = dict()

    for row_num in users_sheet.get_range():
        username = users_sheet.get_cell_data(row_num, "username")
        if not bool(username):
            break
        user_info = users_sheet.get_row_data_dict(row_num)
        users_dict[username] = user_info

    return users_dict

def save_users_data(filepath, users_data):
    """
    Saves users data for storage.
    """
    with open(filepath, "w") as storage:
        json.dump(users_data, storage)

def get_users_data_from_file(filepath):
    with open(filepath, "r") as storage:
        return json.load(storage)

def get_users_data(download=False):
    """
    download: if download = True, data is downloaded from the Google sheet and
    the storage data is refreshed.
    """
    storage_filepath = usr.USERS_DATA
    if download:
        users_dicts = get_users_data_from_sheet()
        save_users_data(storage_filepath, users_dicts)
    else:
        users_dicts = get_users_data_from_file(storage_filepath)
    return {key: User.from_dict(val) for key, val in users_dicts.items()}

# reimbursement data

def get_reimbursement_data():
    pass