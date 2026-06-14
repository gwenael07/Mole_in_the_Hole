import random
from algo.pawn import *


class Player:
    """Représente un joueur dans le jeu.

    Cette classe gère l'identité du joueur, la liste de ses pions sur le plateau,
    ainsi que son deck de cartes (pioche) et l'état de révélation de ces cartes.

    Attributes:
        __player (int): L'identifiant unique ou l'index du joueur.
        __pawnList (list[Pawn]): La liste des objets `Pawn` possédés par le joueur.
        __deck (list[int]): Les valeurs des 6 cartes du joueur (ex: [1, 2, 2, 3, 3, 4]).
        __revealed (list[bool]): Liste de booléens indiquant si la carte à l'index correspondant est révélée.
    """

    def __init__(self, player):
        """Initialise un joueur avec son deck initial et une liste de pions vide.

        Args:
            player (int): L'identifiant du joueur.
        """
        self.__player = player
        self.__pawnList = []

        self.__deck = [1, 2, 2, 3, 3, 4]
        self.__revealed = [False] * 6
        self.resetDeck()

    def resetDeck(self):
        """Mélange aléatoirement les 6 cartes du deck et les cache toutes.

        Cette méthode réinitialise l'état de révélation à `False` pour chaque carte.
        """
        random.shuffle(self.__deck)
        self.__revealed = [False, False, False, False, False, False]

    def getDeck(self):
        """Récupère le deck de cartes du joueur (mélangé).

        Returns:
            list[int]: La liste des valeurs des cartes du deck.
        """
        return self.__deck

    def getRevealed(self):
        """Récupère l'état de révélation de chaque carte du deck.

        Returns:
            list[bool]: Une liste de 6 booléens (True si révélée, False si cachée).
        """
        return self.__revealed

    def drawSpecificCard(self, index):
        """Révèle et pioche une carte spécifique du deck à partir de son index.

        La carte ne peut être piochée que si l'index est valide et qu'elle
        n'a pas encore été révélée.

        Args:
            index (int): L'index de la carte à piocher (0 à 5).

        Returns:
            int | None: La valeur de la carte piochée, ou None si la carte était déjà révélée ou l'index invalide.
        """
        if 0 <= index < 6 and not self.__revealed[index]:
            self.__revealed[index] = True
            return self.__deck[index]
        return None

    def allCardsRevealed(self):
        """Vérifie si toutes les cartes du deck ont été révélées.

        Returns:
            bool: True si les 6 cartes sont révélées, False sinon.
        """
        return all(self.__revealed)

    def checkAndResetDeckIfNeeded(self):
        """Réinitialise le deck automatiquement si toutes les cartes ont été piochées."""
        if self.allCardsRevealed():
            self.resetDeck()

    def drawRandomCard(self):
        """Pioche une carte cachée au hasard.

        Sélectionne aléatoirement une carte parmi celles qui ne sont pas encore révélées.
        Si toutes les cartes ont déjà été révélées, le deck est automatiquement
        réinitialisé et mélangé avant de procéder à la pioche.

        Returns:
            int | None: La valeur de la carte piochée au hasard.
        """
        unrevealedIndexes = [element for element, rev in enumerate(self.__revealed) if not rev]

        if not unrevealedIndexes:
            self.resetDeck()
            unrevealedIndexes = list(range(6))

        idx = random.choice(unrevealedIndexes)
        return self.drawSpecificCard(idx)

    def getPawnPosition(self):
        """Récupère les positions de tous les pions appartenant au joueur.

        Returns:
            list[tuple]: Une liste de couples (x, y) représentant la position de chaque pion.
        """
        coordPawn = []
        for pawn in self.__pawnList:
            coordPawn.append(pawn.getPosition())
        return coordPawn

    def setDeckState(self, deck, revealed):
        self.__deck = deck
        self.__revealed = revealed

    def getPawnList(self):
        """Récupère la liste des objets pions du joueur.

        Returns:
            list[Pawn]: La liste contenant les instances de `Pawn` du joueur.
        """
        return self.__pawnList

    def createPawn(self, x, y):
        """Instancie un nouveau pion pour le joueur et le place aux coordonnées indiquées.

        Le pion créé est automatiquement ajouté à la liste des pions du joueur.

        Args:
            x (int): Coordonnée X de départ du nouveau pion.
            y (int): Coordonnée Y de départ du nouveau pion.
        """
        pawn = Pawn(self.__player)
        pawn.setPosition(x, y)
        self.__pawnList.append(pawn)

    def movePawn(self, x1, y1, x2, y2):
        """Déplace un pion du joueur d'une position de départ vers une position d'arrivée.

        La méthode cherche dans la liste du joueur le pion situé en (x1, y1)
        et met à jour ses coordonnées en (x2, y2).

        Args:
            x1 (int): Coordonnée X actuelle du pion à déplacer.
            y1 (int): Coordonnée Y actuelle du pion à déplacer.
            x2 (int): Nouvelle coordonnée X de destination.
            y2 (int): Nouvelle coordonnée Y de destination.
        """
        for element in range(len(self.__pawnList)):
            pawn = self.__pawnList[element]
            if pawn.getPosition()[0] == x1 and pawn.getPosition()[1] == y1:
                pawn.setPosition(x2, y2)
