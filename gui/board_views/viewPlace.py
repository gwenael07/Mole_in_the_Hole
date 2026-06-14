from gui.board_views.baseBoard import BaseBoard
import algo.ai as ai

def draw(launcher):
    """
    Vue graphique de la phase de placement.
    Permet aux joueurs de poser leurs pions tour à tour sur les cases valides du plateau
    jusqu'à ce que tous les joueurs aient posé leurs pions.
    """
    canvas = launcher.getCanvas()
    game = launcher.getGame()
    screenHeight = launcher.getScreenHeight()
    centerX = launcher.getCenterX()

    canvas.unbind("<Button-1>")

    # VERIFICATION DE L'ÉTAT DU PLACEMENT
    numPlayers = game.getNumPlayers()
    maxPawns = game.getMaxPawns()
    totalPawnsNeeded = numPlayers * maxPawns

    pawnGrid = game.getPawnGrid()
    currentPawns = sum(1 for row in pawnGrid for cell in row if cell is not None)
    isPlacementDone = (currentPawns >= totalPawnsNeeded)

    # GESTION DE L'INTERFACE VISUELLE
    titleText = launcher.getText("place", "title")
    launcher.createTitle(60, titleText, fontSize=40)

    if not isPlacementDone:
        playerIndex = game.getCurrentPlayerIndex()

        names = [
            launcher.getPlayerName(), launcher.getPlayer2Name(),
            launcher.getPlayer3Name(), launcher.getPlayer4Name()
        ]
        rawColors = [
            launcher.getPlayerColor(), launcher.getPlayer2Color(),
            launcher.getPlayer3Color(), launcher.getPlayer4Color()
        ]

        colorMap = {
            "light_green": "#B4E046",
            "shocking_pink": "#FA0080"
        }
        colors = [colorMap.get(c, c) for c in rawColors]

        playerName = names[playerIndex]
        playerColor = colors[playerIndex]

        pawnsPlaced = sum(1 for row in pawnGrid for cell in row if cell == playerIndex + 1)
        pawnsLeft = maxPawns - pawnsPlaced

        hudY = screenHeight - 60

        canvas.create_rectangle(
            centerX - 350, hudY - 45, centerX + 350, hudY + 45,
            fill=launcher.getColor("boxBg"),
            outline=playerColor,
            width=5
        )

        textTurn = launcher.getText("place", "turn").format(playerName.upper())
        canvas.create_text(centerX, hudY - 12, text=textTurn, font=("Helvetica", 24, "bold"), fill=playerColor)

        textRemaining = launcher.getText("place", "remaining").format(pawnsLeft, maxPawns)
        canvas.create_text(centerX, hudY + 18, text=textRemaining, font=("Helvetica", 16, "bold"),
                           fill=launcher.getColor("titleColor"))

    # DESSIN DU PLATEAU
    painter = BaseBoard(launcher)
    hexagonMap = {}

    currentLevel = game.getCurrentLevel() + 1
    boardMatrix = game.getBoardMatrix(currentLevel)

    painter.draw(canvas, hexagonMap, boardMatrix, pawnGrid=pawnGrid, level=currentLevel)

    def onClick(event):
        if isPlacementDone:
            return

        items = canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)

        hexId = None
        for item in items:
            if item in hexagonMap:
                hexId = item
                break

        if hexId is not None:
            row, column = hexagonMap[hexId]

            client = launcher.getNetworkClient()
            if client and client.isRunning():
                client.sendPlacePawn(row, column)
            else:
                success = game.placePawn(row, column)
                if success:
                    launcher.showPagePlace()

    # LOGIQUE IA
    aiTimer = [None]

    if not isPlacementDone:
        isBot = launcher.isPlayerBot(playerIndex)
        if isBot:
            def executeAIPlace():
                """Exécute la fonction de placement de l'IA et met à jour la vue."""
                ai.placeAI(game)
                launcher.showPagePlace()

            aiTimer[0] = canvas.after(400, executeAIPlace)
        else:
            canvas.after(50, lambda: canvas.bind("<Button-1>", onClick))

    # BOUTON DE FIN DE PLACEMENT
    if isPlacementDone:
        def finishPlacement():
            client = launcher.getNetworkClient()
            if not (client and client.isRunning()):
                canvas.unbind("<Button-1>")
                launcher.setLocalPlaced(True)
                launcher.showPageLocal()

        buttonText = launcher.getText("place", "btnValidate")
        launcher.createButton(centerX, screenHeight - 70, buttonText, finishPlacement, fontSize=35)

    # BOUTON RETOUR
    def goBackToLocal():
        if aiTimer[0] is not None:
            canvas.after_cancel(aiTimer[0])

        launcher.showPageLocal()

    buttonBackX = launcher.getScreenWidth() - 80
    buttonBackY = screenHeight - 60
    launcher.createButton(buttonBackX, buttonBackY, "❌", lambda: launcher.returnToLobby(), fontSize=35)
