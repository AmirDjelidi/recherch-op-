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
    
# Jsp comment lire les fichier de facon optimal pour la suite
def lire_probleme_transport(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    # C'est la première ligne qui contient les valeurs de n et m donc celle là elle est bonne mais
    n, m = map(int, lignes[0].split())
    # Mais ici je sais pas comment séparé les ligne pour que ça soit utile plus tard
    provisions = []
    for i in range(1, n+1):
        provisions.append(list(map(float, lignes[i].split()[:-1])))
    
    commandes = list(map(float, lignes[n+1].split()))

    return n, m, provisions, commandes


def main():
    while True:
        file_path = select_file()
        n, m, provisions, commandes = lire_probleme_transport(file_path)
        print("Nombre de fournisseurs:", n)
        print("Nombre de clients:", m)
        print("Provisions:", provisions)
        print("Commandes:", commandes)


if __name__ == '__main__':
    main()