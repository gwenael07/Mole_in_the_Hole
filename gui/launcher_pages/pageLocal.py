def draw(launcher):
    """
    Construit l'interface de configuration d'un salon de jeu local (nombre de joueurs, mode de jeu, bots).

    Args:
        launcher (Launcher) : L'instance principale de l'application.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()
    canvas = launcher.getCanvas()

    launcher.createTitle(centerY - 350, launcher.getText("local", "title"))

    playerCount = launcher.getLocalPlayersCount()
    currentMode = launcher.getLocalMode()
    boardCount = launcher.getLocalBoardsCount()
    isRotated = launcher.isLocalRotated()
    isPlaced = launcher.isLocalPlaced()

    playerEntries = {}

    def saveAllNames():
        """Sauvegarde les noms de tous les joueurs saisis dans les champs texte."""
        if 0 in playerEntries: launcher.setPlayerName(playerEntries[0].get())
        if 1 in playerEntries: launcher.setPlayer2Name(playerEntries[1].get())
        if 2 in playerEntries: launcher.setPlayer3Name(playerEntries[2].get())
        if 3 in playerEntries: launcher.setPlayer4Name(playerEntries[3].get())

    boxWidth = 260
    boxHeight = 350
    spacingX = 40
    startX = centerX - (4 * boxWidth + 3 * spacingX) // 2 + (boxWidth // 2)
    boxY = centerY - 100

    availableColors = [
        "red", "blue", "green", "yellow",
        "orange", "pink", "purple", "gray",
        "light_green", "shocking_pink", "brown", "cyan"
    ]

    def cycleColor(playerIndex, currentColor):
        """Passe à la couleur disponible suivante pour le joueur spécifié."""
        saveAllNames()

        usedColors = []
        if playerCount > 0 and playerIndex != 0: usedColors.append(launcher.getPlayerColor())
        if playerCount > 1 and playerIndex != 1: usedColors.append(launcher.getPlayer2Color())
        if playerCount > 2 and playerIndex != 2: usedColors.append(launcher.getPlayer3Color())
        if playerCount > 3 and playerIndex != 3: usedColors.append(launcher.getPlayer4Color())

        currentIndex = (availableColors.index(currentColor) + 1) % len(availableColors)
        nextColor = availableColors[currentIndex]

        while nextColor in usedColors:
            currentIndex = (currentIndex + 1) % len(availableColors)
            nextColor = availableColors[currentIndex]

        if playerIndex == 0:
            launcher.setPlayerColor(nextColor)
        elif playerIndex == 1:
            launcher.setPlayer2Color(nextColor)
        elif playerIndex == 2:
            launcher.setPlayer3Color(nextColor)
        elif playerIndex == 3:
            launcher.setPlayer4Color(nextColor)

        launcher.showPageLocal()

    for i in range(4):
        positionX = startX + i * (boxWidth + spacingX)
        canvas.create_rectangle(
            positionX - boxWidth // 2, boxY - boxHeight // 2,
            positionX + boxWidth // 2, boxY + boxHeight // 2,
            fill=launcher.getColor("boxBg"),
            outline=launcher.getColor("boxOutline"),
            width=3
        )

        if i < playerCount:
            playerTitle = f"{launcher.getText('local', 'player')} {i + 1}"
            launcher.createLabel(positionX, boxY - 140, playerTitle, fontSize=25)

            if i == 0:
                playerName, playerColor = launcher.getPlayerName(), launcher.getPlayerColor()
            elif i == 1:
                playerName, playerColor = launcher.getPlayer2Name(), launcher.getPlayer2Color()
            elif i == 2:
                playerName, playerColor = launcher.getPlayer3Name(), launcher.getPlayer3Color()
            else:
                playerName, playerColor = launcher.getPlayer4Name(), launcher.getPlayer4Color()

            entryField = launcher.createEntry(positionX, boxY - 70, playerName)
            entryField.config(width=12)
            playerEntries[i] = entryField

            launcher.createLabel(positionX, boxY + 10, launcher.getText("local", "colorClick"), fontSize=15)
            launcher.createColorSquare(positionX, boxY + 60, 60, playerColor, lambda p=i, c=playerColor: cycleColor(p, c))

            # LECTURE DE L'ÉTAT DU JOUEUR
            playerType = launcher.getPlayerType(i)
            if playerType == "human":
                texteBot = launcher.getText("local", "btnHuman")
            elif playerType == "bot_easy":
                texteBot = launcher.getText("local", "btnBotEasy")
            else:
                texteBot = launcher.getText("local", "btnBotMedium")

            def toggleBot(pIdx=i):
                saveAllNames()
                launcher.cyclePlayerType(pIdx)
                launcher.showPageLocal()

            launcher.createButton(positionX, boxY + 120, texteBot, toggleBot, fontSize=15)

            if i >= 2:
                def removePlayer():
                    saveAllNames()
                    launcher.setLocalPlayersCount(playerCount - 1)
                    launcher.setPlayerType(playerCount - 1, "human")
                    launcher.showPageLocal()

                launcher.createButton(positionX, boxY + 155, launcher.getText("local", "btnRemove"), removePlayer,
                                      fontSize=15)

        elif i == playerCount:
            def addPlayer():
                """Ajoute un nouveau joueur au salon local."""
                saveAllNames()
                launcher.setLocalPlayersCount(playerCount + 1)
                cycleColor(playerCount, availableColors[-1])

            launcher.createButton(positionX, boxY, "+", addPlayer, fontSize=80)

    def toggleMode():
        """Bascule entre les modes de jeu 'classic' et 'custom'."""
        saveAllNames()
        newMode = "custom" if currentMode == "classic" else "classic"
        launcher.setLocalMode(newMode)
        launcher.setLocalRotated(False)
        launcher.setLocalPlaced(False)
        launcher.showPageLocal()

    modeText = launcher.getText("local", "mode").format(currentMode.upper())
    launcher.createButton(centerX - 200, centerY + 130, modeText, toggleMode, fontSize=25)

    if currentMode == "custom":
        def changeBoards():
            """Incrémente le nombre de plateaux (de 3 à 6) pour le mode personnalisé."""
            saveAllNames()
            nextBoardsCount = boardCount + 1 if boardCount < 6 else 3
            launcher.setLocalBoardsCount(nextBoardsCount)
            launcher.showPageLocal()

        boardsText = launcher.getText("local", "boards").format(boardCount)
        launcher.createButton(centerX + 200, centerY + 130, boardsText, changeBoards, fontSize=25)

    actionYPosition = centerY + 250

    def quickLaunch():
        """Lance une partie instantanément avec des paramètres aléatoires."""
        saveAllNames()
        launcher.startNewGame()
        gameInstance = launcher.getGame()
        gameInstance.quickLaunch()
        launcher.setLocalRotated(True)
        launcher.setLocalPlaced(True)
        launcher.setQuickLaunch(True)
        launcher.showPageMatch()

    launcher.createButton(centerX + 250, actionYPosition, launcher.getText("local", "btnQuick"), quickLaunch, fontSize=25)

    if currentMode == "classic":
        if not isRotated:
            def doRotate():
                """Démarre la phase de rotation des plateaux."""
                saveAllNames()
                launcher.setQuickLaunch(False)
                launcher.startNewGame()
                launcher.showPageRotate()

            launcher.createButton(centerX - 200, actionYPosition, launcher.getText("local", "btnRotate"), doRotate, fontSize=35)
        elif not isPlaced:
            def doPlace():
                """Démarre la phase de placement initial des pions."""
                saveAllNames()
                launcher.setQuickLaunch(False)
                launcher.showPagePlace()

            launcher.createButton(centerX - 200, actionYPosition, launcher.getText("local", "btnPlace"), doPlace, fontSize=35)
        else:
            def doLaunch():
                """Démarre la partie standard après les phases de préparation."""
                saveAllNames()
                launcher.showPageMatch()

            launcher.createButton(centerX - 200, actionYPosition, launcher.getText("local", "btnLaunch"), doLaunch, fontSize=40)

    elif currentMode == "custom":
        if not isPlaced:
            def doPlace():
                """Génère les plateaux aléatoires et démarre le placement des pions."""
                saveAllNames()
                launcher.setQuickLaunch(False)
                launcher.startNewGame()
                launcher.showPagePlace()

            launcher.createButton(centerX - 200, actionYPosition, launcher.getText("local", "btnPlace"), doPlace, fontSize=35)
        else:
            def doLaunch():
                """Démarre la partie personnalisée."""
                saveAllNames()
                launcher.showPageMatch()

            launcher.createButton(centerX - 200, actionYPosition, launcher.getText("local", "btnLaunch"), doLaunch, fontSize=40)

    def goBack():
        """Réinitialise les états de configuration et retourne au menu."""
        launcher.setLocalRotated(False)
        launcher.setLocalPlaced(False)
        launcher.showPagePlay()

    launcher.createButton(centerX, centerY + 330, launcher.getText("local", "btnBack"), goBack, fontSize=20)