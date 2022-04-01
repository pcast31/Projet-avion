# Projet-avion
Projet d'optimisation de placement de passagers dans un avion par Paul Castéras, Tom De Coninck, Pierre Eberschweiler, Thibaut Pellerin et Alexis Robardet.

CentraleSupélec, en partenariat avec Air France KLM - 2022 - ST7 Optimisation de systèmes de transport passagers

Pour lancer l'exécution du programme, il faut exécuter main.py en suivant les instructions qui y sont présentes. On peut notamment modifier le numéro du scénario considéré et le temps maximal d'exécution pour Gurobi.

- affichage.py : affichage des résultats dans la console
- comparaison.py : comparer la qualité de différentes solutions
- contraintes.py : contraintes du modèle
- dyna_ffichage.py : affichage interactif du modèle dynamique
- individu.py : définition de la classe Individu
- initialisation.py : définition des variables binaires
- lirexcel.py : lecture des données de l'Excel
- main.py : fichier à exécuter
- modele_dynamique.py : avorton de modèle dynamique (inutile désormais)
- objectif.py : définition de la fonction objectif
- permutation.py : gère les permuations des groupes de même taille dans le cadre du modèle dynamique
- postprocessing.py : second traitement de la solution permttant de réunir les groupes sur une même rangée
- pourcenta_ffichage.py : affichage d'une barre de chargement pendant le calcul de Gurobi (non utilisé dans la version finale)
- tk_ffichage.py : affichage des résultats dans une fenêtre
- toutes_solutions.py : autre avorton inutile
