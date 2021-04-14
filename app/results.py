import sqlite3
import json
class Results:

    def __init__(self):
        self.db = sqlite3.connect('results.db')
        self.create_results()

    def get_absolute_party(self, vote_share):
        count = 0
        for vote in vote_share:
            if vote > 0.05:
                count = count + 1
        return count

    def get_absolute_party_result(self, run_id): #return dict 1,2 3
        absolute_parties = [0, 0, 0, 0] #not modular for 4 parties
        no_rounds = 1000 #need to store this in db really!!!!!
        run = self.db.execute('''select id, level, no_of_agents, no_of_parties
                              from run where id = ?''', (run_id,)).fetchone()

        rounds = self.db.execute('''select vote_share
                                 from round where run_id = ?''', (run_id,))
        for round_row in rounds:
            abs_parties = self.get_absolute_party(vote_share=map(float, json.loads(round_row[0])))
            absolute_parties[abs_parties] = absolute_parties[abs_parties] + 1
        absolute_party_percentage = [round(int(count) / no_rounds, 2) for count in absolute_parties]

        #print('Run: ' + str(run[0]) + ' level: ' + str(run[1]))
        print('Absolute Number of parties:')
        print('1: ' + str(absolute_party_percentage[1]))
        print('2: ' + str(absolute_party_percentage[2]))
        print('3: ' + str(absolute_party_percentage[3]))

    def insert_round(self, row, run_id):
        vote_share = str(row['vote_share'])
        vote_count = str(row['vote_count'])
        self.db.execute('''insert into round (vote_share, vote_count, run_id)
                        values (?, ?, ?)''', (vote_share, vote_count, run_id))
        self.db.commit()

    def insert_run(self, row):
        level = row['level']
        no_of_agents = row['no_of_agents']
        no_of_parties = row['no_of_parties']
        row_id = self.db.execute('''insert into run (level, no_of_agents, no_of_parties)
                                 values (?, ?, ?)''', (level, no_of_agents, no_of_parties)).lastrowid
        self.db.commit()
        return row_id


    def create_run_table(self):
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='run'")
        if select.fetchone()[0] == 0:
            print('Table does not exist')
            self.db.execute('''create table run
                            (id number primary key,
                             level number,
                             no_of_agents number,
                             no_of_parties number
                            );''')
        else:
            print('Table exists')

    def create_round_table(self):
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='round'")
        if select.fetchone()[0] == 0:
            print('Table does not exist') #could make an election table but not extensible with number of parties unknown
            self.db.execute('''create table round
                            (id number primary key,
                             vote_share text,
                             vote_count text,
                             run_id number not null,
                             foreign key (run_id) references run (id)
                            );''')
        else:
            print('Table exists')

    def create_results(self):
        self.create_run_table()
        self.create_round_table()

if __name__ == '__main__':
    results = Results()
    results.get_absolute_party_result(run_id=1)
    #results.db.execute('drop table run')
    #results.db.execute('drop table round')
    #results.db.commit()
    #DROP TABLES AND DO ABS ETC
