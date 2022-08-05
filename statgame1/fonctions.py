# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 22:01:17 2022

@author: matra
"""
import csv
import random
import smtplib, requests
from email.mime.text import MIMEText as mt
from bs4 import BeautifulSoup

debug = False


def initialise(ini):
    global debug
    debug = ini


def sendmail(prono):
    combinaison = " ".join(prono[0:5])
    chance = prono[5]
    combi = combinaison + "  " + chance + "."
    mess = f"Bonjour, voici la combinaison que nous pouvons vous proposer {combinaison} numéro chance: {chance}. Cette proposition n'est qu'expérimentale."
    message = combi + "  " \
              + mess
    msg = mt(message, 'plain', 'utf-8')
    msg['From'] = 'matrail72@gmail.com'
    msg['To'] = 'hyvon.ophelie@orange.fr'
    msg['Subject'] = 'Combinaison du loto pour ma chérie'
    email_receiver = ['matrail72@gmail.com', 'hyvon.ophelie@orange.fr']
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('matrail72@gmail.com', '328860g01')
    mailserver.sendmail('matrail72@gmail.com', email_receiver, msg.as_string())
    mailserver.quit()


def annonciateur(dernier_tirage, liste_des_plus_annonciateurs, liste_globale):
    # En-tete des cases
    # 1- Numéro
    # 2- Réussite Totale
    # 3-Forme récente (nbre de sorties lors des 10 derniers tirages)
    # 4-Forme générale(nbre de sorties lors des 70 derniers tirages)
    # 5-Ecart max
    # 6-Ecart Actuel
    # 7-Ecart le plus favorable
    # 8-Ecart le moins favorable
    # 9-La meilleur affinité
    # 10-La moins bonne affinité
    # 11-Annoncé le plus souvent
    # 12-Numéro le moins souvent
    # 13-Numéro le plus annonciateur
    # 14-Numéro le moins annonciateur

    """"Ce numéro est sorti 189 fois (Réussite Totale). Il est sorti 1 fois sur les 10 derniers tirages (forme récente)
    et 6 fois sur les 70 derniers tirages (forme générale). Depuis la création du Loto, son écart maximum à été de 65
    et son écart actuel est de 6. Ses sorties les plus fréquentes se produisent après l'écart 2 (écart + favorable).
    S'il est à l'écart 21 ne le jouez pas car c'est son écart le moins favorable. Si vous voulez le jouer, associez le
    de préférence avec le 6 (affinité + bonne), mais pas avec le 35 (affinité - bonne). Vous pouvez jouer le 39 si au tirage
    précédent figurait le 27, mais oubliez le si au tirage précédent le 32 était présent. Après la sortie du 39, vous pouvez
    favorablement risquer le 35 (+ annonciateur) mais pas le 5 (-annonciateur)."""
    for numero in dernier_tirage[0:5]:
        for data in liste_globale:
            num = data[0]
            if num == numero:
                if data[12] not in liste_des_plus_annonciateurs:
                    liste_des_plus_annonciateurs.append(data[12])
    if debug:
        print("les plus annonciateurs donnent: ", liste_des_plus_annonciateurs)


def moins_annonciateur(dernier_tirage, liste_des_moins_annonciateurs, liste_globale):
    for numero in dernier_tirage[0:5]:
        for data in liste_globale:
            num = data[0]
            if num == numero:
                liste_des_moins_annonciateurs.append(data[13])
    if debug:
        print("les moins annonciateurs donnent: ", liste_des_moins_annonciateurs)


def ecart_favorable(liste_globale, liste_ecart_favorable):
    for data in liste_globale:
        num = data[0]
        if data[5] == data[6]:
            liste_ecart_favorable.append(num)
    if debug:
        print("liste_ecart_favorable: ", liste_ecart_favorable)


def ecart_defavorable(liste_globale, liste_ecart_defavorable):
    for data in liste_globale:
        num = data[0]
        if data[5] == data[7]:
            liste_ecart_defavorable.append(num)
    if debug:
        print("liste_ecart_defavorable: ", liste_ecart_defavorable)


def numero_fort_ecart(liste_globale, liste_fort_ecart):
    for data in liste_globale:
        num = data[0]
        if int(data[5]) >= 20:
            liste_fort_ecart.append(num)
    if debug:
        print("liste_fort_ecart: ", liste_fort_ecart)


def extract_data(soup, liste):
    for number in soup:
        liste_data = []
        for data in number:
            dt = data.string
            liste_data.append(dt)
        liste.append(liste_data)
    return liste


def save_csv(name, liste_globale):
    with open(name, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';', lineterminator='\n')
        for liste in liste_globale:
            writer.writerow(liste)
    return "Les données ont été sauvegardées dans le fichier csv"


def save_tirage_csv(name, liste):
    with open(name, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';', lineterminator='\n')
        writer.writerow(liste)
    return "Le tirage a été enregistré en CSV."


def extract_link(soup):
    liste_link = []
    for link in soup:
        lk = link.get("href")
        liste_link.append(lk)
    return liste_link


def extract_tirage(soup):
    liste_data = []
    for number in soup:
        num = number.string
        liste_data.append(num)
    return liste_data


def combinaison(liste_proba, liste_moins_proba, combinaison, liste_fort_ecart, liste_ecart_favorable,
                liste_des_plus_annonciateurs):
    for num in liste_des_plus_annonciateurs:
        if num in liste_ecart_favorable:
            combinaison.append(num)

    if len(liste_proba) > 5:
        for numero in liste_proba:
            if numero not in liste_moins_proba:
                combinaison.append(numero)

    elif len(liste_proba) < 5:
        combinaison = liste_proba
    else:

        combinaison = liste_proba

    if len(combinaison) > 5:
        while len(combinaison) != 5:
            num = random.choice(combinaison)
            combinaison.remove(num)

    elif len(combinaison) < 5:
        while len(combinaison) != 5:
            num = random.choice(liste_fort_ecart)
            if num not in combinaison:
                combinaison.append(num)
            else:
                pass
    else:
        pass
    combi = []
    for num in combinaison:
        num = int(num)
        combi.append(num)
    combi = sorted(combi)
    car_combi = []
    for num in combi:
        num = str(num)
        car_combi.append(num)
    return car_combi
    if debug:
        print("car_combi: ", car_combi)


def get_data(liste_globale):
    # Statistiques depuis 2008
    b1 = "odd"
    b2 = "even"
    url = "https://www.secretsdujeu.com/page/jeux_loto_statistiques.html"
    page = requests.get(url)
    stat = BeautifulSoup(page.content, 'html.parser')
    # Liste des balises à récupérer
    num = stat.find_all("tr", class_=b1)
    num2 = stat.find_all("tr", class_=b2)
    liste_globale = extract_data(num2, liste_globale)  # Liste les numéros contenus dans les lignes paires
    liste_globale = extract_data(num, liste_globale)  # Liste les numéros contenus dans les lignes impaires

    # Récupération du lien du dernier tirage
    url_tirage = "https://www.fdj.fr/jeux-de-tirage/resultats"
    page2 = requests.get(url_tirage)
    balise = "result-card__link"
    links = BeautifulSoup(page2.content, 'html.parser')
    results_links = links.find_all("a", class_=balise)
    link_list = extract_link(results_links)

    # Récupération des données du dernier tirage
    loto_url = "https://www.fdj.fr/" + link_list[2]
    date = loto_url.split("/")[-1]
    tirage_page = requests.get(loto_url)
    tag = "game-ball"
    resultat = BeautifulSoup(tirage_page.content, 'html.parser')
    result = resultat.find_all("span", class_=tag)
    last_result = extract_tirage(result)
    dernier_tirage = last_result[0:6]
    jour = date.split("-")
    jour = " ".join(jour)
    print("le tirage du", jour, "est:", " ".join(dernier_tirage[0:5]), "le numéro chance est le", dernier_tirage[-1])
    # save_tirage_csv("dernier_tirage\\" + date + '.csv', dernier_tirage)
    return (dernier_tirage, jour)


def get_chance(combi_probable, chance, chance_data, dernier_tirage, liste_chance_des_plus_annonciateurs,
               liste_chance_ecart_defavorable, liste_chance_ecart_favorable, liste_chance_des_moins_annonciateurs):
    """ Traitement du numéro chance"""

    # En-tete des cases
    # 0- Numéro
    # 1- Réussite Totale
    # 2-Forme récente (nbre de sorties lors des 10 derniers tirages)
    # 3-Forme générale(nbre de sorties lors des 70 derniers tirages)
    # 4-Ecart max
    # 5-Ecart Actuel
    # 6-Ecart le plus favorable
    # 7-Ecart le moins favorable
    # 8-NA
    # 9-Annoncé le plus souvent
    # 10-annoncé le moins souvent
    # 11-Numéro le plus annonciateur
    # 12-Numéro le moins annonciateur

    url = "https://www.secretsdujeu.com/loto/statistique-chance"
    b1 = "odd"
    b2 = "even"
    page = requests.get(url)
    stats = BeautifulSoup(page.content, 'html.parser')
    num_chance = stats.find_all('tr', class_=b1)
    num_chance_2 = stats.find_all('tr', class_=b2)
    chance_data = extract_data(num_chance, chance_data)
    chance_data = extract_data(num_chance_2, chance_data)
    tirage = dernier_tirage[0]
    numero_chance = tirage[5]

    for data in chance_data:
        num = data[0]
        if num == numero_chance:
            liste_chance_des_plus_annonciateurs.append(data[11])
    if debug:
        print("Chance Annonciateur: ", liste_chance_des_plus_annonciateurs)

    for data in chance_data:
        num = data[0]
        if data[5] == data[7]:
            liste_chance_ecart_defavorable.append(num)
    if debug:
        print("Chance defavorable: ", liste_chance_ecart_defavorable)

    for data in chance_data:
        num = data[0]
        if data[5] == data[6]:
            liste_chance_ecart_favorable.append(num)
    if debug:
        print("Chance favorable", liste_chance_ecart_favorable)

    for data in chance_data:
        num = data[0]
        if num == numero_chance:
            liste_chance_des_moins_annonciateurs.append(data[12])
    if debug:
        print("Chance moins annonciateur", liste_chance_des_moins_annonciateurs)

    chance = ['0']
    if liste_chance_des_plus_annonciateurs[0] not in liste_chance_ecart_defavorable:
        chance = liste_chance_des_plus_annonciateurs
    else:
        chance = liste_chance_ecart_favorable

    if chance[0] == '0':
        chance[0] = random.randint[1, 10]
    chance_num = chance[0]
    combi_probable.append(chance_num)
    if debug:
        print("Chance prono: ", chance)
