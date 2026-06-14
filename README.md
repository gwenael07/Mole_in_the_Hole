# A Mole in the Hole
___
## Installation

Afin de lancer le jeu, vous allez avoir besoin de:
- python
- pip

Une fois que ceci est installé, ouvrez votre terminal (Powershell sous Windows) et faites ceci:
### Windows
```bash
python -m venv venv
venv/Scripts/activate
pip install .
```

### Linux/MacOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```
Cela installera toutes les librairies et dépendances nécessaires et créera également un exécutable.

#### Note:
Si vous êtes développeur, nous vous conseiller de remplacer `pip install .` par:
```bash
pip install -e .
```
Cela fera en sorte que les modifications que vous faites aux fichiers python seront prises en compte immédiatement sans avoir à refaire la commande d'installation à chaque fois.
## Lancement du jeu

Pour lancer le jeu, rien de plus simple ! Faites seulement dans votre terminal (vous devez avoir fait `venv/Scripts/activate` sous Windows ou `source venv/bin/activate` sous Linux et MacOS avant):
```bash
mole-in-the-hole
```
Le jeu se lancera !
___
## Contrôles

La seule chose dont vous avez besoin est votre **souris** !
___
## Setup

### Thèmes

Plusieurs thèmes sont à votre disposition pour le jeu:
- Banquise
- Volcan
- Désert
- Prairie

Chaque thème a ses propres musiques et effets sonores !

### Langues

Actuellement, le jeu est disponible en 5 langues:

- Anglais
- Français
- Espagnol
- Italien
- Allemand

Choississez celle qui vous convient le mieux !

### Modes de jeu

Le jeu a 2 modes possibles:
- Classique
- Custom

### Classique

Caractéristiques:
- 4 plateaux
- La position des cases n'est pas aléatoire
- Vous disposez d'un deck de 6 cartes, chaque carte indiquant le nombre de cases où vous pouvez bouger (1 carte de 1, 2 de 2, 2 de 3, 1 de 4)

### Custom

Caractéristiques:
- Vous pouvez choisir de jouer avec 3, 4, 5 ou 6 plateaux
- La position des cases est aléatoire
- Vous disposez d'un deck de 6 cartes, chaque carte indiquant le nombre de cases où vous pouvez bouger (1 carte de 1, 2 de 2, 2 de 3, 1 de 4)

### Players

Le jeu peut être joué de **2** à **4** joueurs, le nombre de pions dépendant du nombre de joueurs.

### Types de parties

Il y a deux types de parties:
- Local (sur le même ordinateur)
- LAN (en réseau local avec des ordinateurs différents)

Si vous êtes seuls, vous pouvez jouer face à une IA

L'IA a deux modes de difficulté:
- Facile
- Normal
#### Pions classique

Le nombre de pions dépend du mode de jeu, voilà pour le mode classique:

| Nb Joueurs | Nb Pions |
|------------|----------|
| 2          | 10       |
| 3          | 7        |
| 4          | 6        |

#### Pions custom

Voilà pour le mode custom:

Pour 3 plateaux:               

| Nb Joueurs | Nb Pions |
|------------|----------|
| 2          | 7        |
| 3          | 6        |
| 4          | 5        |

Pour 4 plateaux:

| Nb Joueurs | Nb Pions |
|------------|----------|
| 2          | 10       |
| 3          | 7        |
| 4          | 6        |

Pour 5 plateaux:

| Nb Joueurs | Nb Pions |
|------------|----------|
| 2          | 12       |
| 3          | 10       |
| 4          | 8        |

Pour 6 plateaux:

| Nb Joueurs | Nb Pions |
|------------|----------|
| 2          | 14       |
| 3          | 11       |
| 4          | 7        |

### Phase d'installation

- Vous tournez le plateau (à gauche ou à droite)
- Chaque joueur place ses pions chacun son tour sur des cases sans trou.
- Un pion par case

**OU**

Vous utilisez le lancement rapide
___
## Gameplay
- Vous tirez une carte.
- Vous bougez votre pion en fonction de la valeur inscrite sur la carte et en suivant les règles suivantes:
  - Le déplacement se fait seulement en ligne droite
  - Il ne peut pas se finir sur une case déjà occupée
  - Il est impossible de passer par dessus un autre pion
  - Vous **devez** bouger votre pion. Par conséquent, si le seul déplacement possible est un pion qui est déjà sur un trou, il faut le faire.
  - Si tous les pions d'un joueur sont sur un trou, il peut passer son tour
  - Si un joueur ne peut pas bouger de pions, il peut passer son tour

Quand tous les trous d'un plateau sont remplis, il y a un changement de plateau. Tous les pions qui n'étaient pas sur un trou sont éliminés.

#### ***Attention !***

Si vous êtes à deux joueurs sur le dernier plateau et que vous jouez en mode classique, vous ne pourrez accéder au trou final que par certains chemins ! Si vous arrivez sur la case finale en passant par une barrière, vous finirez de l'autre côté alors attention !

Quand le trou du dernier plateau est rempli, la partie est finie ! 

### Cases bonus

A partir du deuxième plateau, des cases spéciales vont apparaître. Si un joueur finit son tour dessus, il peut rejouer.

### Gagnant

Le gagnant est le joueur dont le pion était sur le trou du dernier plateau.
