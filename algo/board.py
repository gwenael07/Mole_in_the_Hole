from copy import deepcopy
from random import shuffle

class Board:
    """
        Classe representant un plateau hexagonal du jeu.

        Un plateau est compose :
        - de cases vides (0)
        - de trous (5)
        - de bonus (6)
        - de zones inexistantes (None)

        Le plateau peut etre :
        - fixe : positions predefinies
        - aleatoire : positions generees dynamiquement
    """
    def __init__(self, numberBoard, underBoardRandom=False):
        """
            Initialise un plateau.

            Parametres
            ----------
            numberBoard : int
                Numero du plateau.

            underBoardRandom : bool | Board
                False pour un plateau fixe.
                Objet Board correspondant au plateau inferieur
                pour un plateau aleatoire.

            Attributes
            ----------
            __board : list
                Matrice representant le plateau.

            __height : int
                Taille de la matrice.

            __midBoard : int
                Centre du plateau utilise pour les rotations.

            __underBoard : Board | bool
                Plateau situe en dessous.
        """
        self.__numberBoard = numberBoard

        self.__tabHoles = [
                            {1:[(0,5),(0,7),(2,8),(3,1),(3,3),(3,6),(4,4),(5,2),(5,5),(6,4),(6,6),(7,0),(8,1)]},
                            {2:[(0,4),(1,6),(2,3),(3,7),(5,1),(7,2),(7,4),(8,0)]},
                            {3:[(2,5),(3,1),(3,8),(8,2)]},
                            {4:[(4,4)]}]

        self.__tabBonus = [
                            {1:[None]},
                            {2:[(1,7),(4,0),(4,5),(8,4)]},
                            {3:[(0,6),(5,0),(5,4),(6,6)]},
                            {4:[(0,8),(2,3),(6,5),(8,0)]}]

        self.__board = [[None if
                         l==0 and c<=3 or l==1 and c<=2 or l==2 and c<=1 or
                         l==3 and c==0 or l==5 and c==8 or l==6 and c>=7 or
                         l==7 and c>=6 or l==8 and c>=5
                         else 0
                         for c in range(9)] for l in range(9)]

        self.__height = len(self.__board)
        self.__midBoard = 4
        self.__underBoard = underBoardRandom

        if underBoardRandom == False:
            self.addHoles()
            self.addBonus()



    def getBoard(self):
        """
            Retourne la matrice du plateau.

            Returns
            -------
            list
                Matrice contenant les cases du plateau.
        """
        return self.__board

    def getHeight(self):
        """
            Retourne la hauteur de la matrice.

            Returns
            -------
            int
                Taille du plateau.
        """
        return self.__height

    def addHoles(self):
        """
            Place les trous fixes du plateau.

            Les trous sont representes par la valeur 5.
            Les positions proviennent de __tabHoles.
        """
        for element in self.__tabHoles[self.__numberBoard-1][self.__numberBoard]:
            self.__board[element[0]][element[1]] = 5

    def addBonus(self):
        """
            Place les bonus fixes du plateau.

            Les bonus sont representes par la valeur 6.
            Le premier plateau ne contient pas de bonus.
        """
        for element in self.__tabBonus[self.__numberBoard - 1][self.__numberBoard]:
            if self.__numberBoard != 1:
                self.__board[element[0]][element[1]] = 6

    def matrixToAxial(self, r, q):
        """
            Convertit des coordonnees matricielles
            vers des coordonnees axiales hexagonales.

            Parametres
            ----------
            r : int
                Ligne de la matrice.

            q : int
                Colonne de la matrice.

            Returns
            -------
            tuple
                Coordonnees axiales.
        """
        return r - self.__midBoard, q - self.__midBoard

    def axialToCube(self, r, q):
        """
            Convertit des coordonnees axiales
            vers des coordonnees cubiques.

            Parametres
            ----------
            r : int
                Coordonnee axiale r.

            q : int
                Coordonnee axiale q.

            Returns
            -------
            tuple
                Coordonnees cubiques (r, q, s).
        """
        return r, q, -q - r

    def turn60Clock(self, r, q, s):
        """
            Effectue une rotation de 60 degres
            dans le sens horaire sur des coordonnees cubiques.

            Parametres
            ----------
            r : int
                Coordonnee cube r.

            q : int
                Coordonnee cube q.

            s : int
                Coordonnee cube s.

            Returns
            -------
            tuple
                Coordonnees cubiques apres rotation.
        """
        return -s, -r, -q

    def axialToMatrix(self, r, q):
        """
            Convertit des coordonnees axiales
            vers des coordonnees matricielles.

            Parametres
            ----------
            r : int
                Coordonnee axiale r.

            q : int
                Coordonnee axiale q.

            Returns
            -------
            tuple
                Coordonnees dans la matrice.
        """
        return r + self.__midBoard, q + self.__midBoard

    def turnMatrix(self):
        """
            Effectue une rotation complete du plateau
            de 60 degres dans le sens horaire.

            Toutes les cases valides sont converties :
            matrice -> axial -> cube -> rotation -> matrice.
        """
        newBoard = deepcopy(self.__board)
        for row in range(self.__height):
            for column in range(self.__height):
                if self.__board[row][column] != None:
                    axial_r, axial_q = self.matrixToAxial(row, column)
                    cube_r, cube_q, cube_s = self.axialToCube(axial_r, axial_q)
                    new_r, new_q, new_s = self.turn60Clock(cube_r, cube_q, cube_s)
                    indice_r, indice_q = self.axialToMatrix(new_r, new_q)
                    newBoard[indice_r][indice_q] = self.__board[row][column]
        self.__board = deepcopy(newBoard)

    def placeSimpleElement(self, valeur, quantity):
        """
            Place aleatoirement des elements sur le plateau.

            Les positions sont choisies parmi les cases libres.

            Parametres
            ----------
            valeur : int
                Valeur a placer sur le plateau.

            quantite : int
                Nombre d'elements a placer.
        """
        freeCase = [(row, column) for row in range(self.__height) for column in range(self.__height)
                 if self.__board[row][column] == 0]
        shuffle(freeCase)
        placed = 0
        for (row, column) in freeCase:
            if placed < quantity:
                self.__board[row][column] = valeur
                placed += 1

    def validHex(self, row, column):
        """
            Verifie si une case est valide
            par rapport au plateau inferieur.

            Une case est valide uniquement si
            la case situee en dessous est vide.

            Parametres
            ----------
            row : int
                Ligne de la case.

            column : int
                Colonne de la case.

            Returns
            -------
            bool
                True si la case est valide.
        """
        case = self.__underBoard.getBoard()[row][column]
        return case == 0

    def placeValidElement(self, value, quantity):
        """
            Place aleatoirement des elements
            sans superposition interdite.

            Les elements sont uniquement places
            sur des cases valides par rapport
            au plateau inferieur.

            Parametres
            ----------
            value : int
                Valeur a placer.

            quantity : int
                Nombre d'elements a placer.
        """
        freeCase = [(row, column) for row in range(self.__height) for column in range(self.__height)
                 if self.__board[row][column] == 0]
        shuffle(freeCase)
        placed = 0
        for (row, column) in freeCase:
            if placed < quantity:
                if self.validHex(row, column):
                    self.__board[row][column] = value
                    placed += 1

