# GraphPartitioning

# Partie "Méthodes Approchées"
Vous trouverez différents fichiers dans ce dossier :
- objectivefunctions.py : Regroupe toutes les fonctions permettant de calculer le coût de la coupe, la variation de gain, etc.
- glouton.py : Algorithme Glouton (v1 et v2)
- kernighanlinV1 : Algorithme de Kernighan-Lin (v1)
- kernighanlinV2 : Algorithme de Kernighan-Lin (v2)
- recuitSimule.py : Algorithme Recuit-Simule
- script.py : Fonctions utiles pour la manipulation de fichier et la création de graphes
- main.py :  Main principal depuis lequel vous pouvez tester les algorithmes


Fonctionnement :
- Allez dans le dossier "Méthodes Approchées".
- Ouvrez main.py.
- Choisissez le graphe et l'algorithme que vous souhaitez tester dans la fonction "main". Attention à ne pas modifier les fonctions en dessous.
- Lancez le programme.

Remarques :
- Les résultats s'affichent dans la console et indiquent par défaut le temps d'exécution et le coût de la coupe trouvé. Si vous souhaitez afficher les résultats en mode verbose, modifiez la valeur de la variable "verbose" en début de main à True.
- L'algorithme Kernighan-Lin (v1) n'est pas adapté aux grands graphes. Il est déconseillé de le tester avec un autre graphe que celui renvoyé par la fonction "getTestGraph".



# Partie "Méthodes Exactes"
Vous trouverez différents fichiers dans ce dossier :
- plneV1 : Version 1 du programme PLNE
- plneV2 : Version 2 du programme PLNE
- plneV3 : Version 3 du programme PLNE
- script.py : Fonctions utiles pour la manipulation de fichier et la création de graphes
- objectivefunctions.py : Regroupe toutes les fonctions permettant de calculer le coût de la coupe, la variation de gain, etc.
- main.py :  Main principal depuis lequel vous pouvez tester les algorithmes

Fonctionnement :
- Allez dans le dossier "Méthodes Exactes".
- Ouvrez main.py.
- Choisissez le graphe et l'algorithme que vous souhaitez tester dans la fonction "main". Attention à ne pas modifier les fonctions en dessous.
- Lancez le programme.

Remarque :
- Les algorithmes ne sont pas adaptés aux grands graphes. Il est déconseillé de les tester avec un autre graphe que celui renvoyé par la fonction "getTestGraph".