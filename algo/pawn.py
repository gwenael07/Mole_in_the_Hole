class Pawn:
    """Représente un pion sur le plateau de jeu.

    Cette classe gère les coordonnées spatiales du pion et son appartenance
    à un joueur spécifique. Les attributs sont privés (préfixés par `__`)
    pour respecter l'encapsulation.

    Attributes:
        __x (int | None): La coordonnée X (ligne ou colonne) du pion sur le plateau.
        __y (int | None): La coordonnée Y (colonne ou ligne) du pion sur le plateau.
        __player (int): L'identifiant ou l'index du joueur à qui appartient ce pion.
    """

    def __init__(self, player: int):
        """Initialise un nouveau pion associé à un joueur.

        À la création, le pion n'a pas encore de position définie sur le plateau.

        Args:
            player (int): L'identifiant du joueur propriétaire du pion.
        """
        self.__x = None
        self.__y = None
        self.__player = player

    def getPosition(self):
        """Récupère les coordonnées actuelles du pion.

        Returns:
            tuple: Un couple (x, y) représentant la position du pion. 
                   Retourne (None, None) si le pion n'a pas encore été placé.
        """
        return (self.__x, self.__y)

    def setPosition(self, x, y):
        """Met à jour les coordonnées du pion sur le plateau.

        Args:
            x (int): La nouvelle coordonnée X.
            y (int): La nouvelle coordonnée Y.
        """
        self.__x = x
        self.__y = y
