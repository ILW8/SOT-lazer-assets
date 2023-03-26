import csv
from collections import defaultdict
from pprint import pprint


class User:
    def __init__(self, user_name, user_id):
        self.user_name = user_name
        self.user_id = user_id

    def __str__(self):
        return f"{self.user_name} ({self.user_id})"

    def __repr__(self):
        return f"{self.user_name} ({self.user_id})"


class Team:
    def __init__(self, team_name: str, team_members: list, team_acronym=None):
        self.team_name: str = team_name
        self.team_members: list[User] = team_members
        self.team_acronym = team_acronym  # will normalize `None`s later

    def __str__(self):
        return f"{self.team_name} ({self.team_acronym}) [{', '.join(str(tm) for tm in self.team_members)}]"


class Teams:
    def __init__(self, teams = None):
        self.teams: list[Team] = teams if teams is not None else list()
        self.acronyms = dict()
        self.populate_team_acronyms()

    def __repr__(self):
        return f"[{', '.join([str(team) for team in self.teams])}]"

    def add_team(self, team: Team):
        self.teams.append(team)

    def populate_team_acronyms(self):
        for team in self.teams:
            if team.team_acronym is not None:
                self.acronyms[team.team_acronym] = team
                continue

            if len(team.team_name.split()) > 1:
                # generate acronym using first letter of each word
                tentative_acronym = "".join([word[0] for word in team.team_name.split()])
                if tentative_acronym in self.acronyms:
                    # pad with number until unique
                    counter = 0
                    new_acronym = tentative_acronym
                    while new_acronym in self.acronyms:
                        new_acronym = f"{tentative_acronym}{counter}"
                    tentative_acronym = new_acronym
                team.team_acronym = tentative_acronym
                self.acronyms[tentative_acronym] = team
                continue
            # else generate using first n letters
            # TODO: finish this
        pass


def build_bracket(teams: Teams):
    pass


def main():
    # parse team list
    data = defaultdict(lambda: defaultdict(list))  # key: team name, value: team data

    with open("./SOT Ref sheet - TeamsReal.csv", "r") as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            try:
                user_id = int(row[0])
                user_name = row[1]
                team_name = row[3]
                user = User(user_name, user_id)
                data[team_name]["user_name"].append(user)
            except ValueError:
                pass  # probably table header
    # pprint(data)

    teams = Teams()
    for team_name, team_data in data.items():
        teams.add_team(Team(team_name, team_data["user_name"]))
    teams.populate_team_acronyms()
    print(teams)


if __name__ == "__main__":
    main()
