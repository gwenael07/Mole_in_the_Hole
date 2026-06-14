import os
import tkinter as tk

from gui.core.StateManager import StateManager
from gui.core.ResourceManager import ResourceManager
from gui.core.UIFactory import UIFactory
from gui.core.NetworkController import NetworkController
from gui.core.Navigator import Navigator


class GUICore:
    """
    Classe principale du programme.
    Agit comme une Façade pour les 5 Managers : StateManager, ResourceManager, UIFactory, NetworkController, Navigator.
    Gère la fenêtre Tkinter et le canvas global.
    """

    def __init__(self, rootWindow):
        self.__rootWindow = rootWindow
        self.__rootWindow.title("Mole in the Hole")

        # CONFIGURATION FENÊTRE
        self.__rootWindow.attributes('-fullscreen', True)
        self.__rootWindow.bind("<Escape>", lambda event: self.quitGame())
        self.__screenWidth = self.__rootWindow.winfo_screenwidth()
        self.__screenHeight = self.__rootWindow.winfo_screenheight()

        # Canvas global
        self.__canvas = tk.Canvas(self.__rootWindow, width=self.__screenWidth, height=self.__screenHeight, bg="#2c3e50")
        self.__canvas.pack(fill="both", expand=True)

        # INITIALISATION DES MANAGERS
        self.stateManager = StateManager()
        self.resourceManager = ResourceManager(self)
        self.uiFactory = UIFactory(self)
        self.networkController = NetworkController(self)
        self.navigator = Navigator(self)

        # INITIALISATION
        self.resourceManager.loadResources()
        self.navigator.showPageMain()
        self.resourceManager.updateMusic()

    # UTILITAIRES DE BASE
    def getRootWindow(self):
        return self.__rootWindow

    def getCanvas(self):
        return self.__canvas

    def getScreenWidth(self):
        return self.__screenWidth

    def getScreenHeight(self):
        return self.__screenHeight

    def getCenterX(self):
        return self.__screenWidth // 2

    def getCenterY(self):
        return self.__screenHeight // 2

    # RESOURCE MANAGER
    def loadResources(self):
        self.resourceManager.loadResources()

    def getCurrentLang(self):
        return self.resourceManager.getCurrentLang()

    def setLanguage(self, langCode):
        self.resourceManager.setLanguage(langCode)

    def getText(self, targetPage, textKey):
        return self.resourceManager.getText(targetPage, textKey)

    def getColor(self, elementKey):
        return self.resourceManager.getColor(elementKey)

    def getThemesList(self):
        return self.resourceManager.getThemesList()

    def getCurrentThemeName(self):
        return self.resourceManager.getCurrentThemeName()

    def setThemeName(self, targetThemeName):
        self.resourceManager.setThemeName(targetThemeName)

    def getTextureFolder(self):
        return self.resourceManager.getTextureFolder()

    def getEarthColor(self, levelIndex):
        return self.resourceManager.getEarthColor(levelIndex)

    def getGuiTextureCache(self):
        return self.resourceManager.getGuiTextureCache()

    def isSoundEnabled(self):
        return self.resourceManager.isSoundEnabled()

    def setSoundEnabled(self, soundState):
        self.resourceManager.setSoundEnabled(soundState)

    def updateMusic(self, forceRestart=False):
        self.resourceManager.updateMusic(forceRestart)

    def playFootstepSound(self):
        self.resourceManager.playFootstepSound()

    def playVoice(self, voiceName):
        self.resourceManager.playVoice(voiceName)

    # UI FACTORY
    def clearCanvas(self):
        self.uiFactory.clearCanvas()

    def drawBackground(self):
        self.uiFactory.drawBackground()

    def createTitle(self, positionY, titleText, fontSize=70):
        return self.uiFactory.createTitle(positionY, titleText, fontSize)

    def createButton(self, positionX, positionY, buttonText, onClickCommand, fontSize=35):
        return self.uiFactory.createButton(positionX, positionY, buttonText, onClickCommand, fontSize)

    def createLabel(self, positionX, positionY, labelText, fontSize=30):
        return self.uiFactory.createLabel(positionX, positionY, labelText, fontSize)

    def createEntry(self, positionX, positionY, defaultText="", maxLength=12):
        return self.uiFactory.createEntry(positionX, positionY, defaultText, maxLength)

    def createColorSquare(self, positionX, positionY, squareSize, squareColor, onClickCommand, isSelected=False):
        return self.uiFactory.createColorSquare(positionX, positionY, squareSize, squareColor, onClickCommand,
                                                isSelected)

    def createPlayerBox(self, positionX, positionY, titleText, defaultName, currentColor, onColorCycle, onRemove=None,
                        isAddBox=False, onAdd=None):
        return self.uiFactory.createPlayerBox(positionX, positionY, titleText, defaultName, currentColor, onColorCycle,
                                              onRemove, isAddBox, onAdd)

    # STATE MANAGER

    def isCheatsEnabled(self):
        return self.stateManager.isCheatsEnabled()

    def setCheatsEnabled(self, state):
        self.stateManager.setCheatsEnabled(state)

    def getPlayerType(self, index):
        return self.stateManager.getPlayerType(index)

    def setPlayerType(self, index, playerType):
        self.stateManager.setPlayerType(index, playerType)

    def isPlayerBot(self, index):
        return self.stateManager.isPlayerBot(index)

    def cyclePlayerType(self, index):
        self.stateManager.cyclePlayerType(index)

    def getPlayerName(self):
        return self.stateManager.getPlayerName()

    def setPlayerName(self, targetName):
        self.stateManager.setPlayerName(targetName)

    def getPlayerColor(self):
        return self.stateManager.getPlayerColor()

    def setPlayerColor(self, targetColor):
        self.stateManager.setPlayerColor(targetColor)

    def getPlayer2Name(self):
        return self.stateManager.getPlayer2Name()

    def setPlayer2Name(self, targetName):
        self.stateManager.setPlayer2Name(targetName)

    def getPlayer2Color(self):
        return self.stateManager.getPlayer2Color()

    def setPlayer2Color(self, targetColor):
        self.stateManager.setPlayer2Color(targetColor)

    def getPlayer3Name(self):
        return self.stateManager.getPlayer3Name()

    def setPlayer3Name(self, targetName):
        self.stateManager.setPlayer3Name(targetName)

    def getPlayer3Color(self):
        return self.stateManager.getPlayer3Color()

    def setPlayer3Color(self, targetColor):
        self.stateManager.setPlayer3Color(targetColor)

    def getPlayer4Name(self):
        return self.stateManager.getPlayer4Name()

    def setPlayer4Name(self, targetName):
        self.stateManager.setPlayer4Name(targetName)

    def getPlayer4Color(self):
        return self.stateManager.getPlayer4Color()

    def setPlayer4Color(self, targetColor):
        self.stateManager.setPlayer4Color(targetColor)

    def getLocalMode(self):
        return self.stateManager.getLocalMode()

    def setLocalMode(self, targetMode):
        self.stateManager.setLocalMode(targetMode)

    def getLocalBoardsCount(self):
        return self.stateManager.getLocalBoardsCount()

    def setLocalBoardsCount(self, targetCount):
        self.stateManager.setLocalBoardsCount(targetCount)

    def getLocalPlayersCount(self):
        return self.stateManager.getLocalPlayersCount()

    def setLocalPlayersCount(self, targetCount):
        self.stateManager.setLocalPlayersCount(targetCount)

    def isLocalRotated(self):
        return self.stateManager.isLocalRotated()

    def setLocalRotated(self, rotationState):
        self.stateManager.setLocalRotated(rotationState)

    def isLocalPlaced(self):
        return self.stateManager.isLocalPlaced()

    def setLocalPlaced(self, placementState):
        self.stateManager.setLocalPlaced(placementState)

    def isQuickLaunch(self):
        return self.stateManager.isQuickLaunch()

    def setQuickLaunch(self, state):
        self.stateManager.setQuickLaunch(state)

    def getOnlineMode(self):
        return self.stateManager.getOnlineMode()

    def setOnlineMode(self, targetMode):
        self.stateManager.setOnlineMode(targetMode)

    def getOnlineBoardsCount(self):
        return self.stateManager.getOnlineBoardsCount()

    def setOnlineBoardsCount(self, targetCount):
        self.stateManager.setOnlineBoardsCount(targetCount)

    def getOnlinePlayersCount(self):
        return self.stateManager.getOnlinePlayersCount()

    def setOnlinePlayersCount(self, targetCount):
        self.stateManager.setOnlinePlayersCount(targetCount)

    def getNetworkId(self):
        return self.stateManager.getNetworkId()

    def setNetworkId(self, networkId):
        self.stateManager.setNetworkId(networkId)

    def getOnlineLobbyData(self):
        return self.stateManager.getOnlineLobbyData()

    def setOnlineLobbyData(self, lobbyData):
        self.stateManager.setOnlineLobbyData(lobbyData)

    def getNetworkRole(self):
        return self.stateManager.getNetworkRole()

    def setNetworkRole(self, targetRole):
        self.stateManager.setNetworkRole(targetRole)

    def getDiscoveredGames(self):
        return self.stateManager.getDiscoveredGames()

    def addDiscoveredGame(self, targetIp, gameInfo):
        self.stateManager.addDiscoveredGame(targetIp, gameInfo)

    def getNetworkClient(self):
        return self.stateManager.getNetworkClient()

    def setNetworkClient(self, targetClient):
        self.stateManager.setNetworkClient(targetClient)

    def getGameServer(self):
        return self.stateManager.getGameServer()

    def setGameServer(self, targetServer):
        self.stateManager.setGameServer(targetServer)

    def getGame(self):
        return self.stateManager.getGame()

    def setGame(self, game):
        self.stateManager.setGame(game)

    def getRotateLevel(self):
        return self.stateManager.getRotateLevel()

    def setRotateLevel(self, targetLevel):
        self.stateManager.setRotateLevel(targetLevel)

    def getMatchSelectedHex(self):
        return self.stateManager.getMatchSelectedHex()

    def setMatchSelectedHex(self, hexagonCoordinates):
        self.stateManager.setMatchSelectedHex(hexagonCoordinates)

    def getMatchValidMoves(self):
        return self.stateManager.getMatchValidMoves()

    def setMatchValidMoves(self, validMovesList):
        self.stateManager.setMatchValidMoves(validMovesList)

    def getMatchCurrentCard(self):
        return self.stateManager.getMatchCurrentCard()

    def setMatchCurrentCard(self, drawnCard):
        self.stateManager.setMatchCurrentCard(drawnCard)

    # NAVIGATOR
    def showPageMain(self):
        self.navigator.showPageMain()

    def showPageCredits(self):
        self.navigator.showPageCredits()

    def showPagePlay(self):
        self.navigator.showPagePlay()

    def showPageProfile(self):
        self.navigator.showPageProfile()

    def showPageOptions(self):
        self.navigator.showPageOptions()

    def showPageLocal(self):
        self.navigator.showPageLocal()

    def showPageOnline(self):
        self.navigator.showPageOnline()

    def showPageRotate(self):
        self.navigator.showPageRotate()

    def showPagePlace(self):
        self.navigator.showPagePlace()

    def showPageMatch(self):
        self.navigator.showPageMatch()

    def showPageEnd(self, winnerId):
        self.navigator.showPageEnd(winnerId)

    # NETWORK CONTROLLER
    def onNetworkMessageReceived(self, incomingMessage):
        self.networkController.onNetworkMessageReceived(incomingMessage)

    # GAME LOGIC
    def startNewGame(self):
        """Instancie un nouveau moteur de jeu (Game)."""
        from algo.game import Game
        isGameOnline = self.getNetworkClient() is not None

        activePlayerCount = self.getOnlinePlayersCount() if isGameOnline else self.getLocalPlayersCount()
        activeMode = self.getOnlineMode() if isGameOnline else self.getLocalMode()
        activeBoardCount = self.getOnlineBoardsCount() if isGameOnline else self.getLocalBoardsCount()

        if activeMode == "classic":
            game = Game(numPlayers=activePlayerCount)
        elif activeMode == "custom":
            game = Game(numPlayers=activePlayerCount, randomBoard=True, numBoards=activeBoardCount)

        self.setGame(game)
        self.setRotateLevel(1)
        self.setLocalRotated(False)
        self.setLocalPlaced(False)

    def resetMatchState(self):
        """Réinitialise les sélections du joueur local pour le match et synchronise le paquet de cartes."""
        self.setMatchSelectedHex(None)
        self.setMatchValidMoves([])
        self.setMatchCurrentCard(None)
        game = self.getGame()
        if game:
            game.resetCurrentCard()

    def quitGame(self):
        """Ferme proprement toutes les connexions réseau en cours et détruit la fenêtre de l'application."""
        discoverer = self.stateManager.getLanDiscoverer()
        if discoverer:
            try:
                discoverer.stopListening()
            except Exception:
                pass

        client = self.getNetworkClient()
        if client:
            try:
                client.close()
            except Exception:
                pass

        server = self.getGameServer()
        if server:
            try:
                server.stop()
            except Exception:
                pass

        self.__rootWindow.destroy()
        os._exit(0)

    def returnToLobby(self):
        """
        Gère le bouton de retour depuis n'importe quelle vue de jeu.
        - Si en ligne : envoie le signal RETURN_TO_LOBBY au serveur pour tout le monde.
        - Si en local : retourne simplement au menu local.
        """
        self.resetMatchState()
        client = self.getNetworkClient()
        if client and client.isRunning():
            client.sendReturnToLobby()
        else:
            self.navigator.showPageLocal()