def select_file():
    num = input("Veuillez entrer le numéro du fichier à utiliser (1-12)\n0 pour quitter: ")
    file_path = f'probleme {num}.txt'
    if num == '0':
        print("Au revoir!")
        exit()
    else:
        if num not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            print("Numéro invalide!")
            file_path = select_file()
        return file_path
    
def lire_probleme_transport(fichier):
    with open(fichier, 'r') as fichi:
        lignes = fichi.readlines()
        
        dimensions = lignes[0].split()
        nb_lignes = int(dimensions[0])
        nb_colonnes = int(dimensions[1])
        
        matrice = []
        matrice_couts = []
        offres = []

        for ligne in lignes[1:1 + nb_lignes]:
            elements = list(map(int, ligne.split()))
            matrice_couts.append(elements[:-1])
            offres.append(elements[-1])
            
            valeurs_ligne = [int(valeur) for valeur in ligne.strip().split()]
            matrice.append(valeurs_ligne)

        matrice.append(list(map(int, lignes[1 + nb_lignes].split())))
        demande = list(map(int, lignes[1 + nb_lignes].split()))

        return matrice_couts, offres, demande, matrice

def afficher_matrice(matrice):
    max_width = max(len(str(elem)) for row in matrice for elem in row)
    for ligne in matrice:
        print(' | '.join(f"{elem:>{max_width}}" for elem in ligne))

def afficher_tableau(tabl):
    for i in range(len(tabl)):
        print(str(tabl[i]))

def matrice_couts(matrice):
    matrice_cout = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            matrice_cout.append(matrice[i][j])

    return matrice_cout

def coin_nord_ouest(costs, offre, demande):

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

def methode_potentiel(matrice_solution, matrice_cout):
    lignes, colonnes = len(matrice_solution), len(matrice_solution[0])
    truc = []

    # Parcours de la matrice_solution
    for i in range(lignes):
        for j in range(colonnes):
            # Si la valeur dans la matrice_solution est positive
            if matrice_solution[i][j] > 0:
                # Impression des informations
                print("C{}S{}: {}".format(j+1, i+1, matrice_cout[i][j]))
                # Stockage des informations
                truc.append((j+1, i+1, matrice_cout[i][j]))

    # Création d'un ensemble pour stocker les couples
    couples = set(truc)

    # Création d'un ensemble pour stocker les lignes et les colonnes connectées
    connectes = set()

    # Parcours de chaque couple
    for couple in couples:
        j, i, _ = couple
        connectes.add(j)
        connectes.add(i)

    # Trouver les couples isolés
    couples_isoles = couples - connectes

    # Signalisation des couples isolés
    for couple_isole in couples_isoles:
        print("Attention: Le couple {} est isolé.".format(couple_isole))

    return truc







def main():
    while True:
        file_path = select_file()
        matrice_couts, offres, demande, matrice = lire_probleme_transport(file_path)

        print("Matrice :")
        afficher_matrice(matrice)

        print("Matrice des coûts :")
        afficher_matrice(matrice_couts)

        print("Offres :")
        afficher_tableau(offres)

        print("Demandes :")
        afficher_tableau(demande)

        print("Nord Ouest :")
        matrice_solution, cou_total = coin_nord_ouest(matrice_couts, offres, demande)
        afficher_matrice(matrice_solution)
        print("Cou total :\n" + str(cou_total))

        truc =methode_potentiel(matrice_solution, matrice_couts)
        print(truc)


if __name__ == '__main__':
    main()
