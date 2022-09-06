from datetime import datetime, date

class Task():
    def __init__(self, name, done, notes, recurring,star,tags,date_started=None,date_to_do=None,last_done="2020-01-01",recurring_type=None,recurring_value=None):
        self.name = name
        self.done = done
        self.last_done = datetime.strptime(last_done,"%Y-%m-%d").date()
        self.notes = notes
        self.recurring = recurring
        self.recurring_type = recurring_type
        self.recurring_value = recurring_value
        self.date_created = date.today()
        if date_started:
            self.date_started = datetime.strptime(date_started,"%Y-%m-%d").date()  
        else:
            self.date_started = date.today()
        if date_to_do:
            self.date_to_do = datetime.strptime(date_to_do,"%Y-%m-%d").date()
        else:
            self.date_to_do = date.today()

        self.star = star
        self.tags = tags

