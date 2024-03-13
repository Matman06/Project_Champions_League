import networkx as nx
import matplotlib.pyplot as plt

# Données complètes des rencontres
rencontres=[
('1', 'A2', 'D8'),
('1', 'A4', 'B4'),
('1', 'A5', 'B6'),
('1', 'A7', 'C8'),
('1', 'A9', 'A1'),
('1', 'B3', 'C3'),
('1', 'B5', 'D4'),
('1', 'B7', 'A8'),
('1', 'B9', 'B1'),
('1', 'C2', 'A3'),
('1', 'C4', 'D6'),
('1', 'C7', 'A6'),
('1', 'C9', 'C1'),
('1', 'D2', 'C6'),
('1', 'D3', 'C5'),
('1', 'D5', 'B8'),
('1', 'D7', 'B2'),
('1', 'D9', 'D1'),
('2', 'A1', 'D5'),
('2', 'A3', 'A4'),
('2', 'A6', 'B3'),
('2', 'A8', 'B5'),
('2', 'B1', 'D9'),
('2', 'B2', 'C4'),
('2', 'B4', 'C2'),
('2', 'B6', 'D3'),
('2', 'B8', 'B9'),
('2', 'C1', 'A2'),
('2', 'C3', 'A5'),
('2', 'C5', 'A7'),
('2', 'C6', 'C7'),
('2', 'C8', 'D7'),
('2', 'D1', 'D2'),
('2', 'D4', 'A9'),
('2', 'D6', 'B7'),
('2', 'D8', 'C9'),
('3', 'A2', 'B1'),
('3', 'A5', 'A6'),
('3', 'A7', 'B8'),
('3', 'A9', 'B2'),
('3', 'B3', 'D6'),
('3', 'B5', 'B6'),
('3', 'B7', 'D1'),
('3', 'B9', 'C5'),
('3', 'C2', 'D8'),
('3', 'C4', 'A1'),
('3', 'C6', 'A8'),
('3', 'C7', 'C8'),
('3', 'C9', 'B4'),
('3', 'D2', 'A3'),
('3', 'D3', 'D4'),
('3', 'D5', 'C1'),
('3', 'D7', 'C3'),
('3', 'D9', 'A4'),
('4', 'A1', 'A2'),
('4', 'A3', 'B7'),
('4', 'A4', 'D7'),
('4', 'A6', 'D3'),
('4', 'A8', 'C7'),
('4', 'B1', 'C6'),
('4', 'B2', 'B3'),
('4', 'B4', 'A7'),
('4', 'B6', 'C9'),
('4', 'B8', 'D2'),
('4', 'C1', 'B9'),
('4', 'C3', 'C4'),
('4', 'C5', 'D9'),
('4', 'C8', 'A9'),
('4', 'D1', 'A5'),
('4', 'D4', 'D5'),
('4', 'D6', 'C2'),
('4', 'D8', 'B5'),
('5', 'A2', 'C3'),
('5', 'A5', 'D4'),
('5', 'A7', 'A8'),
('5', 'A9', 'D6'),
('5', 'B3', 'A1'),
('5', 'B5', 'C1'),
('5', 'B7', 'B8'),
('5', 'B9', 'A3'),
('5', 'C2', 'B6'),
('5', 'C4', 'C5'),
('5', 'C6', 'B2'),
('5', 'C7', 'D1'),
('5', 'C9', 'A4'),
('5', 'D2', 'B1'),
('5', 'D3', 'B4'),
('5', 'D5', 'A6'),
('5', 'D7', 'D8'),
('5', 'D9', 'C8'),
('6', 'A1', 'C6'),
('6', 'A3', 'D9'),
('6', 'A4', 'A5'),
('6', 'A6', 'C2'),
('6', 'A8', 'D2'),
('6', 'B1', 'A9'),
('6', 'B2', 'D5'),
('6', 'B4', 'B5'),
('6', 'B6', 'A2'),
('6', 'B8', 'C7'),
('6', 'C1', 'D3'),
('6', 'C3', 'B7'),
('6', 'C5', 'B3'),
('6', 'C8', 'C9'),
('6', 'D1', 'C4'),
('6', 'D4', 'B9'),
('6', 'D6', 'D7'),
('6', 'D8', 'A7'),
('7', 'A2', 'A3'),
('7', 'A5', 'C5'),
('7', 'A7', 'D1'),
('7', 'A9', 'C1'),
('7', 'B2', 'A4'),
('7', 'B3', 'B4'),
('7', 'B5', 'A6'),
('7', 'B7', 'C8'),
('7', 'B9', 'D8'),
('7', 'C2', 'C3'),
('7', 'C4', 'B8'),
('7', 'C6', 'D4'),
('7', 'C7', 'B1'),
('7', 'C9', 'D2'),
('7', 'D3', 'A1'),
('7', 'D5', 'D6'),
('7', 'D7', 'A8'),
('7', 'D9', 'B6'),
('8', 'A1', 'B9'),
('8', 'A3', 'C9'),
('8', 'A4', 'C4'),
('8', 'A6', 'A7'),
('8', 'A8', 'A9'),
('8', 'B1', 'B2'),
('8', 'B4', 'D7'),
('8', 'B6', 'B7'),
('8', 'B8', 'A5'),
('8', 'C1', 'C2'),
('8', 'C3', 'D5'),
('8', 'C5', 'C6'),
('8', 'C8', 'B5'),
('8', 'D1', 'B3'),
('8', 'D2', 'D3'),
('8', 'D4', 'C7'),
('8', 'D6', 'A2'),
('8', 'D8', 'D9')]

    

def rencontres_inter_pots(char1, char2, rencontres):
    li_rencontres_inter_pots = []
    for rencontre in rencontres:
        if (str(char1) in rencontre[1] and str(char2) in rencontre[2]) or (str(char2) in rencontre[1] and str(char1) in rencontre[2]):
            li_rencontres_inter_pots.append(rencontre)
    return li_rencontres_inter_pots


rencontres_AC = rencontres_inter_pots("A", "C", rencontres)
rencontres_AB = rencontres_inter_pots("A", "B", rencontres)
rencontres_AD = rencontres_inter_pots("A", "D", rencontres)
rencontres_BC = rencontres_inter_pots("B", "C", rencontres)
rencontres_BD = rencontres_inter_pots("B", "D", rencontres)

li_rencontres_interpots = [rencontres, rencontres_AB, rencontres_AC, rencontres_AD, rencontres_BC, rencontres_BD]
for li_rencontres in li_rencontres_interpots:
    # Création du graphe orienté
    
    # Création du graphe orienté
    G = nx.DiGraph()

    # Ajout des arêtes avec le jour comme attribut
    for jour, team1, team2 in li_rencontres:
        G.add_edge(team1, team2, day=jour)

    # Définition d'un système de couleurs pour les jours
    colors = {'1': 'red', '2': 'blue', '3': 'green', '4': 'yellow', '5': 'orange', '6': 'purple', '7': 'brown', '8': 'grey'}

    # Assignation des couleurs aux arêtes en fonction du jour
    edge_colors = [colors[G[u][v]['day']] for u, v in G.edges()]

    # Choix d'une disposition pour le graphe
    pos = nx.spring_layout(G)

    # Dessin du graphe
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors, node_size=1500, font_size=12, arrowsize=20, width=2)

    # Optionnel : Ajouter des étiquettes aux arêtes pour les jours
    edge_labels = dict([((u, v,), d['day']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

    plt.show()
