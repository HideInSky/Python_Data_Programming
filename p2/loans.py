import csv
import json
from zipfile import ZipFile
from io import TextIOWrapper

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
    }
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup.keys():
                self.race.add(race_lookup[r])
    def __repr__(self):
        return f'Applicant({repr(self.age)}, {repr(list(self.race))})'
    def lower_age(self):
        temp = self.age.replace('<', '-')
        temp = temp.replace('>', '-')
        l = temp.split('-')
        if l[0]:
            return int(l[0])
        return int(l[1])
    def __lt__(self, other):
        if (self.lower_age() < other.lower_age()):
            return True
        else:
            return False

        
class Loan:
    def __init__(self, values):
        # loan_amount; property_value; interest_rate; applicants
        try:
            self.loan_amount = float(values["loan_amount"])
        except ValueError:
            self.loan_amount = -1
        try:
            self.property_value = float(values["property_value"])
        except ValueError:
            self.property_value = -1
        try:
            self.interest_rate = float(values["interest_rate"])
        except ValueError:
            self.interest_rate = -1
            
        self.applicants = []
        applicant1_race = []
        applicant1_age = values["applicant_age"]
        for key in values.keys():
            if (key[:15] == "applicant_race-"):
                if (values[key]):
                    applicant1_race.append(values[key])
        applicant1 = Applicant(applicant1_age, applicant1_race)
        self.applicants.append(applicant1)
        
        if (values["co-applicant_age"] != "9999"):
            applicant2_age = values["co-applicant_age"]
            applicant2_race = []
            for key in values.keys():
                if (key[:18] == "co-applicant_race-"):
                    if (values[key]):
                        applicant2_race.append(values[key])
            applicant2 = Applicant(applicant2_age, applicant2_race)
            self.applicants.append(applicant2)
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    def yearly_amounts(self, yearly_payment):
        assert self.interest_rate > 0 and self.loan_amount > 0
        result = []
        amt = self.loan_amount
        while amt > 0:
            yield amt
            amt = amt * (1 + self.interest_rate/100)
            amt -= yearly_payment
        return result

class Bank():
    def __init__(self, name):
        with open("banks.json", "r") as f:
            d = json.load(f)
            for i in d:
                if i["name"] == name:
                    self.lei = i["lei"]
        self.loans_lib = []
        with ZipFile('wi.zip') as zf:
            csv_file = zf.namelist()[0]
             # adapted from https://docs.python.org/3/library/csv.html#csv.DictReader
            with zf.open(csv_file, 'r') as f:
                reader = csv.DictReader(TextIOWrapper(f))
                for row in reader:
                    if self.lei == row["lei"]:
                        self.loans_lib.append(Loan(row))

    def __getitem__(self, lookup):
        return self.loans_lib[lookup]
    
    def __len__(self):
        return len(self.loans_lib)
                               
                
        
