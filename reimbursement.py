"""
FILENAME: reimbursement.py
DESC: Contains class representing Reimbursement objects
AUTHOR: Angelina Li
DATE: 01/03/17
"""

import config.user_info as usr

class Reimbursement:
    """
    Represents one reimbursement that has yet to be processed
    """

    def __init__(self, username, date, event_name, purpose, amount, 
            num_attendees, other_students=None, notes=None, receipt=None,  
            processed_by=None):
        self.username = username
        self.date = date
        self.event_name = event_name
        self.purpose = purpose
        self.amount = float(amount)
        self.num_attendees = int(num_attendees)
        self.other_students = other_students
        self.notes = notes
        self.receipt = receipt
        self.processed_by = processed_by

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
            "num_attendees", "other_students", "notes", "receipt", 
            "processed_by"]
        allowed_params = {k: v for k, v in param_dict if k in allowed_keys}
        return cls(**allowed_params)

    def get_additional_notes(self, user_data):
        """
        Will return a string representing any additional notes that should be 
        created for this reimbursement.
        user_data: an obj that contains a .get() method to get data for a
        specific user given their username.
        """
        notes = []
        if self.num_attendees > 0 and self.other_students:
            notes.append(self._get_usernames(user_data))
        if self.notes:
            notes.append(self._get_notes())

    def _get_usernames(self, user_data):
        """
        The user __str__ method should return:
        "{username}, class year: {class_year}, banner id: {id}"
        """
        msg = ["The following students were paid for with this reimbursement:"]
        if self.username not in self.other_students:
            msg.append(str(user_data.get(self.username)))
        for student in self.other_students:
            msg.append(str(user_data.get(student)))
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
                account=self.account
            )