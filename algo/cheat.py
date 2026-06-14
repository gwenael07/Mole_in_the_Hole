class CheatManager:
    def __init__(self, game):
        """
        Parametres
        ----------
        game : Game
            Instance du jeu sur laquelle appliquer les cheats.
        """
        self.__game = game

    def fillHoles(self):
        """Remplit les trous vides du plateau en y déplaçant les pions disponibles hors des trous.

        La méthode scanne le plateau pour trouver les cases de type "trou" (valeur 5) 
        qui sont vides. Si plus d'un trou est vide, elle garde le premier intact et 
        tente de remplir tous les autres trous identifiés en y déplaçant un à un les 
        pions des joueurs situés sur des cases normales.

        Cette opération met à jour la position du pion dans la liste du joueur 
        concerné ainsi que dans la grille globale `pawnGrid`.

        Args:
            self: L'instance de la classe actuelle (qui possède l'attribut `__game`).

        Returns:
            None

        Raises:
            Exception: Les erreurs potentielles lors de l'appel à `movePawn` sur 
                l'objet joueur sont interceptées de manière silencieuse (pass).
        """
        game = self.__game
        level = game.getCurrentLevel()
        board = game.getBoardMatrix(level + 1)
        pawnGrid = game.getPawnGrid()

        emptyHoles = []
        for row in range(9):
            for column in range(9):
                if board[row][column] == 5 and pawnGrid[row][column] is None:
                    emptyHoles.append((row, column))

        if len(emptyHoles) > 1:
            holesToFill = emptyHoles[1:]
            for row in range(9):
                for column in range(9):
                    if board[row][column] != 5 and pawnGrid[row][column] is not None:
                        if holesToFill:
                            destinationRow, destinationColumn = holesToFill.pop(0)
                            pawnId = pawnGrid[row][column]
                            try:
                                game._Game__players[pawnId - 1].movePawn(row, column, destinationRow, destinationColumn)
                            except:
                                pass
                            pawnGrid[destinationRow][destinationColumn] = pawnId
                            pawnGrid[row][column] = None
