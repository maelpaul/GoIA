Projet IA Go


Auteurs:

PAUL Maël
LADAGNOUS Louis-Victor


Fonctionnement de notre joueur (GiGoChad): 

En début de partie, notre joueur joue des coups calculés à l'aide du programme games.py. Ce programme utilise les 
parties professionnelles du fichier games.json et les sépare en deux, d'un côté celles donnant la victoire aux NOIRS
et de l'autre celles donnant la victoire aux BLANCS. Ainsi, si notre joueur joue les NOIRS, il utilisera les parties 
donnant la victoire aux NOIRS pour trouver le meilleur coup possible, cela fonctionne de la même manière s'il joue les
BLANCS. En ce qui concerne le tout premier coup de la partie, le meilleur coup possible est celui qui donne la plus grande
chance que les NOIRS gagnent à la fin. Pour les autres coups, on regarde si le coup de l'adversaire a déjà été joué, si non,
il n'y a pas de données et on va devoir jouer un coup calculé à l'aide de l'iterative deepening, si oui, on regarde quel coup
suivant nous donne la meilleure chance de gagner et on le joue, dans le cas où aucun coup ne nous fait gagner, on joue un coup
calculé à l'aide de l'iterative deepening.
En milieu de partie, lorsque plus aucun coup ne peut être joué en utilisant la banque de données games.json, tous les coups
joués sont calculés avec un iterative deepening, tant que le temps restant à jouer pour le coup courant est supérieur au temps 
de calcul à la profondeur précédente (le temps restant est calculé à l'aide du timeout, qui correspond au temps de calcul maximal 
que l'on autorise pour un coup), on relance un alphabeta de profondeur égale à la précédente plus 1. Le temps de jeu est aussi 
vérifié lors du passage dans l'alphabeta, ce qui permet de ne pas dépasser le temps maximal autorisé pour un coup. La profondeur 
ne permet pas d'atteindre la fin de partie, nous utilisons donc une heuristique pour évaluer le plateau de Go et ainsi trouver 
lequel est le plus avantageux pour nous.
En fin de partie, s'il reste peu de temps de jeu (environ moins d'une minute), le coup à jouer est calculé à l'aide d'un alphabeta 
rapide de profondeur 3 qui utilise une heuristique elle aussi calculée rapidement, cela nous permet de jouer un coup optimal de 
manière très rapide et ainsi d'éviter de faire un Timeout qui nous fait perdre la partie.

En ce qui concerne l'heuristique employée lors de la phase de milieu de partie, une évaluation du plateau courant est effectuée. 
L'heuristique se base sur trois critères : 
    - le nombre de pierres blanches/noires
    - le nombre de libertés accessibles par chaque pion sur le plateau (en fonction de sa couleur)
    - le "poids" des pierres autour de chaque pion du plateau, qui nous donne un "poids total" et donc l'influence de chaque 
    couleur sur le plateau.

L'heuristique consiste donc à calculer, pour chaque coup possible depuis la position courante, le "poids" du plateau en 
fonction des critères mentionnés précédemment.

En fin de partie, on fait usage d'une autre heuristique, beaucoup moins performante mais beaucoup plus rapide. Cette heuristique 
utilise simplement la fonction compute_score() afin d'évaluer le plateau actuel. Elle permet ainsi de jouer des coups en fin de 
partie de manière très rapide tout en essayant de jouer des coups qui ne sont pas aléatoires.

En ce qui concerne le calcul du meilleur coup en début de partie, la création de la bibliothèque d'ouverture en séparant les
parties donnant la victoire aux NOIRS et celles aux BLANCS nous a paru évident. Nous avons ensuite choisi d'utiliser un iterative
deepening, un alphabeta et une heuristique car nous avions pu voir avec les échecs que c'était la manière la plus efficace de 
calculer le meilleur coup à jouer. Nous avons tout de même comparé avec un MonteCarlo qui s'est révélé moins efficace. Pour la
fin de partie, après avoir remarqué que nous dépassions parfois le temps maximal de 30 minutes de calcul pour un joueur, nous
avons décidé de résoudre le problème en implémentant un alphabeta (de profondeur 3) et une heuristique rapide.

Nous avons vérifié la validité de notre player en jouant contre le random player, le gnugo player, notre player, ainsi que des
players d'autres équipes.


Indications:

Goban.py 
---------

Fichier contenant les règles du jeu de GO avec les fonctions et méthodes pour parcourir (relativement) efficacement
l'arbre de jeu, à l'aide de legal_moves() et push()/pop() comme vu en cours.

Ce fichier sera utilisé comme arbitre dans le tournoi. Vous avez maintenant les fonctions de score implantés dedans.
Sauf problème, ce sera la methode result() qui donnera la vainqueur quand is_game_over() sera Vrai.

Vous avez un décompte plus précis de la victoire dans final_go_score()

Pour vous aider à parcourir le plateau de jeu, si b est un Board(), vous pouvez avoir accès à la couleur de la pierre
posée en (x,y) en utilisant b[Board.flatten((x,y))]


GnuGo.py
--------

Fichier contenant un ensemble de fonctions pour communiquer avec gnugo. Attention, il faut installer correctement (et
à part gnugo sur votre machine).  Je l'ai testé sur Linux uniquement mais cela doit fonctionner avec tous les autres
systèmes (même s'ils sont moins bons :)).


starter-go.py
-------------

Exemples de deux développements aléatoires (utilisant legal_moves et push/pop). Le premier utilise legal_moves et le
second weak_legal_moves, qui ne garanti plus que le coup aléatoire soit vraiment légal (à cause des Ko).

La première chose à faire est probablement de 


localGame.py
------------

Permet de lancer un match de myPlayer contre lui même, en vérifiant les coups avec une instanciation de Goban.py comme
arbitre. Vous ne devez pas modifier ce fichier pour qu'il fonctionne, sans quoi je risque d'avoir des problèmes pour
faire entrer votre IA dans le tournoi.


playerInterface.py
------------------

Classe abstraite, décrite dans le sujet, permettant à votre joueur d'implanter correctement les fonctions pour être
utilisé dans localGame et donc, dans le tournoi. Attention, il faut bien faire attention aux coups internes dans Goban
(appelés "flat") et qui sont utilisés dans legal_moves/weak_legal_moves et push/pop des coups externes qui sont
utilisés dans l'interface (les named moves). En interne, un coup est un indice dans un tableau 1 dimension
-1, 0.._BOARDSIZE^2 et en externe (dans cette interface) les coups sont des chaines de caractères dans "A1", ..., "J9",
"PASS". Il ne faut pas se mélanger les pinceaux.


myPlayer.py
-----------

Fichier que vous devrez modifier pour y mettre votre IA pour le tournoi. En l'état actuel, il contient la copie du
joueur randomPlayer.py


randomPlayer.py
---------------

Un joueur aléatoire que vous pourrez conserver tel quel


gnugoPlayer.py
--------------

Un joueur basé sur gnugo. Vous permet de vous mesurer à lui simplement.


namedGame.py
------------

Permet de lancer deux joueurs différents l'un contre l'autre.
Il attent en argument les deux modules des deux joueurs à importer.


EXEMPLES DE LIGNES DE COMMANDES:
================================

python3 localGame.py
--> Va lancer un match myPlayer.py contre myPlayer.py

python3 namedGame.py myPlayer randomPlayer
--> Va lancer un match entre votre joueur (NOIRS) et le randomPlayer
 (BLANC)

python3 namedGame.py gnugoPlayer myPlayer
 --> gnugo (level 0) contre votre joueur (très dur à battre)
