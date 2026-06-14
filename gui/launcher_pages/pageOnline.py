import threading
import time
from network.server import GameServer
from network.client import NetworkClient
from network.LANDiscovery import LANDiscoverer


def draw(launcher):
    """
    Gère l'affichage conditionnel de la page multijoueur.
    """
    networkClient = launcher.getNetworkClient()

    if not networkClient or not networkClient.isRunning():
        drawDiscovery(launcher)
    else:
        drawLobby(launcher)


def drawDiscovery(launcher):
    """
    Affiche l'écran de recherche de parties sur le réseau local ou de création de serveur.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()
    canvas = launcher.getCanvas()

    launcher.createTitle(centerY - 380, launcher.getText("online", "title"))

    networkRole = launcher.getNetworkRole()

    def setRole(newRole):
        if newRole == "host" and getattr(launcher, "_lanDiscoverer", None):
            launcher._lanDiscoverer.stopListening()
        launcher.setNetworkRole(newRole)
        launcher.showPageOnline()

    colorHost = launcher.getColor("btnHover") if networkRole == "host" else launcher.getColor("btnNormal")
    colorClient = launcher.getColor("btnHover") if networkRole == "client" else launcher.getColor("btnNormal")

    hostButton = launcher.createButton(centerX - 150, centerY - 310, launcher.getText("online", "btnHost"),
                                       lambda: setRole("host"), fontSize=30)
    canvas.itemconfig(hostButton, fill=colorHost)

    clientButton = launcher.createButton(centerX + 150, centerY - 310, launcher.getText("online", "btnJoin"),
                                         lambda: setRole("client"), fontSize=30)
    canvas.itemconfig(clientButton, fill=colorClient)

    entryContainer = {}
    availableColors = [
        "red", "blue", "green", "yellow",
        "orange", "pink", "purple", "gray",
        "light_green", "shocking_pink", "brown", "cyan"
    ]

    def cycleColor():
        if "nameEntry" in entryContainer:
            launcher.setPlayerName(entryContainer["nameEntry"].get())
        currentColor = launcher.getPlayerColor()
        currentIndex = (availableColors.index(currentColor) + 1) % len(availableColors)
        launcher.setPlayerColor(availableColors[currentIndex])
        launcher.showPageOnline()

    entryContainer["nameEntry"] = launcher.createPlayerBox(
        positionX=centerX - 250, positionY=centerY + 20,
        titleText=launcher.getText("online", "profileTitle"),
        defaultName=launcher.getPlayerName(),
        currentColor=launcher.getPlayerColor(),
        onColorCycle=cycleColor
    )

    def connectToServer(targetIp):
        launcher.setPlayerName(entryContainer["nameEntry"].get())

        def messageHandler(incomingMessage):
            canvas.after(0, lambda: launcher.onNetworkMessageReceived(incomingMessage))

        newClient = NetworkClient(targetIp, 5000, messageHandler)
        if newClient.connect():
            launcher.setNetworkClient(newClient)
            launcher.clearCanvas()
            launcher.drawBackground()
            launcher.createTitle(centerY, launcher.getText("online", "enteringLobby"), fontSize=40)
        else:
            failText = launcher.getText("online", "connectFail").format(targetIp)
            launcher.createLabel(centerX, centerY + 300, failText, fontSize=20)
            canvas.itemconfig(canvas.find_all()[-1], fill="red")

    networkSectionX = centerX + 250
    networkSectionY = centerY + 20

    if networkRole == "host":
        def startHost():
            launcher.setPlayerName(entryContainer["nameEntry"].get())
            serverConfig = {
                "mode": launcher.getOnlineMode(),
                "boards": launcher.getOnlineBoardsCount(),
                "theme": launcher.getCurrentThemeName()
            }
            gameServer = GameServer(serverConfig)
            launcher.setGameServer(gameServer)
            threading.Thread(target=gameServer.start, daemon=True).start()
            time.sleep(0.5)
            connectToServer("127.0.0.1")

        launcher.createButton(networkSectionX, centerY + 20, launcher.getText("online", "btnCreate"), startHost,
                              fontSize=35)

    elif networkRole == "client":
        if not getattr(launcher, "_lanDiscoverer", None):
            def onGameFound(discoveredIp, gameInfo):
                launcher.addDiscoveredGame(discoveredIp, gameInfo)
                canvas.after(0, launcher.showPageOnline)

            launcher._lanDiscoverer = LANDiscoverer(onGameFound)

        launcher._lanDiscoverer.startListening()

        launcher.createLabel(networkSectionX, networkSectionY - 120, launcher.getText("online", "discoveredGames"),
                             fontSize=25)

        listYPosition = networkSectionY - 60
        discoveredGamesList = launcher.getDiscoveredGames()
        if not discoveredGamesList:
            launcher.createLabel(networkSectionX, listYPosition, launcher.getText("online", "searching"), fontSize=20)
        else:
            for discoveredIp, gameInfo in discoveredGamesList.items():
                buttonText = f"{gameInfo.get('name', 'Game')} ({discoveredIp})"
                launcher.createButton(networkSectionX, listYPosition, buttonText,
                                      lambda target=discoveredIp: connectToServer(target), fontSize=25)
                listYPosition += 50

    def goBack():
        if "nameEntry" in entryContainer:
            launcher.setPlayerName(entryContainer["nameEntry"].get())
        if getattr(launcher, "_lanDiscoverer", None):
            launcher._lanDiscoverer.stopListening()
        
        # Reset local defaults
        launcher.setPlayerName("Player 1")
        launcher.setPlayer2Name("Player 2")
        launcher.setPlayer3Name("Player 3")
        launcher.setPlayer4Name("Player 4")
        launcher.setPlayerColor("red")
        launcher.setPlayer2Color("blue")
        launcher.setPlayer3Color("green")
        launcher.setPlayer4Color("yellow")

        launcher.showPagePlay()

    launcher.createButton(centerX, centerY + 350, launcher.getText("online", "btnBack"), goBack, fontSize=20)


def drawLobby(launcher):
    """
    Affiche le salon d'attente multijoueur en ligne avec synchronisation des joueurs et des paramètres.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()
    canvas = launcher.getCanvas()

    launcher.createTitle(centerY - 350, launcher.getText("online", "title"))

    networkClient = launcher.getNetworkClient()
    onlineLobbyData = launcher.getOnlineLobbyData()
    lobbyPlayers = onlineLobbyData.get("players", {})
    currentMode = onlineLobbyData.get("mode", "classic")
    boardCount = onlineLobbyData.get("boards", 4)
    localPlayerId = str(launcher.getNetworkId())
    isLocalHost = (localPlayerId == "0")

    boxWidth = 260
    spacingX = 40
    startX = centerX - (4 * boxWidth + 3 * spacingX) // 2 + (boxWidth // 2)
    boxY = centerY - 80

    entryContainer = {}
    availableColors = [
        "red", "blue", "green", "yellow",
        "orange", "pink", "purple", "gray",
        "light_green", "shocking_pink", "brown", "cyan"
    ]


    colorsUsedByOlderPlayers = [playerInfo.get("color") for playerId, playerInfo in lobbyPlayers.items() if
                                int(playerId) < int(localPlayerId)]

    if launcher.getPlayerColor() in colorsUsedByOlderPlayers:
        allUsedColors = [playerInfo.get("color") for playerId, playerInfo in lobbyPlayers.items() if
                         playerId != localPlayerId]
        for colorCandidate in availableColors:
            if colorCandidate not in allUsedColors:
                launcher.setPlayerColor(colorCandidate)
                networkClient.sendProfile(launcher.getPlayerName(), colorCandidate)
                break

    def cycleColor(targetId):
        if targetId == localPlayerId:
            if "nameEntry" in entryContainer:
                launcher.setPlayerName(entryContainer["nameEntry"].get())

            currentColor = launcher.getPlayerColor()
            currentlyUsedByOthers = [playerInfo.get("color") for playerId, playerInfo in lobbyPlayers.items() if
                                     playerId != localPlayerId]

            currentIndex = (availableColors.index(currentColor) + 1) % len(availableColors)
            newColor = availableColors[currentIndex]

            while newColor in currentlyUsedByOthers:
                currentIndex = (currentIndex + 1) % len(availableColors)
                newColor = availableColors[currentIndex]

            launcher.setPlayerColor(newColor)
            networkClient.sendProfile(launcher.getPlayerName(), newColor)
            launcher.showPageOnline()

    for i in range(4):
        positionX = startX + i * (boxWidth + spacingX)
        playerStringIndex = str(i)

        if playerStringIndex in lobbyPlayers:
            playerData = lobbyPlayers[playerStringIndex]
            playerName = playerData.get("name", f"Player {i + 1}")
            playerColor = playerData.get("color", "white")

            if playerStringIndex == "0" and localPlayerId == "0":
                boxTitle = launcher.getText("online", "hostYou")
            elif playerStringIndex == localPlayerId:
                boxTitle = launcher.getText("online", "you")
            else:
                boxTitle = f"{launcher.getText('online', 'player')} {i + 1}"

            if playerStringIndex == localPlayerId:
                entryContainer["nameEntry"] = launcher.createPlayerBox(
                    positionX=positionX, positionY=boxY, titleText=boxTitle,
                    defaultName=launcher.getPlayerName(),
                    currentColor=launcher.getPlayerColor(),
                    onColorCycle=lambda idx=playerStringIndex: cycleColor(idx)
                )
            else:
                launcher.createPlayerBox(
                    positionX=positionX, positionY=boxY, titleText=boxTitle,
                    defaultName=playerName,
                    currentColor=playerColor,
                    onColorCycle=lambda: None
                )
        else:
            canvas.create_rectangle(positionX - boxWidth // 2, boxY - 175, positionX + boxWidth // 2, boxY + 175,
                                    fill=launcher.getColor("boxBg"), outline=launcher.getColor("boxOutline"), width=3)

            waitingText = launcher.getText("online", "waitingPlayer").format(i + 1)
            launcher.createLabel(positionX, boxY, waitingText, fontSize=20)

    def saveMyName(event):
        if "nameEntry" in entryContainer:
            newName = entryContainer["nameEntry"].get()
            launcher.setPlayerName(newName)
            networkClient.sendProfile(newName, launcher.getPlayerColor())

    if "nameEntry" in entryContainer:
        entryContainer["nameEntry"].bind("<FocusOut>", saveMyName)
        entryContainer["nameEntry"].bind("<Return>", saveMyName)

    if isLocalHost:
        def toggleMode():
            newMode = "custom" if currentMode == "classic" else "classic"
            networkClient.sendUpdateSettings(newMode, boardCount)

        modeText = launcher.getText("local", "mode").format(currentMode.upper())
        launcher.createButton(centerX - 200, centerY + 130, modeText, toggleMode, fontSize=25)

        if currentMode == "custom":
            def changeBoards():
                nextBoardsCount = boardCount + 1 if boardCount < 6 else 3
                networkClient.sendUpdateSettings(currentMode, nextBoardsCount)

            boardsText = launcher.getText("local", "boards").format(boardCount)
            launcher.createButton(centerX + 200, centerY + 130, boardsText, changeBoards, fontSize=25)
    else:
        modeText = launcher.getText("local", "mode").format(currentMode.upper())
        launcher.createLabel(centerX - 200, centerY + 130, modeText, fontSize=25)
        if currentMode == "custom":
            boardsText = launcher.getText("local", "boards").format(boardCount)
            launcher.createLabel(centerX + 200, centerY + 130, boardsText, fontSize=25)

    def leaveLobby():
        networkClient.close()
        launcher.setNetworkClient(None)
        gameServer = launcher.getGameServer()
        if gameServer:
            gameServer.stop()
            launcher.setGameServer(None)
        launcher.setOnlineLobbyData({})
        
        # Reset local defaults
        launcher.setPlayerName("Player 1")
        launcher.setPlayer2Name("Player 2")
        launcher.setPlayer3Name("Player 3")
        launcher.setPlayer4Name("Player 4")
        launcher.setPlayerColor("red")
        launcher.setPlayer2Color("blue")
        launcher.setPlayer3Color("green")
        launcher.setPlayer4Color("yellow")

        launcher.showPageOnline()

    launcher.createButton(centerX - 200, centerY + 250, launcher.getText("online", "btnLeave"), leaveLobby, fontSize=25)

    if isLocalHost:
        def launchConfig():
            if len(lobbyPlayers) >= 2:
                networkClient.sendStartGame()

        def launchQuick():
            if len(lobbyPlayers) >= 2:
                networkClient.sendNetworkQuickLaunch()

        colorLaunchButton = launcher.getColor("btnNormal") if len(lobbyPlayers) >= 2 else "gray"

        configButton = launcher.createButton(centerX + 200, centerY + 220, launcher.getText("online", "btnConfig"),
                                             launchConfig, fontSize=30)
        canvas.itemconfig(configButton, fill=colorLaunchButton)

        quickButton = launcher.createButton(centerX + 200, centerY + 280, launcher.getText("online", "btnQuick"),
                                            launchQuick, fontSize=30)
        canvas.itemconfig(quickButton, fill=colorLaunchButton)
    else:
        launcher.createLabel(centerX + 200, centerY + 250, launcher.getText("online", "waitingHost"), fontSize=25)