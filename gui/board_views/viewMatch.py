import math
from gui.board_views.baseBoard import BaseBoard
from algo.cheat import CheatManager


def draw(launcher):
    """
    Dessine la vue graphique principale du match en cours.
    """
    canvas = launcher.getCanvas()
    game = launcher.getGame()
    screenHeight = launcher.getScreenHeight()
    centerX = launcher.getCenterX()

    # Récupération de l'état actuel de la partie
    selectedHex = launcher.getMatchSelectedHex()
    validMoves = launcher.getMatchValidMoves()
    currentCard = launcher.getMatchCurrentCard()

    canvas.unbind("<Button-1>")

    level = game.getCurrentLevel() + 1
    client = launcher.getNetworkClient()
    if client is not None:
        totalBoards = launcher.getOnlineBoardsCount()
        isLocalTurn = (game.getCurrentPlayerIndex() == launcher.getNetworkId())
    else:
        totalBoards = launcher.getLocalBoardsCount()
        isLocalTurn = True
    playerIndex = game.getCurrentPlayerIndex()

    names = [launcher.getPlayerName(), launcher.getPlayer2Name(), launcher.getPlayer3Name(), launcher.getPlayer4Name()]
    colorMap = {
        "light_green": "#B4E046",
        "shocking_pink": "#FA0080"
    }

    rawColors = [
        launcher.getPlayerColor(), launcher.getPlayer2Color(),
        launcher.getPlayer3Color(), launcher.getPlayer4Color()
    ]

    colors = [colorMap.get(c, c) for c in rawColors]

    playerName = names[playerIndex]
    playerColor = colors[playerIndex]

    titleText = launcher.getText("match", "title").format(level, totalBoards)
    launcher.createTitle(60, titleText, fontSize=40)

    # Interface Utilisateur (HUD)
    hudY = screenHeight - 60

    canvas.create_rectangle(
        centerX - 350, hudY - 45, centerX + 350, hudY + 45,
        fill=launcher.getColor("boxBg"),
        outline=playerColor,
        width=5
    )

    statusText = launcher.getText("match", "turnOf").format(playerName.upper())
    canvas.create_text(centerX, hudY - 15, text=statusText, font=("Helvetica", 24, "bold"), fill=playerColor)

    if currentCard is None:
        instruction = launcher.getText("match", "drawPrompt")
    elif selectedHex:
        instruction = launcher.getText("match", "movePrompt")
    else:
        instruction = launcher.getText("match", "selectPrompt")

    canvas.create_text(centerX, hudY + 15, text=instruction, font=("Helvetica", 16, "italic"),
                       fill=launcher.getColor("textSecondary"))

    # Rendu du plateau de jeu
    painter = BaseBoard(launcher)
    hexMap = {}
    boardMatrix = game.getBoardMatrix(level)
    pawnGrid = game.getPawnGrid()

    painter.draw(canvas, hexMap, boardMatrix, pawnGrid=pawnGrid, selectedHex=selectedHex, level=level)

    for hexId, (row, column) in hexMap.items():
        if (row, column) in validMoves:
            canvas.itemconfig(hexId, outline=launcher.getColor("validMove"), width=5)

    # Rendu de la pioche
    centerY = launcher.getCenterY()
    deckCenterX = (centerX + 350 + centerX * 2) // 2
    deckCenterY = centerY

    canvas.create_text(deckCenterX, deckCenterY - 140, text=launcher.getText("match", "deckTitle"),
                       font=("Helvetica", 24, "bold"), fill=launcher.getColor("titleColor"))

    hexRadius = 35
    circleRadius = 80

    deckValues, deckRevealed = game.getPlayerDeck()
    activeIndex = game.getCurrentCardIndex()

    for i in range(6):
        angle = math.radians(i * 60 - 30)
        hexX = deckCenterX + circleRadius * math.cos(angle)
        hexY = deckCenterY + circleRadius * math.sin(angle)

        points = []
        for j in range(6):
            pointAngle = math.radians(j * 60 - 30)
            points.append(hexX + hexRadius * math.cos(pointAngle))
            points.append(hexY + hexRadius * math.sin(pointAngle))

        isRevealed = deckRevealed[i]

        if isRevealed:
            if i == activeIndex:
                canvas.create_polygon(points, fill=launcher.getColor("cardBg"), outline=playerColor, width=5)
                canvas.create_text(hexX, hexY, text=str(deckValues[i]), font=("Helvetica", 26, "bold"), fill=playerColor)
            else:
                canvas.create_polygon(points, fill=launcher.getColor("cardDisabledBg"),
                                      outline=launcher.getColor("textSecondary"), width=2)
                canvas.create_text(hexX, hexY, text=str(deckValues[i]), font=("Helvetica", 20, "bold"),
                                   fill=launcher.getColor("textSecondary"))
        else:
            cardId = canvas.create_polygon(points, fill=launcher.getColor("cardBg"), outline=playerColor, width=3)
            textId = canvas.create_text(hexX, hexY, text="?", font=("Helvetica", 20, "bold"), fill=playerColor)

            if currentCard is None and isLocalTurn:
                def onCardClick(event, index=i):
                    """Gère le clic de l'utilisateur sur une carte face cachée."""
                    client = launcher.getNetworkClient()
                    if client and client.isRunning():
                        client.sendDrawCard(index)
                    else:
                        newCard = game.drawSpecificCard(index)
                        launcher.setMatchCurrentCard(newCard)
                        launcher.showPageMatch()

                canvas.tag_bind(cardId, "<Button-1>", onCardClick)
                canvas.tag_bind(textId, "<Button-1>", onCardClick)

                canvas.tag_bind(cardId, "<Enter>",
                                lambda event, cardIdReference=cardId: canvas.itemconfig(cardIdReference, fill=launcher.getColor("cardDisabledBg")))
                canvas.tag_bind(cardId, "<Leave>",
                                lambda event, cardIdReference=cardId: canvas.itemconfig(cardIdReference, fill=launcher.getColor("cardBg")))

        # Gestion du passage de tour
        def doPassTurn():
            """Passe le tour du joueur actif et réinitialise l'état visuel."""
            client = launcher.getNetworkClient()
            if client and client.isRunning():
                launcher.resetMatchState()
                client.sendPassTurn()
            else:
                game.nextTurn()
                launcher.resetMatchState()
                launcher.showPageMatch()

        if currentCard is not None and game.canSkipTurn() and isLocalTurn:
            launcher.createButton(deckCenterX, deckCenterY + 150, launcher.getText("match", "btnPass"), doPassTurn,
                                  fontSize=20)

    def onClick(event):
        matchCurrentCard = launcher.getMatchCurrentCard()
        matchSelectedHex = launcher.getMatchSelectedHex()
        matchValidMoves = launcher.getMatchValidMoves()

        items = canvas.find_overlapping(event.x - 1, event.y - 1, event.x + 1, event.y + 1)

        hexId = None
        for item in items:
            if item in hexMap:
                hexId = item
                break

        if hexId is None or matchCurrentCard is None:
            return

        row, column = hexMap[hexId]

        if matchSelectedHex is None:
            if pawnGrid[row][column] == playerIndex + 1:
                launcher.setMatchSelectedHex((row, column))
                launcher.setMatchValidMoves(game.getValidMoves(row, column))
                launcher.showPageMatch()

        else:
            startRow, startColumn = matchSelectedHex

            if pawnGrid[row][column] == playerIndex + 1:
                launcher.setMatchSelectedHex((row, column))
                launcher.setMatchValidMoves(game.getValidMoves(row, column))
                launcher.showPageMatch()
                return

            if (startRow, startColumn) == (row, column):
                launcher.resetMatchState()
                launcher.showPageMatch()
                return

            if (row, column) in matchValidMoves:
                isHole = (game.getBoardMatrix(game.getCurrentLevel() + 1)[row][column] == 5)
                success = game.movePawn(startRow, startColumn, row, column)
                if success:
                    launcher.playFootstepSound()
                    launcher.resetMatchState()
                    client = launcher.getNetworkClient()
                    if client and client.isRunning():
                        client.sendMove([startRow, startColumn], [row, column])
                        launcher.showPageMatch()
                        return
                    if game.checkHoles():
                        pawnsBefore = [len(game._Game__players[p].getPawnList()) for p in range(game.getNumPlayers())]
                        game.checkPawns()
                        pawnsAfter = [len(game._Game__players[p].getPawnList()) for p in range(game.getNumPlayers())]
                        eliminationDetected = any(b > 0 and a == 0 for b, a in zip(pawnsBefore, pawnsAfter))
                        winnerId = game.winner()
                        if winnerId is False:
                            game.playerEliminated()
                            if eliminationDetected:
                                launcher.playVoice("player_eliminated")
                            else:
                                launcher.playVoice("area_secured")
                            game.setCurrentLevel(game.getCurrentLevel() + 1)
                            launcher.updateMusic()
                        else:
                            launcher.showPageEnd(winnerId)
                            return
                    else:
                        if isHole:
                            launcher.playVoice("area_secured")
                    launcher.showPageMatch()

    # GESTION DU TYPE DE JOUEUR (HUMAIN OU IA)
    playerType = launcher.getPlayerType(playerIndex)

    aiTimer = [None]

    if playerType != "human":
        import algo.ai as ai

        def executeAITurn():
            """Exécute le coup de l'IA en fonction de sa difficulté."""
            if playerType == "bot_easy":
                ai.moveAIEasy(game)
            elif playerType == "bot_medium":
                ai.moveAIMedium(game)

            launcher.resetMatchState()

            if game.checkHoles():
                game.checkPawns()
                winnerId = game.winner()
                if winnerId is False:
                    game.playerEliminated()
                    game.setCurrentLevel(game.getCurrentLevel() + 1)
                    launcher.updateMusic()
                else:
                    launcher.showPageEnd(winnerId)
                    return

            launcher.showPageMatch()

        aiTimer[0] = canvas.after(1000, executeAITurn)

    else:
        if isLocalTurn:
            canvas.after(50, lambda: canvas.bind("<Button-1>", onClick))

    # BOUTON RETOUR EN BAS
    def goBackToMenu():
        if aiTimer[0] is not None:
            canvas.after_cancel(aiTimer[0])

        launcher.resetMatchState()
        client = launcher.getNetworkClient()
        if client and client.isRunning():
            launcher.showPageOnline()
        else:
            launcher.setLocalRotated(False)
            launcher.setLocalPlaced(False)
            launcher.showPageLocal()

    buttonBackX = launcher.getScreenWidth() - 80
    buttonBackY = screenHeight - 60
    launcher.createButton(buttonBackX, buttonBackY, "❌", lambda: launcher.returnToLobby(), fontSize=35)

    # SYSTÈME DE TRICHE
    def doCheatFill():
        client = launcher.getNetworkClient()
        if client and client.isRunning():
            client.sendCheat()
        else:
            CheatManager(game).fillHoles()

            launcher.resetMatchState()
            launcher.showPageMatch()

    if launcher.isCheatsEnabled():
        launcher.createButton(100, screenHeight - 30, launcher.getText("match", "cheatFill"), doCheatFill, fontSize=12)