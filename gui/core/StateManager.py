class StateManager:
    """
    Gère toutes les variables d'état (joueurs, lobby, jeu en cours, réseau).
    """

    def __init__(self):
        # VARIABLES D'ÉTAT : JOUEURS
        self.__playerTypes = {0: "human", 1: "human", 2: "human", 3: "human"}

        self.__playerName = "Player 1"
        self.__playerColor = "red"
        self.__player2Name = "Player 2"
        self.__player2Color = "blue"
        self.__player3Name = "Player 3"
        self.__player3Color = "green"
        self.__player4Name = "Player 4"
        self.__player4Color = "yellow"

        # VARIABLES D'ÉTAT : LOBBY LOCAL
        self.__localPlayersCount = 2
        self.__localMode = "classic"
        self.__localBoardsCount = 4
        self.__localIsRotated = False
        self.__localIsPlaced = False
        self.__isQuickLaunch = False

        # VARIABLES D'ÉTAT : ONLINE LOBBY
        self.__onlinePlayersCount = 2
        self.__onlineMode = "classic"
        self.__onlineBoardsCount = 4
        self.__onlineIsRotated = False
        self.__onlineIsPlaced = False

        # VARIABLES D'ÉTAT : RÉSEAU (ONLINE)
        self.__networkRole = "host"
        self.__serverIp = "127.0.0.1"
        self.__networkClient = None
        self.__gameServer = None
        self.__discoveredGames = {}
        self._lanDiscoverer = None

        self.__networkId = 0
        self.__onlineLobbyData = {}

        # VARIABLES D'ÉTAT : MOTEUR DE JEU
        self.__game = None
        self.__rotateLevel = 1
        self.__matchSelectedHex = None
        self.__matchValidMoves = []
        self.__matchCurrentCard = None
        self.__cheatsEnabled = False

    # JOUEURS
    def getPlayerType(self, index):
        return self.__playerTypes.get(index, "human")

    def setPlayerType(self, index, playerType):
        self.__playerTypes[index] = playerType

    def isPlayerBot(self, index):
        return self.getPlayerType(index) != "human"

    def cyclePlayerType(self, index):
        types = ["human", "bot_easy", "bot_medium"]
        current = self.getPlayerType(index)
        nextIndex = (types.index(current) + 1) % len(types)
        self.__playerTypes[index] = types[nextIndex]

    def getPlayerName(self):
        return self.__playerName

    def setPlayerName(self, targetName):
        self.__playerName = targetName

    def getPlayerColor(self):
        return self.__playerColor

    def setPlayerColor(self, targetColor):
        self.__playerColor = targetColor

    def getPlayer2Name(self):
        return self.__player2Name

    def setPlayer2Name(self, targetName):
        self.__player2Name = targetName

    def getPlayer2Color(self):
        return self.__player2Color

    def setPlayer2Color(self, targetColor): self.__player2Color = targetColor

    def getPlayer3Name(self):
        return self.__player3Name

    def setPlayer3Name(self, targetName):
        self.__player3Name = targetName

    def getPlayer3Color(self):
        return self.__player3Color

    def setPlayer3Color(self, targetColor):
        self.__player3Color = targetColor

    def getPlayer4Name(self):
        return self.__player4Name

    def setPlayer4Name(self, targetName):
        self.__player4Name = targetName

    def getPlayer4Color(self):
        return self.__player4Color

    def setPlayer4Color(self, targetColor): self.__player4Color = targetColor

    # LOCAL LOBBY
    def getLocalMode(self):
        return self.__localMode

    def setLocalMode(self, targetMode):
        self.__localMode = targetMode

    def getLocalBoardsCount(self):
        return self.__localBoardsCount

    def setLocalBoardsCount(self, targetCount):
        self.__localBoardsCount = targetCount

    def getLocalPlayersCount(self):
        return self.__localPlayersCount

    def setLocalPlayersCount(self, targetCount):
        self.__localPlayersCount = targetCount

    def isLocalRotated(self):
        return self.__localIsRotated

    def setLocalRotated(self, rotationState):
        self.__localIsRotated = rotationState

    def isLocalPlaced(self):
        return self.__localIsPlaced

    def setLocalPlaced(self, placementState):
        self.__localIsPlaced = placementState

    def isQuickLaunch(self):
        return self.__isQuickLaunch

    def setQuickLaunch(self, state):
        self.__isQuickLaunch = state

    # ONLINE LOBBY
    def getOnlineMode(self):
        return self.__onlineMode

    def setOnlineMode(self, targetMode):
        self.__onlineMode = targetMode

    def getOnlineBoardsCount(self):
        return self.__onlineBoardsCount

    def setOnlineBoardsCount(self, targetCount):
        self.__onlineBoardsCount = targetCount

    def getOnlinePlayersCount(self):
        return self.__onlinePlayersCount

    def setOnlinePlayersCount(self, targetCount):
        self.__onlinePlayersCount = targetCount

    # NETWORK
    def getNetworkId(self):
        return self.__networkId

    def setNetworkId(self, networkId):
        self.__networkId = networkId

    def getOnlineLobbyData(self):
        return self.__onlineLobbyData

    def setOnlineLobbyData(self, lobbyData):
        self.__onlineLobbyData = lobbyData

    def getNetworkRole(self):
        return self.__networkRole

    def setNetworkRole(self, targetRole):
        self.__networkRole = targetRole

    def getDiscoveredGames(self):
        return self.__discoveredGames

    def addDiscoveredGame(self, targetIp, gameInfo):
        self.__discoveredGames[targetIp] = gameInfo

    def getNetworkClient(self):
        return self.__networkClient

    def setNetworkClient(self, targetClient):
        self.__networkClient = targetClient

    def getGameServer(self):
        return self.__gameServer

    def setGameServer(self, targetServer):
        self.__gameServer = targetServer

    def getLanDiscoverer(self):
        return self._lanDiscoverer

    def setLanDiscoverer(self, discoverer):
        self._lanDiscoverer = discoverer

    # JEU EN COURS
    def getGame(self):
        return self.__game

    def setGame(self, game):
        self.__game = game

    def getRotateLevel(self):
        return self.__rotateLevel

    def setRotateLevel(self, targetLevel):
        self.__rotateLevel = targetLevel

    def getMatchSelectedHex(self):
        return self.__matchSelectedHex

    def setMatchSelectedHex(self, hexagonCoordinates):
        self.__matchSelectedHex = hexagonCoordinates

    def getMatchValidMoves(self):
        return self.__matchValidMoves

    def setMatchValidMoves(self, validMovesList):
        self.__matchValidMoves = validMovesList

    def getMatchCurrentCard(self):
        return self.__matchCurrentCard

    def setMatchCurrentCard(self, drawnCard):
        self.__matchCurrentCard = drawnCard
        if self.__game:
            self.__game.setCurrentCard(drawnCard)

    # OPTIONS (CHEATS)
    def isCheatsEnabled(self):
        return self.__cheatsEnabled

    def setCheatsEnabled(self, state):
        self.__cheatsEnabled = state
