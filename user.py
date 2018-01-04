"""
FILENAME: user.py
DESC: Contains class representing User objects
AUTHOR: Angelina Li
DATE: 01/03/17
"""

import config.user_info as usr

class User:

    def __init__(self, username, unit_box, banner_id, year):
        self.username = username
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