def createRandomBoards(nbBoards: int):
    """
        Cree une liste de plateaux aleatoires.

        Cette fonction genere entre 3 et 6 plateaux hexagonaux.
        Chaque plateau contient un nombre de trous et de bonus
        dependant de sa position dans la pile.

        Parametres
        ----------
        nbPlateaux : int
            Nombre de plateaux a generer (entre 3 et 6).

        Returns
        -------
        list
            Liste d'objets Board ordonnes du bas vers le haut.

        Raises
        ------
        ValueError
            Si nbPlateaux est inferieur a 3 ou superieur a 6.
    """
    if not (3 <= nbBoards <= 6):
        raise ValueError("Le nombre de plateaux doit etre entre 3 et 6.")

    tabHoles = [26, 19, 13, 8, 4, 1]

    boards = []
    prevBoard = None

    for i in range(nbBoards):

        isFirst = (i == 0)

        underArg = 'random' if prevBoard is None else prevBoard

        board = Board(numberBoard=i + 1, underBoardRandom=underArg)

        if prevBoard is None:
            board.placeSimpleElement(valeur=5, quantity=tabHoles[i+len(tabHoles)-nbBoards])
            if not isFirst:
                board.placeSimpleElement(valeur=6, quantity=4)

        else:
            board.placeValidElement(value=5, quantity=tabHoles[i+len(tabHoles)-nbBoards])
            if not isFirst:
                board.placeValidElement(value=6, quantity=4)
        boards.append(board)
        prevBoard = board

    return boards

def createFixedBoards():
    """
        Cree les 4 plateaux fixes du jeu.

        Chaque plateau utilise des positions predefinies
        pour les trous et les bonus.

        Returns
        -------
        list
            Liste de 4 objets Board fixes.
    """
    boards = []

    for i in range(4):

        board = Board(numberBoard=i + 1)

        boards.append(board)

    return boards

def createBoards(mode="fixed", nbBoards=4):
    """
        Fonction principale de creation des plateaux.

        Permet de choisir entre generation fixe ou aleatoire.

        Parametres
        ----------
        mode : str
            Mode de generation ("fixed" ou "random").

        nbPlateaux : int
            Nombre de plateaux a generer en mode aleatoire.

        Returns
        -------
        list
            Liste de plateaux (Board).

        Raises
        ------
        ValueError
            Si le mode n'est pas reconnu.
    """
    if mode == "fixed":

        return createFixedBoards()

    elif mode == "random":

        return createRandomBoards(nbBoards)

    else:
        raise ValueError("Mode invalide.")
