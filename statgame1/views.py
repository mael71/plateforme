from django.shortcuts import render
from .import fonctions


# Create your views here.

def loto(request):
    import os
    import datetime

    debug = False

    fonctions.initialise(debug)

    liste_stat = []

    liste_des_plus_annonciateurs = []
    liste_ecart_favorable = []
    liste_ecart_defavorable = []
    liste_fort_ecart = []
    liste_des_moins_annonciateurs = []
    liste_chance_des_plus_annonciateurs = []
    chance_data = []
    combinaison = []
    liste_chance_ecart_defavorable = []
    liste_chance_ecart_favorable = []
    liste_chance_des_moins_annonciateurs = []
    chance = []
    lastt = []

    dernier_tirage = fonctions.get_data(liste_stat)

    dernier_tirage = fonctions.extract_data(lastt, dernier_tirage)
    print(dernier_tirage)
    date = str(datetime.datetime.now())[0:19]
    date = date.replace(':', '_')
    date = date.replace('-', '_')
    date = date.replace(' ', '-')

    #csv_file = fonctions.save_csv("data.csv", liste_stat)

    # Permet de trier les listes en fonctions de la fréquence de sortie
    # sort_list = sorted(liste_stat, key=lambda x: x[1], reverse=True)

    # Permet de trier la liste en fonction de la sortie lors des 10 derniers tirages
    # sort_last_10 = sorted(liste_stat, key=lambda x: x[2], reverse=True)

    # csv_sorted = fonctions.save_csv("statistiques\sorted_data.csv", sort_list)
    # csv_last_10 = fonctions.save_csv("statistiques\sorted_data_last_10.csv", sort_last_10)

    # Crée une liste en fonctions des signes anonciateurs selon le dernier tirage
    fonctions.annonciateur(dernier_tirage, liste_des_plus_annonciateurs, liste_stat)

    # Crée une liste en fonctions des écarts favorables
    fonctions.ecart_favorable(liste_stat, liste_ecart_favorable)

    # Crée une liste des numéros les plus défavorables en selon le dernier tirage
    fonctions.ecart_defavorable(liste_stat, liste_ecart_defavorable)

    """Crée une liste des numéro n'étant pas sortis depuis "x" tirages pour y\n
     choisir des numéros si besoin de compéter le pronostic"""
    fonctions.numero_fort_ecart(liste_stat, liste_fort_ecart)

    # Crée une liste en fonction des numéros les moins anonciateurs
    fonctions.moins_annonciateur(dernier_tirage, liste_des_moins_annonciateurs, liste_stat)

    # Liste les numéros avec forte probabilité de sortie
    liste_proba = liste_ecart_favorable + liste_des_plus_annonciateurs

    # Liste les numéros avec faible probabilité de sortie
    liste_moins_proba = liste_ecart_favorable + liste_des_moins_annonciateurs

    # Crée une liste de pronostic
    combi_probable = fonctions.combinaison(liste_proba, liste_moins_proba, combinaison, liste_fort_ecart,
                                           liste_ecart_favorable, liste_des_plus_annonciateurs)
    num_chance = fonctions.get_chance(combi_probable, chance, chance_data, dernier_tirage,
                                      liste_chance_des_plus_annonciateurs, liste_chance_ecart_defavorable,
                                      liste_chance_ecart_favorable, liste_chance_des_moins_annonciateurs)
    # fonctions.save_csv("chance_data.csv", chance_data)
    # fonctions.save_tirage_csv("pronostic\\" + date + ".csv", combi_probable)
    # if not debug:
    # fonctions.sendmail(combi_probable)
    print("voici le pronostic que nous pouvons vous proposer: ", combi_probable)
    # os.system("pause")
    print('click sur le bouton')
    last_ti_list = dernier_tirage[0]
    date = dernier_tirage[1]
    context = {'boule1': combi_probable[0],
               'boule2': combi_probable[1],
               'boule3': combi_probable[2],
               'boule4': combi_probable[3],
               'boule5': combi_probable[4],
               'boule_chance': combi_probable[5],
               'dt1': last_ti_list[0],
               'dt2': last_ti_list[1],
               'dt3': last_ti_list[2],
               'dt4': last_ti_list[3],
               'dt5': last_ti_list[4],
               'dt_chance': last_ti_list[2],
               'date': date
               }
    print(context)
    return render(request, 'accueil.html', context)
