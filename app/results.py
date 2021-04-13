import sqlite3
class Results:
    def __init__(self):
        self.db = sqlite3.connect('results.db')

    def create_run_table(self):
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='run'")
        if select.fetchone()[0] == 0:
            print('Table does not exist')
            self.db.execute('''create table run
                            (id number primary key not null,
                             level number,
                             no_of_agents number,
                             no_of_parties number
                            );''')
        else:
            print('Table exists')

    #def create_results(self): #standard interface

if __name__ == '__main__':
    results = Results()
    results.create_run_table()