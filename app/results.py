import sqlite3
import json
class Results:

    def __init__(self):
        self.db = sqlite3.connect('results.db')
        self.create_results()

    #Stat methods
    def get_strat_vote_percentage(self, agent):

        count = 0
        for voter in agent:
            if voter.pure_vote_id != voter.previous_vote_id:
                count = count + 1
        return (count / len(agent))

    def get_vote_count(self, agent):
        votes = [0, 0, 0]
        for voter in agent:
            votes[voter.previous_vote_id] = votes[voter.previous_vote_id] + 1
        return votes

    def get_vote_share(self, agent):
        votes = [0, 0, 0]
        for voter in agent:
            votes[voter.previous_vote_id] = votes[voter.previous_vote_id] + 1
        distribution = [round(vote / len(agent), 2) for vote in votes]
        return distribution

    def get_absolute_party(self, vote_share):
        count = 0
        for vote in vote_share:
            if vote > 0.05:
                count = count + 1
        return count

    def print_results(self, run_id):
        self.get_absolute_party_result(run_id=run_id)
        self.get_strat_vote_percentage(run_id=run_id)

    def get_absolute_party_result(self, run_id): #return dict 1,2 3
        absolute_parties = [0, 0, 0, 0] #not modular for 4 parties
        no_rounds = 1 #need to store this in db really!!!!!
        run = self.db.execute('''select id, level, no_of_agents, no_of_parties
                              from run where id = ?''', (run_id,)).fetchone()

        rounds = self.db.execute('''select vote_share
                                 from round where run_id = ?''', (run_id,))
        for round_row in rounds:
            abs_parties = self.get_absolute_party(vote_share=map(float, json.loads(round_row[0])))
            absolute_parties[abs_parties] = absolute_parties[abs_parties] + 1
        absolute_party_percentage = [round(int(count) / no_rounds, 2) for count in absolute_parties]

        print('Run: ' + str(run[0]) + ' level: ' + str(run[1]))
        print('Absolute Number of parties:')
        print('1: ' + str(absolute_party_percentage[1]))
        print('2: ' + str(absolute_party_percentage[2]))
        print('3: ' + str(absolute_party_percentage[3]))

    def insert_round(self, objects, run_id):
        #proccess stats from objects
        agent = objects[0]
        vote_count = str(self.get_vote_count(agent=agent))
        vote_share = str(self.get_vote_share(agent=agent))
        strat_percentage = str(self.get_strat_vote_percentage(agent=agent))

        print(vote_share)

        #insert row
        self.db.execute('''insert into round (vote_share, vote_count, strategic_vote_percentage, run_id)
                        values (?, ?, ?, ?)''', (vote_share, vote_count, strat_percentage, run_id))
        self.db.commit()

    #Table methods
    def insert_mode(self, parameters):
        id = parameters['id']
        level = parameters['level']
        no_agent = parameters['no_agent']
        no_party = parameters['no_party']
        no_round = parameters['rounds']
        no_election = parameters['elections'] #make consistent with no_ !

        self.db.execute('''insert into mode (id, level, no_agent, no_party, no_round, no_election)
                                values (?, ?, ?, ?, ?, ?)''', (id, level, no_agent, no_party, no_round, no_election))
        self.db.commit()

    def insert_run(self, parameters):
        #If parameter mode doesn't exist, create it.
        mode_id = int(parameters['id'])
        select = self.db.execute('''select count(*) from mode where id = ?''', (mode_id,))
        if select.fetchone()[0] == 0:
            self.insert_mode(parameters=parameters)

        #insert run and return it's id
        row_id = self.db.execute('''insert into run (mode_id)
                                 values (?)''', (mode_id,)).lastrowid
        self.db.commit()
        return row_id

    def create_mode_table(self): #no_round is redundnat but still justified. No seperate round level parameters1
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='mode'")
        if select.fetchone()[0] == 0:
            self.db.execute('''create table mode
                            (id integer primary key,
                             level number,
                             no_agent number,
                             no_party number,
                             no_round number,
                             no_election number           
                            );''')

    def create_run_table(self):
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='run'")
        if select.fetchone()[0] == 0:
            self.db.execute('''create table run
                            (id integer primary key,
                             mode_id integer not null,
                             foreign key (mode_id) references mode (id)
                            );''')

    def create_round_table(self):
        select = self.db.execute("select count(*) from sqlite_master where type='table' and name='round'")
        if select.fetchone()[0] == 0: #could make an election table but not extensible with number of parties unknown
            self.db.execute('''create table round
                            (id integer primary key,
                             vote_share text,
                             vote_count text,
                             strategic_vote_percentage text,
                             run_id integer not null,
                             foreign key (run_id) references run (id)
                            );''')

    def create_results(self):
        self.create_mode_table()
        self.create_run_table()
        self.create_round_table()

#if __name__ == '__main__':
    #results = Results()
    #results.get_absolute_party_result(run_id=1)

