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

def calculer_penalites(couts):
    n = len(couts)
    m = len(couts[0])
    penalites_lignes = []
    penalites_colonnes = []

    # Calcul des pénalités pour les lignes
    for i in range(n):
        ligne_sorted = sorted(couts[i])
        penalite = ligne_sorted[1] - ligne_sorted[0] if len(ligne_sorted) > 1 else 0
        penalites_lignes.append(penalite)

    # Calcul des pénalités pour les colonnes
    for j in range(m):
        colonne = [couts[i][j] for i in range(n)]
        colonne_sorted = sorted(colonne)
        penalite = colonne_sorted[1] - colonne_sorted[0] if len(colonne_sorted) > 1 else 0
        penalites_colonnes.append(penalite)

    return penalites_lignes, penalites_colonnes

matrice_couts, offres, demandes = lire_fichier_complet('problems/probleme 13.txt')
penalite_ligne, penalite_colonne = calculer_penalites(matrice_couts)
if matrice_couts is not None:
    print("Matrice des coûts:", matrice_couts)
    print("Offres:", offres)
    print("Demandes:", demandes)
    print("Penalite ligne:", penalite_ligne)
    print("Penalite colonne:", penalite_colonne)

solution, cout_total = coin_nord_ouest(matrice_couts,offres, demandes)



'''
costs = [[30, 20, 20],[10, 50, 20],[50, 40, 30]]
offre = [450, 600, 350]
demande = [500, 600, 300]
'''

print("Solution initiale:")
for row in solution:
    print(row)
print("Coût total:", cout_total)
