from algo.board import Board, createBoards
from algo.player import Player
from random import shuffle


class Game:
    """
        Gere le deroulement d'une partie,
        les joueurs, les plateaux et les mouvements.
    """
    def __init__(self, numPlayers = 2,randomBoard = False,numBoards = 4, aiPlayers = None):
        """
            Initialise une nouvelle partie.

            Parametres
            ----------
            numPlayers : int
                Nombre de joueurs.

            randomBoard : bool
                Definit si les plateaux sont aleatoires.

            numBoards : int
                Nombre de plateaux utilises.

            aiPlayers : list
                Liste des joueurs controles par l'IA.
        """
        # joueur
        self.__numPlayers = numPlayers
        self.__players = [Player(i) for i in range(1, numPlayers + 1)]
        self.__currentPlayerIndex = 0
        self.__maxPawns = 6

        if numBoards == 3:
            if numPlayers == 2:
                self.__maxPawns = 7
            elif numPlayers == 3:
                self.__maxPawns = 6
            else:
                self.__maxPawns = 5

        elif numBoards == 4:
            if numPlayers == 2:
                self.__maxPawns = 10
            elif numPlayers == 3:
                self.__maxPawns = 7
            else:
                self.__maxPawns = 6

        elif numBoards == 5:
            if numPlayers == 2:
                self.__maxPawns = 12
            elif numPlayers == 3:
                self.__maxPawns = 10
            else:
                self.__maxPawns = 8

        elif numBoards == 6:
            if numPlayers == 2:
                self.__maxPawns = 14
            elif numPlayers == 3:
                self.__maxPawns = 11
            else:
                self.__maxPawns = 7


        # board
        self.__randomBoard = randomBoard
        if self.__randomBoard == False:
            self.__boards = createBoards(mode="fixed")
        else:
            self.__boards = createBoards(mode="random", nbBoards=numBoards)

        self.__currentLevel = 0

        # game
        self.__pawnGrid = [[None for column in range(self.__boards[self.__currentLevel].getHeight())] for row in
                           range(self.__boards[self.__currentLevel].getHeight())]
        self.__currentCardValue = 0
        self.__currentCardIndex = None
        self.__bonusTurn = False

        self.__aiPlayers = aiPlayers if aiPlayers else []

    def getPlayerDeck(self):
        player = self.__players[self.__currentPlayerIndex]
        return player.getDeck(), player.getRevealed()

    def getCurrentCardIndex(self):
        return self.__currentCardIndex

    def getBoardMatrix(self, numBoard):
        return self.__boards[numBoard - 1].getBoard()

    def getNumPlayers(self):
        return self.__numPlayers

    def getMaxPawns(self):
        return self.__maxPawns

    def getPawnGrid(self):
        return self.__pawnGrid


    def getCurrentLevel(self):
        return self.__currentLevel

    def setCurrentLevel(self, newLevel):
        self.__currentLevel = newLevel

    def setCurrentCard(self, cardValue):
        self.__currentCardValue = cardValue
        if cardValue is None:
            self.__currentCardIndex = None

    def resetCurrentCard(self):
        self.__currentCardValue = None
        self.__currentCardIndex = None
        player = self.__players[self.__currentPlayerIndex]
        player.checkAndResetDeckIfNeeded()

    def getCurrentPlayerIndex(self):
        return self.__currentPlayerIndex

    def placePawn(self, row, column):
        """
           Place un pion sur le plateau.

           Parametres
           ----------
           row : int
               Ligne de la case.

           column : int
               Colonne de la case.

           Returns
           -------
           bool
               True si le pion est place.
        """
        board_matrix = self.__boards[self.__currentLevel].getBoard()

        # verification
        if board_matrix[row][column] is None:
            return False
        if board_matrix[row][column] == 5:
            return False
        if self.__pawnGrid[row][column] is not None:
            return False

        # placer le pion
        player = self.__players[self.__currentPlayerIndex]
        player.createPawn(row, column)
        self.__pawnGrid[row][column] = self.__currentPlayerIndex + 1

        self.__currentPlayerIndex = (self.__currentPlayerIndex + 1) % self.__numPlayers
        return True

    def drawCard(self):
        """
            Pioche une carte pour le joueur courant.

            Returns
            -------
            int
                Valeur de la carte piochee.
        """
        player = self.__players[self.__currentPlayerIndex]
        self.__currentCardValue = player.drawRandomCard()
        return self.__currentCardValue



    def drawSpecificCard(self, index):
        """
            Pioche une carte specifique.

            Parametres
            ----------
            index : int
                Index de la carte.

            Returns
            -------
            int
                Valeur de la carte.
        """
        player = self.__players[self.__currentPlayerIndex]
        val = player.drawSpecificCard(index)
        if val is not None:
            self.__currentCardValue = val
            self.__currentCardIndex = index
        return val



    def validHexaMove(self, startRow, startColumn, endRow, endColumn, distance):
        """
            Verifie si un mouvement hexagonal est valide.

            Parametres
            ----------
            startRow : int
                Ligne de depart.

            startColumn : int
                Colonne de depart.

            endRow : int
                Ligne d'arrivee.

            endColumn : int
                Colonne d'arrivee.

            distance : int
                Distance du mouvement.

            Returns
            -------
            bool
                True si le mouvement est valide.
        """
        distanceRow = endRow - startRow
        distanceColumn = endColumn - startColumn

        # verifier la ligne droite en coord axiale
        if not (distanceRow == 0 or distanceColumn == 0 or distanceRow == -distanceColumn):
            return False

        # verifier la distance exacte
        hexaDistance = max(abs(distanceRow), abs(distanceColumn), abs(distanceRow + distanceColumn))
        if hexaDistance != distance:
            return False

        # verifier que la case d'arrivee n'est pas occupee
        if self.__pawnGrid[endRow][endColumn] is not None:
            return False

        # saut autre pion
        stepRow = distanceRow // hexaDistance if distanceRow != 0 else 0
        stepColumn = distanceColumn // hexaDistance if distanceColumn != 0 else 0

        currRow, currColumn = startRow + stepRow, startColumn + stepColumn
        while (currRow, currColumn) != (endRow, endColumn):
            if self.__pawnGrid[currRow][currColumn] is not None:
                return False
            currRow += stepRow
            currColumn += stepColumn

        if not self.__randomBoard and self.playerCanPlay() == 2 and self.__currentLevel == 3:
            if (endRow, endColumn) == (4, 4):
                blocked = [(3, 4), (2, 4), (1, 4), (0, 4), 
                           (5, 3), (6, 2), (7, 1), (8, 0),  
                           (4, 5), (4, 6), (4, 7), (4, 8)]  
                if (startRow, startColumn) in blocked:
                    return False

        return True

    def getValidMoves(self, startRow, startColumn):
        """
            Retourne les mouvements possibles d'un pion.

            Parametres
            ----------
            startRow : int
                Ligne de depart.

            startColumn : int
                Colonne de depart.

            Returns
            -------
            list
                Liste des mouvements possibles.
        """
        moves = []
        if self.__currentCardValue == 0 or self.__currentCardValue is None:
            return moves
        boardMatrix = self.__boards[self.__currentLevel].getBoard()
        for row in range(9):
            for column in range(9):
                if boardMatrix[row][column] is None:
                    continue
                if self.validHexaMove(startRow, startColumn, row, column, self.__currentCardValue):
                    moves.append((row, column))
        return moves


    def movePawn(self, startRow, startColumn, endRow, endColumn):
        """
            Deplace un pion.

            Parametres
            ----------
            startRow : int
                Ligne de depart.

            startColumn : int
                Colonne de depart.

            endRow : int
                Ligne d'arrivee.

            endColumn : int
                Colonne d'arrivee.

            Returns
            -------
            bool
                True si le deplacement est effectue.
        """
        self.__bonusTurn = False
        # verification
        if self.__pawnGrid[startRow][startColumn] != self.__currentPlayerIndex + 1:
            return False
        valid = self.validHexaMove(startRow, startColumn, endRow, endColumn, self.__currentCardValue)
        if not valid:
            return False

        # mouvement
        player = self.__players[self.__currentPlayerIndex]
        player.movePawn(startRow, startColumn, endRow, endColumn)
        self.__pawnGrid[endRow][endColumn] = self.__pawnGrid[startRow][startColumn]
        self.__pawnGrid[startRow][startColumn] = None

        # cases spéciales
        board_matrix = self.__boards[self.__currentLevel].getBoard()
        if board_matrix[endRow][endColumn] == 6 and not self.__bonusTurn:
            self.__bonusTurn = True
            self.resetCurrentCard()
            return True

        # Fin du tour
        self.resetCurrentCard()
        self.__bonusTurn = False
        self.nextTurn()
        return True

    def playerCanPlay(self):
        """
            Compte les joueurs pouvant jouer

            Returns
            -------
            int
                Nombre de joueurs actifs.
        """
        active_players = set()
        for row in self.__pawnGrid:
            for cell in row:
                if cell is not None and isinstance(cell, int) and 1 <= cell <= self.__numPlayers:
                    active_players.add(cell)
        return len(active_players)

    def playerEliminated(self):
        """
            Passe les joueurs elimines.
        """
        if self.playerCanPlay() > 0:
            while not any(c == self.__currentPlayerIndex + 1 for r in self.__pawnGrid for c in r):
                self.__currentPlayerIndex = (self.__currentPlayerIndex + 1) % self.__numPlayers

    def checkHoles(self):
        """
            Verifie si tous les trous sont remplis.

            Returns
            -------
            bool
                True si tous les trous sont remplis.
        """
        boardMatrix = self.__boards[self.__currentLevel].getBoard()
        for row in range(Board.getHeight(self.__boards[self.__currentLevel])):
            for column in range(Board.getHeight(self.__boards[self.__currentLevel])):
                if boardMatrix[row][column] == 5 and self.__pawnGrid[row][column] is None:
                    return False
        return True

    def checkPawns(self):
        """
            Verifie les pions presents sur les cases interdites et les supprimes du jeu.
        """
        boardMatrix = self.__boards[self.__currentLevel].getBoard()
        for player in range(self.__numPlayers):
            for row in range(Board.getHeight(self.__boards[self.__currentLevel])):
                for column in range(Board.getHeight(self.__boards[self.__currentLevel])):
                    if boardMatrix[row][column] == 0 and self.__pawnGrid[row][column] == player + 1:
                        self.__pawnGrid[row][column] = None
                        if len(self.__players[player].getPawnList()) > 0:
                            self.__players[player].getPawnList().pop()

    def turnBoard(self, numBoard, reverse=False):
        """
            Fait tourner un plateau.

            Parametres
            ----------
            numBoard : int
                Numero du plateau.

            reverse : bool
                Definit le sens de rotation.
        """
        if reverse:
            for i in range(5):
                self.__boards[numBoard - 1].turnMatrix()
        else:
            self.__boards[numBoard - 1].turnMatrix()

    def winner(self):
        """
            Verifie si un joueur a gagne.

            Returns
            -------
            int
                Numero du joueur gagnant.
        """
        if self.__currentLevel == len(self.__boards) - 1:
            boardMatrix = self.__boards[self.__currentLevel].getBoard()

            for player in range(self.__numPlayers):
                for row in range(Board.getHeight(self.__boards[self.__currentLevel])):
                    for column in range(Board.getHeight(self.__boards[self.__currentLevel])):
                        if boardMatrix[row][column] == 5 and self.__pawnGrid[row][column] == player + 1:
                            return player + 1
        elif self.playerCanPlay() == 1:
            for player in range(self.__numPlayers):
                if any(c == player + 1 for r in self.__pawnGrid for c in r):
                    return player + 1
        return False

    def nextTurn(self):
        """
            Passe au tour du joueur suivant.
        """
        self.__currentPlayerIndex = (self.__currentPlayerIndex + 1) % self.__numPlayers

        if self.playerCanPlay() > 0:
            while not any(c == self.__currentPlayerIndex + 1 for r in self.__pawnGrid for c in r):
                self.__currentPlayerIndex = (self.__currentPlayerIndex + 1) % self.__numPlayers

        nextPlayer = self.__players[self.__currentPlayerIndex]
        nextPlayer.checkAndResetDeckIfNeeded()

        self.__currentCardValue = None
        self.__currentCardIndex = None

    def isAIPlayer(self, playerIndex):
        """
           Verifie si un joueur est controle par l'IA.

           Parametres
           ----------
           playerIndex : int
               Index du joueur.

           Returns
           -------
           bool
               True si le joueur est une IA.
        """
        return playerIndex in self.__aiPlayers

    def quickLaunch(self):
        """
            Place rapidement les pions sur le plateau.
        """
        totalPawns = self.__numPlayers * self.__maxPawns
        boardMatrix = self.__boards[self.__currentLevel].getBoard()

        validCells = []
        for row in range(9):
            for column in range(9):
                if boardMatrix[row][column] is not None and boardMatrix[row][column] != 5:
                    validCells.append((row, column))

        shuffle(validCells)
        for pawn in range(totalPawns):
            if validCells:
                row, column = validCells.pop()
                self.placePawn(row, column)

    def canSkipTurn(self):
        """
            Verifie si le joueur peut passer son tour.

            Returns
            -------
            bool
                True si le joueur peut passer son tour.
        """
        if self.__currentCardValue is None or self.__currentCardValue == 0:
            return False

        boardMatrix = self.__boards[self.__currentLevel].getBoard()
        playerNum = self.__currentPlayerIndex + 1

        allInHoles = True
        hasPawns = False
        pawnsInHolesHaveMoves = False

        for row in range(Board.getHeight(self.__boards[self.__currentLevel])):
            for column in range(Board.getHeight(self.__boards[self.__currentLevel])):
                if self.__pawnGrid[row][column] == playerNum:
                    hasPawns = True
                    if boardMatrix[row][column] != 5:
                        allInHoles = False
                        if self.getValidMoves(row, column):
                            return False
                    else:
                        if self.getValidMoves(row, column):
                            pawnsInHolesHaveMoves = True

        if not hasPawns:
            return True
        if allInHoles:
            return True
        if pawnsInHolesHaveMoves:
            return False

        return True