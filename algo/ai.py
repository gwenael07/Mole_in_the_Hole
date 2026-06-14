from random import randint, shuffle


def placeAI(game):
    """Positionne aléatoirement un pion de l'IA sur une case valide du plateau.

    La méthode cherche une case disponible qui n'est ni vide (None), ni un trou (5),
    et qui ne contient pas déjà un autre pion.

    Args:
        game: L'instance du jeu contenant l'état actuel et les méthodes de manipulation.

    Returns:
        bool: True si le pion a été placé avec succès, False sinon.
    """
    level = game.getCurrentLevel() + 1
    boardMatrix = game.getBoardMatrix(level)
    pawnGrid = game.getPawnGrid()

    size = len(boardMatrix)
    row = randint(0, size - 1)
    column = randint(0, size - 1)

    while boardMatrix[row][column] is None or boardMatrix[row][column] == 5 or pawnGrid[row][column] is not None:
        row = randint(0, size - 1)
        column = randint(0, size - 1)

    return game.placePawn(row, column)


def moveAIEasy(game):
    """Gère le tour de l'IA en mode facile.

    L'IA pioche une carte, sélectionne un de ses pions au hasard, puis choisit
    une destination de manière purement aléatoire parmi ses mouvements valides.
    Si aucun mouvement n'est possible pour l'ensemble de ses pions, elle passe son tour.

    Args:
        game: L'instance du jeu contenant l'état actuel et les méthodes de manipulation.

    Returns:
        bool: True si un déplacement a été effectué, False si le tour a été passé.
    """
    game.drawCard()
    playerIndex = game.getCurrentPlayerIndex()
    pawnGrid = game.getPawnGrid()
    pawnList = []

    level = game.getCurrentLevel() + 1
    size = len(game.getBoardMatrix(level))

    for row in range(size):
        for column in range(size):
            if pawnGrid[row][column] == playerIndex + 1:
                pawnList.append((row, column))

    if not pawnList:
        game.nextTurn()
        return False

    shuffle(pawnList)

    for pawn in pawnList:
        startRow, startColumn = pawn
        validMoves = game.getValidMoves(startRow, startColumn)

        if validMoves:
            endRow, endColumn = validMoves[randint(0, len(validMoves) - 1)]
            return game.movePawn(startRow, startColumn, endRow, endColumn)

    game.nextTurn()
    return False


def moveAIMedium(game):
    """Gère le tour de l'IA en mode intermédiaire avec une logique de priorité.

    L'IA pioche une carte et applique la stratégie suivante :
    1. Elle privilégie le déplacement des pions qui ne sont pas encore dans un trou (5).
    2. Pour ces pions, elle tente en priorité absolue d'aller vers une case "trou" (5).
    3. Si aucun mouvement vers un trou n'est possible, elle choisit un autre mouvement valide.
    4. En dernier recours, si aucun pion extérieur ne peut bouger, elle déplace un de ses pions déjà situés dans un trou.

    Si aucun mouvement n'est possible, elle passe son tour.

    Args:
        game: L'instance du jeu contenant l'état actuel et les méthodes de manipulation.

    Returns:
        bool: True si un déplacement a été effectué, False si le tour a été passé.
    """
    game.drawCard()
    playerIndex = game.getCurrentPlayerIndex()
    pawnGrid = game.getPawnGrid()
    level = game.getCurrentLevel() + 1
    boardMatrix = game.getBoardMatrix(level)
    pawnList = []

    size = len(boardMatrix)

    for row in range(size):
        for column in range(size):
            if pawnGrid[row][column] == playerIndex + 1:
                pawnList.append((row, column))

    if not pawnList:
        game.nextTurn()
        return False

    pawnsInHoles = []
    pawnsOutsideHoles = []

    for pawn in pawnList:
        row, column = pawn
        if boardMatrix[row][column] == 5:
            pawnsInHoles.append(pawn)
        else:
            pawnsOutsideHoles.append(pawn)

    shuffle(pawnsOutsideHoles)

    for pawn in pawnsOutsideHoles:
        startRow, startColumn = pawn
        validMoves = game.getValidMoves(startRow, startColumn)

        if validMoves:
            movesToHoles = []
            otherMoves = []

            for endRow, endColumn in validMoves:
                if boardMatrix[endRow][endColumn] == 5:
                    movesToHoles.append((endRow, endColumn))
                else:
                    otherMoves.append((endRow, endColumn))

            if movesToHoles:
                endRow, endColumn = movesToHoles[randint(0, len(movesToHoles) - 1)]
                return game.movePawn(startRow, startColumn, endRow, endColumn)
            elif otherMoves:
                endRow, endColumn = otherMoves[randint(0, len(otherMoves) - 1)]
                return game.movePawn(startRow, startColumn, endRow, endColumn)

    shuffle(pawnsInHoles)

    for pawn in pawnsInHoles:
        startRow, startColumn = pawn
        validMoves = game.getValidMoves(startRow, startColumn)

        if validMoves:
            endRow, endColumn = validMoves[randint(0, len(validMoves) - 1)]
            return game.movePawn(startRow, startColumn, endRow, endColumn)

    game.nextTurn()
    return False
