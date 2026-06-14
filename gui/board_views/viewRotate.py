from gui.board_views.baseBoard import BaseBoard


def draw(launcher) -> None:
    """
    Vue graphique de la phase d'orientation.
    Permet aux joueurs de configurer la position des trous pour chaque couche (1 à 4)
    avant de commencer le placement des pions.
    """
    canvas = launcher.getCanvas()
    game = launcher.getGame()
    level = launcher.getRotateLevel()

    canvas.unbind("<Button-1>")

    # DESSIN DU PLATEAU (Arrière-plan)
    painter = BaseBoard(launcher)
    hexagonMap = {}
    boardMatrix = game.getBoardMatrix(level)

    painter.draw(canvas, hexagonMap, boardMatrix, level=level)

    # TITRE
    titleText = launcher.getText("rotate", "title").format(level)
    launcher.createTitle(80, titleText, fontSize=50)

    def rotate(reverse: bool) -> None:
        client = launcher.getNetworkClient()
        if client and client.isRunning():
            client.sendTurnBoard(level, reverse)
        else:
            game.turnBoard(level, reverse=reverse)
            launcher.showPageRotate()

    def validateStep() -> None:
        client = launcher.getNetworkClient()
        isOnline = client is not None
        totalBoards = launcher.getOnlineBoardsCount() if isOnline else launcher.getLocalBoardsCount()

        if level < totalBoards:
            if client and client.isRunning():
                client.sendChangeOrientationBoard(level + 1)
            else:
                launcher.setRotateLevel(level + 1)
                launcher.showPageRotate()
        else:
            if client and client.isRunning():
                client.sendFinishOrientation()
            else:
                launcher.setLocalRotated(True)
                launcher.showPageLocal()

    # INTERFACE UTILISATEUR
    centerX = launcher.getCenterX()
    screenHeight = launcher.getScreenHeight()
    controlY = screenHeight - 100

    buttonLeft = launcher.getText("rotate", "btnLeft")
    buttonRight = launcher.getText("rotate", "btnRight")
    buttonValidate = launcher.getText("rotate", "btnValidate")

    launcher.createButton(centerX - 300, controlY, buttonLeft, lambda: rotate(True), fontSize=30)
    launcher.createButton(centerX, controlY, buttonValidate, validateStep, fontSize=35)
    launcher.createButton(centerX + 300, controlY, buttonRight, lambda: rotate(False), fontSize=30)

    # BOUTON RETOUR EN BAS À DROITE
    def goBackToLocal() -> None:
        launcher.setLocalRotated(False)
        launcher.showPageLocal()

    buttonBackX = launcher.getScreenWidth() - 80
    buttonBackY = screenHeight - 60
    launcher.createButton(buttonBackX, buttonBackY, "❌", lambda: launcher.returnToLobby(), fontSize=35)
