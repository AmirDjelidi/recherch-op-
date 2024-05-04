def coin_nord_ouest(offre, demande):


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




    return solution

def lire_fichier_complet(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()

        # Première ligne pour les dimensions, pas nécessaire pour le parsing puisque le fichier contient directement les données
        nb_lignes = int(lignes[0].split()[1])

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

# Exemple d'utilisation
matrice_couts, offres, demandes = lire_fichier_complet('problems/probleme 13.txt')
if matrice_couts is not None:
    print("Matrice des coûts:", matrice_couts)
    print("Offres:", offres)
    print("Demandes:", demandes)


'''
costs = [[30, 20, 20],[10, 50, 20],[50, 40, 30]]
offre = [450, 600, 350]
demande = [500, 600, 300]
'''
solution = coin_nord_ouest(offres, demandes)

print("Solution initiale:")
for row in solution:
    print(row)
