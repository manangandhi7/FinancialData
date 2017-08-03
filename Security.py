import csv
import os
import pandas


class Security:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.face_value = 0.0
        self.number_of_shares = 0.0
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\play_data\TCS.csv'), 'r') as f:
            self.history_data = [row for row in csv.reader(f) if row[0] != '']
        #print 'new sec initialized!'

    #id = ""
    name = ""
    face_value = 0.0
    number_of_shares = 0.0

    def get_history_data(self):
        return self.history_data

if __name__ == '__main__':
    security = Security()
    print(security.get_history_data())
