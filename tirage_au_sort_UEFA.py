import random
import numpy as np
import csv
import random as rd


teams = [[{"club": "ManCity", "nationality": "England"},
          {"club": "Bayern", "nationality": "Germany"},
          {"club": "Liverpool", "nationality": "England"},
          {"club": "Real", "nationality": "Spain"},
          {"club": "PSG", "nationality": "France"}, 
          {"club": "ManUnited", "nationality": "England"},
          {"club": "Barcelona", "nationality": "Spain"},
          {"club": "Inter", "nationality": "Italy"},
          {"club": "Sevilla", "nationality": "Spain"}],
         [{"club": "Dortmund", "nationality": "Germany"},
          {"club": "Atletico", "nationality": "Spain"},
          {"club": "Leipzig", "nationality": "Germany"},
          {"club": "Benfica", "nationality": "Portugal"},
          {"club": "Napoli", "nationality": "Italy"},
          {"club": "Porto", "nationality": "Portugal"},
          {"club": "Arsenal", "nationality": "England"},
          {"club": "Shakhtar", "nationality": "Ukraine"},
          {"club": "Salzburg", "nationality": "Austria"}],
         [{"club": "Atalanta", "nationality": "Italy"},
          {"club": "Feyenoord", "nationality": "Netherlands"},
          {"club": "Milan", "nationality": "Italy"},
          {"club": "Braga", "nationality": "Portugal"},
          {"club": "Eindhoven", "nationality": "Netherlands"},
          {"club": "Lazio", "nationality": "Italy"},
          {"club": "Crvena", "nationality": "Serbia"},
          {"club": "Copenhagen", "nationality": "Denmark"},
          {"club": "YB", "nationality": "Switzerland"}],
          [{"club": "Sociedad", "nationality": "Spain"},
           {"club": "Marseille", "nationality": "France"},
           {"club": "Galatasaray", "nationality": "Turkey"},
           {"club": "Celtic", "nationality": "Scotland"},
           {"club": "Qarabag", "nationality": "Azerbaijan"},
           {"club": "Newcastle", "nationality": "England"},
           {"club": "Berlin", "nationality": "Germany"},
           {"club": "Antwerp", "nationality": "Belgium"},
           {"club": "Lens", "nationality": "France"}]]


def init_graph(): 
    '''Renvoie la matrice de taille 36x36 avec None si le match est
       possible et 0 s'il est impossible (même nationalité et diagonale)'''
    graph = np.array([[None for _ in range(36)] for _ in range(36)])
    np.fill_diagonal(graph, 0)
    for pot in range(4):
        for i in range(9):
            team = teams[pot][i]
            for opponent_pot in range(4):
                for opponent_i in range(9):
                    opponent_team = teams[opponent_pot][opponent_i]
                    if team["nationality"] == opponent_team["nationality"]:
                        graph[9*pot+i, 9*opponent_pot+opponent_i] = 0
    return graph


def write_to_csv(matches):
    with open("tirage_au_sort_1.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for match in matches:
            writer.writerow(match)


def block_is_fillable(graph, pot, opponent_pot):
    '''Regarde si le bloc (pot, opponent_pot) et (opponent_pot, pot) est remplissable
       avec un 1 par ligne et 1 un par colonne''' 
    def aux(graph, i):
        '''Fontion récursive qui vérifie si on peut remplir à partir de la ligne i'''
        if i==9:
            return True
        else:
            home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != 0]
            away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != 0]
            possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
            for (home, away) in possible_matches:
                new_graph = np.copy(graph)
                new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
                new_graph[9*opponent_pot+home, 9*pot+i] = 0 # no return
                for k in range(9):
                    if k != home:
                        new_graph[9*pot+i, 9*opponent_pot+k] = 0 
                    if k != i:
                        new_graph[9*pot+k, 9*opponent_pot+home] = 0
                new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
                new_graph[9*pot+i, 9*opponent_pot+away] = 0 # no return
                for k in range(9):
                    if k != away:
                        new_graph[9*opponent_pot+k, 9*pot+i] = 0
                    if k != i:
                        new_graph[9*opponent_pot+away, 9*pot+k] = 0
                if aux(graph, i+1):
                    return True
            return False
    return aux(graph, 0)


def is_fillable(graph):
    for pot in range(4):
        for opponent_pot in range(4):
            if not block_is_fillable(graph, pot, opponent_pot):
                return False
    return True


def all_matches(graph, pot, i, opponent_pot): 
    '''Retourne l'ensemble des matchs possibles entre l'équipe (pot, i) et les 
    équipes du pot opponent_pot en vérifiant récursivement qu'on peut compléter la matrice'''
    home_opponents = [j for j in range(9) if graph[9*pot+i, 9*opponent_pot+j] != 0]
    away_opponents = [j for j in range(9) if graph[9*opponent_pot+j, 9*pot+i] != 0]
    possible_matches = [(x, y) for x in home_opponents for y in away_opponents if x != y]
    true_matches = []
    for (home, away) in possible_matches:
        new_graph = np.copy(graph)
        new_graph[9*pot+i, 9*opponent_pot+home] = 1 # home match
        new_graph[9*opponent_pot+home, 9*pot+i] = 0 # no return
        for k in range(9):
            if k != home:
                new_graph[9*pot+i, 9*opponent_pot+k] = 0
            if k != i:
                new_graph[9*pot+k, 9*opponent_pot+home] = 0
        new_graph[9*opponent_pot+away, 9*pot+i] = 1 # away match
        new_graph[9*pot+i, 9*opponent_pot+away] = 0 # no return
        for k in range(9):
            if k != away:
                new_graph[9*opponent_pot+k, 9*pot+i] = 0
            if k != i:
                new_graph[9*opponent_pot+away, 9*pot+k] = 0
        if is_fillable(new_graph):
            true_matches.append((home, away))
    return true_matches
    

def tirage_au_sort(graph):
    '''Effectue le tirage au sort'''
    matches_list = []
    for pot in range(4):
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        rd.shuffle(indices)
        for i in indices:
            opponents = [teams[pot][i]["club"]]
            for opponent_pot in range(4):
                (home, away) = random.choice(all_matches(graph, pot, i, opponent_pot))
                graph[9*pot+i, 9*opponent_pot+home] = 1
                graph[9*opponent_pot+home, 9*pot+i] = 0
                for k in range(9):
                    if k != home:
                        graph[9*pot+i, 9*opponent_pot+k] = 0
                    if k != i:
                        graph[9*pot+k, 9*opponent_pot+home] = 0
                graph[9*opponent_pot+away, 9*pot+i] = 1
                graph[9*pot+i, 9*opponent_pot+away] = 0
                for k in range(9):
                    if k != away:
                        graph[9*opponent_pot+k, 9*pot+i] = 0
                    if k != i:
                        graph[9*opponent_pot+away, 9*pot+k] = 0
                opponents.append((teams[opponent_pot][home]["club"], teams[opponent_pot][away]["club"]))
            print(opponents)
            matches_list.append(opponents)
    write_to_csv(matches_list)
    print("CSV file 'tirage_au_sort_1.csv' has been generated successfully.")


graph = init_graph()
tirage_au_sort(graph)
