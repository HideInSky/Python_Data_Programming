# project: p7
# submitter: lin364@wisc.edu
# partner: None
# hours: 2

from sklearn.linear_model import LogisticRegression

class UserPredictor:
    def __init__(self):
        self.users = None
        self.logs = None
        self.model = LogisticRegression(fit_intercept=False)
        self.cols = ['age', 'past_purchase_amt', 'keyboard_secs', 'keyboard_times', 'total_secs']

    def reformat(self):
        length = len(self.users)
        
        keyboard_secs = [0] * length
        keyboard_times = [0] * length
        total_secs = [0] * length
        
        first_id = int(self.users.at[0, 'user_id'])
        
        for idx, row in self.logs.iterrows():
            url = row['url']
            user_id = row['user_id']
            
            total_secs[user_id - first_id] += row['seconds']
            if url != '/keyboard.html':
                continue
            seconds = row['seconds']
            keyboard_times[user_id - first_id] += 1
            keyboard_secs[user_id - first_id] += seconds
            
        
        self.users['keyboard_secs'] = keyboard_secs
        self.users['keyboard_times'] = keyboard_times 
        self.users['total_secs'] = total_secs
        
        
    def fit(self, users, logs, y):
        self.users = users
        self.logs = logs
        
        self.reformat()
        self.model.fit(self.users[self.cols], y['y'])
        
    def predict(self, test_users, test_logs):
        self.users = test_users
        self.logs = test_logs
        
        self.reformat()
        return self.model.predict(self.users[self.cols])