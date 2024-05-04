import time
def coin_nord_ouest(costs,offre, demande):


    solution = [[0] * len(demande) for _ in range(len(offre))]


    i, j = 0, 0


    while i < len(offre) and j < len(demande):

        quantite_allouee = min(offre[i], demande[j])
        solution[i][j] = quantite_allouee


        offre[i] -= quantite_allouee
        demande[j] -= quantite_allouee


        if offre[i] == 0:
            i += 1
        if demande[j] == 0:
            j += 1

    cout_total = sum(costs[i][j] * solution[i][j] for i in range(len(offre)) for j in range(len(demande)))


    return solution, cout_total

def lire_fichier_complet(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()

        dimensions = lignes[0].split()
        nb_lignes = int(dimensions[0])
        nb_colonnes = int(dimensions[1])


        matrice_couts = []
        offres = []

        # Lecture des coûts et des offres
        for ligne in lignes[1:1 + nb_lignes]:
            elements = list(map(int, ligne.split()))
            matrice_couts.append(elements[:-1])  # Tous sauf le dernier élément
            offres.append(elements[-1])  # Dernier élément

        # Lecture des demandes, qui sont sur la dernière ligne après les coûts et offres
        demandes = list(map(int, lignes[1 + nb_lignes].split()))

        return matrice_couts, offres, demandes

    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'existe pas.")
        return None, None, None
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        return None, None, None


def trouver_meilleure_arrete(penalites_lignes, penalites_colonnes):
    max_penalite_ligne = max(penalites_lignes)
    max_penalite_colonne = max(penalites_colonnes)

    # Collecter tous les indices avec la pénalité maximale pour les lignes et les colonnes
    indices_max_lignes = [i for i, val in enumerate(penalites_lignes) if val == max_penalite_ligne]
    indices_max_colonnes = [j for j, val in enumerate(penalites_colonnes) if val == max_penalite_colonne]

    # Décider sur la base de la stratégie choisie
    if max_penalite_ligne > max_penalite_colonne:
        return ('ligne', indices_max_lignes[0], max_penalite_ligne)
    elif max_penalite_colonne > max_penalite_ligne:
        return ('colonne', indices_max_colonnes[0], max_penalite_colonne)
    else:
        # En cas d'égalité, choisir la ligne ou la colonne selon un critère (ici premier trouvé, premier choisi)
        # Si vous voulez choisir de façon aléatoire ou selon un autre critère, c'est ici que vous le feriez
        if indices_max_lignes[0] < indices_max_colonnes[0]:
            return ('ligne', indices_max_lignes[0], max_penalite_ligne)
        else:
            return ('colonne', indices_max_colonnes[0], max_penalite_colonne)

def reallocation_selon_arete(solution_initiale, couts, offre, demande, arrete, index):
    n = len(couts)
    m = len(couts[0])

    if arrete == 'ligne':
        ligne = index
        # Récupérer la liste des coûts non utilisés
        non_used_costs = [(couts[ligne][j], j) for j in range(m) if solution_initiale[ligne][j] == 0]

        if non_used_costs:  # Vérifier si la liste est non vide
            min_cout_col = min(non_used_costs)
            col_to_increase = min_cout_col[1]

            # Trouver l'index de la colonne pour réduire la quantité dans la même ligne
            max_cout_col = max((couts[ligne][j], j) for j in range(m) if solution_initiale[ligne][j] > 0)
            col_to_decrease = max_cout_col[1]

            # Réallocation
            quantite_a_reallouer = min(offre[ligne], demande[col_to_increase], solution_initiale[ligne][col_to_decrease])
            solution_initiale[ligne][col_to_increase] += quantite_a_reallouer
            solution_initiale[ligne][col_to_decrease] -= quantite_a_reallouer

    elif arrete == 'colonne':
        colonne = index
        # Récupérer la liste des coûts non utilisés
        non_used_costs = [(couts[i][colonne], i) for i in range(n) if solution_initiale[i][colonne] == 0]

        if non_used_costs:  # Vérifier si la liste est non vide
            min_cout_row = min(non_used_costs)
            row_to_increase = min_cout_row[1]

            # Trouver l'index de la ligne pour réduire la quantité dans la même colonne
            max_cout_row = max((couts[i][colonne], i) for i in range(n) if solution_initiale[i][colonne] > 0)
            row_to_decrease = max_cout_row[1]

            # Réallocation
            quantite_a_reallouer = min(demande[colonne], offre[row_to_increase], solution_initiale[row_to_decrease][colonne])
            solution_initiale[row_to_increase][colonne] += quantite_a_reallouer
            solution_initiale[row_to_decrease][colonne] -= quantite_a_reallouer

    return solution_initiale

def calculer_penalites(couts, solution_initiale):
    n = len(couts)
    m = len(couts[0])
    penalites_lignes = []
    penalites_colonnes = []

    # Calcul des pénalités pour les lignes
    for i in range(n):
        ligne_couts = [(couts[i][j], solution_initiale[i][j]) for j in range(m)]
        # Filtrer pour obtenir seulement les coûts où il y a des allocations
        ligne_couts = [cout for cout, quantite in ligne_couts if quantite > 0]
        if len(ligne_couts) > 1:
            sorted_couts = sorted(ligne_couts)
            penalite = sorted_couts[1] - sorted_couts[0]
            penalites_lignes.append(penalite)
        else:
            penalites_lignes.append(0)  # Pas de pénalité si une seule allocation ou aucune

    # Calcul des pénalités pour les colonnes
    for j in range(m):
        colonne_couts = [(couts[i][j], solution_initiale[i][j]) for i in range(n)]
        # Filtrer pour obtenir seulement les coûts où il y a des allocations
        colonne_couts = [cout for cout, quantite in colonne_couts if quantite > 0]
        if len(colonne_couts) > 1:
            sorted_couts = sorted(colonne_couts)
            penalite = sorted_couts[1] - sorted_couts[0]
            penalites_colonnes.append(penalite)
        else:
            penalites_colonnes.append(0)  # Pas de pénalité si une seule allocation ou aucune

    return penalites_lignes, penalites_colonnes
def solution_initiale_moindre_cout(couts, offre, demande):
    n = len(offre)
    m = len(demande)
    solution = [[0] * m for _ in range(n)]

    # Créer une liste des coûts avec leurs indices pour faciliter le tri et l'allocation
    couts_indices = [(couts[i][j], i, j) for i in range(n) for j in range(m)]
    couts_indices.sort()  # Trier par coût

    for cout, i, j in couts_indices:
        if offre[i] > 0 and demande[j] > 0:
            quantite_allouee = min(offre[i], demande[j])
            solution[i][j] = quantite_allouee
            offre[i] -= quantite_allouee
            demande[j] -= quantite_allouee

    return solution

def calculer_cout_total(couts, solution):
    n = len(couts)
    m = len(couts[0])
    cout_total = 0
    for i in range(n):
        for j in range(m):
            cout_total += solution[i][j] * couts[i][j]
    return cout_total
def balas_hammer(couts, offre, demande):
    solution_initiale = solution_initiale_moindre_cout(couts, offre.copy(), demande.copy())
    cout_total_precedent = calculer_cout_total(couts, solution_initiale)
    cpt = 0
    while True:
        penalites_lignes, penalites_colonnes = calculer_penalites(couts, solution_initiale)

        arrete, index, penalite = trouver_meilleure_arrete(penalites_lignes, penalites_colonnes)

        if penalite == 0:
            break  # Aucune amélioration possible
        cout_total_actuel = calculer_cout_total(couts, solution_initiale)
        if cout_total_actuel == cout_total_precedent:
            break  # Arrêter si le coût total n'a pas diminué
        solution_initiale = reallocation_selon_arete(solution_initiale, couts, offre, demande, arrete, index)
        print(solution_initiale)


        cout_total_precedent = cout_total_actuel


    return solution_initiale, cout_total_actuel

matrice_couts, offres, demandes = lire_fichier_complet('problems/probleme 14.txt')

if matrice_couts is not None:
    print("Matrice des coûts:", matrice_couts)
    print("Offres:", offres)
    print("Demandes:", demandes)
    """solution, cout_total = coin_nord_ouest(matrice_couts, offres, demandes)
    print("Solution initiale après Nord-Ouest:")
    for row in solution:
        print(row)"""
    
    solution1, cout_total = balas_hammer(matrice_couts, offres, demandes)
    print("Solution initiale après Balas-Hammer:")
    print(solution1)
    for ligne in solution1:
        print(ligne)
    print("Coût total:", cout_total)
