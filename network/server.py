import socket
import threading
import random
from network.netUtils import sendJson, recvJson
import platform
import ctypes
import json
import time
from algo.game import Game
from algo.board import Board
from algo.cheat import CheatManager
from network import firewall
from network.getIps import getAllLocalIps

HOST = "0.0.0.0"
PORT = 5000


class GameServer:
    """
    Le serveur de jeu centralisé gérant le multiplexage des connexions, la gestion du salon,
    la distribution des paquets et la validation faisant autorité des règles.
    """

    def __init__(self, gameConfig):
        """
        Initialise l'architecture d'écoute TCP du GameServer.

        Args:
            gameConfig (dict) : Configurations du match (mode, plateaux, etc.).
        """
        self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__serverSocket.bind((HOST, PORT))
        self.__serverSocket.listen()

        self.__clients = []
        self.__playerMap = {}
        self.__playersData = {}
        self.__lock = threading.Lock()

        self.__config = gameConfig
        self.__expectedPlayers = 4

        self.__game = None
        self.__hasDrawn = False
        self.__broadcasting = False
        self.__phase = "WAITING"
        self.__pawnsPlaced = 0
        self.__totalPawns = 0

    def broadcast(self, messageData):
        """
        Distribue un dictionnaire JSON sécurisé à tous les clients connectés.

        Args:
            messageData (dict) : Le contenu des données à distribuer.
        """
        for clientConnection in self.__clients:
            try:
                sendJson(clientConnection, messageData)
            except Exception as exceptionError:
                pass

    def broadcastLobbyUpdate(self):
        """Diffuse les informations des joueurs et paramètres du salon à tout le monde."""
        self.broadcast({
            "type": "LOBBY_UPDATE",
            "players": self.__playersData,
            "mode": self.__config.get("mode", "classic"),
            "boards": self.__config.get("boards", 4)
        })

    def handleClient(self, clientConnection, playerId):
        """
        Surveille les interactions par socket pour une connexion joueur.
        Boucle sécurisée sans 'break' qui ignore les erreurs de logique mineures.

        Args:
            clientConnection (socket.socket) : Le socket dédié au client.
            playerId (int) : L'identifiant unique de la session.
        """
        sendJson(clientConnection, {"type": "WELCOME", "id": playerId})
        clientActive = True
        clientConnection.settimeout(None)

        while clientActive and self.__phase != "CLOSED":
            try:
                incomingMessage = recvJson(clientConnection)
                if incomingMessage is None:
                    clientActive = False
                else:
                    self.processMessage(playerId, incomingMessage)
            except socket.timeout:
                pass
            except (ConnectionResetError, OSError):
                clientActive = False
            except Exception as e:
                pass

        self.removeClient(clientConnection, playerId)

    def removeClient(self, clientConnection, playerId):
        """
        Nettoie toutes les données liées à un joueur déconnecté et met à jour le lobby.
        Si la partie était en cours, renvoie tout le monde au salon.

        Args:
            clientConnection (socket.socket) : L'objet socket à détruire.
            playerId (int) : L'identifiant du joueur à supprimer.
        """
        with self.__lock:
            if clientConnection in self.__clients:
                self.__clients.remove(clientConnection)
            if clientConnection in self.__playerMap:
                del self.__playerMap[clientConnection]

            stringId = str(playerId)
            if stringId in self.__playersData:
                del self.__playersData[stringId]

            try:
                clientConnection.close()
            except Exception:
                pass

            if self.__phase == "WAITING":
                self.broadcastLobbyUpdate()
            else:
                self.__phase = "WAITING"
                self.__game = None
                self.broadcastLobbyUpdate()
                self.broadcast({"type": "RETURN_TO_LOBBY"})

    def processMessage(self, playerId, incomingMessage):
        """
        Analyse et valide les paquets réseau entrants en fonction de la phase de jeu.

        Args:
            playerId (int) : L'identifiant numérique du joueur qui envoie.
            incomingMessage (dict) : L'objet de données décodé.
        """
        with self.__lock:
            msgType = incomingMessage.get("type")

            if msgType == "RETURN_TO_LOBBY":
                if self.__phase != "WAITING":
                    self.__phase = "WAITING"
                    self.__game = None
                    self.broadcastLobbyUpdate()
                    self.broadcast({"type": "RETURN_TO_LOBBY"})
                return

            if self.__phase == "WAITING":
                if msgType == "PROFILE":
                    self.__playersData[str(playerId)] = {"name": incomingMessage.get("name"),
                                                         "color": incomingMessage.get("color")}
                    self.broadcastLobbyUpdate()

                elif msgType == "UPDATE_SETTINGS":
                    if playerId == 0:
                        self.__config["mode"] = incomingMessage.get("mode")
                        self.__config["boards"] = incomingMessage.get("boards")
                        self.broadcastLobbyUpdate()

                elif msgType == "START_GAME":
                    if playerId == 0:
                        self.__broadcasting = False
                        self.__pawnsPlaced = 0
                        self.__hasDrawn = False

                        isCustomMode = (self.__config.get("mode") == "custom")
                        boardsCount = self.__config.get("boards", 4)
                        self.__expectedPlayers = len(self.__clients)
                        gameSeed = random.randint(0, 1000000)
                        random.seed(gameSeed)

                        self.__game = Game(numPlayers=self.__expectedPlayers, randomBoard=isCustomMode,
                                           numBoards=boardsCount)
                        self.__totalPawns = self.__expectedPlayers * self.__game.getMaxPawns()

                        if isCustomMode:
                            self.__phase = "SETUP"
                            self.broadcast({
                                "type": "SETUP_START",
                                "players": self.__expectedPlayers,
                                "theme": self.__config.get("theme", "meadow"),
                                "players_data": self.__playersData,
                                "mode": "custom",
                                "boards": boardsCount,
                                "pawnGrid": self.__game.getPawnGrid(),
                                "current_turn": self.__game.getCurrentPlayerIndex(),
                                "is_initial_start": True,
                                "seed": gameSeed
                            })
                        else:
                            self.__phase = "ORIENTATION"
                            self.broadcast({
                                "type": "ORIENTATION_START",
                                "players": self.__expectedPlayers,
                                "theme": self.__config.get("theme", "meadow"),
                                "board_num": 1,
                                "board": self.__game.getBoardMatrix(1),
                                "players_data": self.__playersData,
                                "mode": "classic",
                                "boards": boardsCount,
                                "seed": gameSeed
                            })

                elif msgType == "NETWORK_QUICK_LAUNCH":
                    if playerId == 0:
                        self.__broadcasting = False
                        self.__phase = "PLAYING"
                        self.__pawnsPlaced = 0
                        self.__hasDrawn = False

                        self.__expectedPlayers = len(self.__clients)
                        isCustomMode = (self.__config.get("mode") == "custom")
                        boardsCount = self.__config.get("boards", 4)
                        gameSeed = random.randint(0, 1000000)
                        random.seed(gameSeed)

                        self.__game = Game(numPlayers=self.__expectedPlayers, randomBoard=isCustomMode,
                                           numBoards=boardsCount)
                        self.__totalPawns = self.__expectedPlayers * self.__game.getMaxPawns()

                        rotationsApplied = {}
                        for levelIndex in range(1, boardsCount + 1):
                            turnsAmount = random.randint(0, 5)
                            rotationsApplied[str(levelIndex)] = turnsAmount
                            for _ in range(turnsAmount):
                                self.__game.turnBoard(levelIndex)

                        self.__game.quickLaunch()
                        self.__pawnsPlaced = self.__totalPawns
                        self.broadcast({
                            "type": "GAME_START",
                            "quick_launch": True,
                            "players": self.__expectedPlayers,
                            "theme": self.__config.get("theme", "meadow"),
                            "players_data": self.__playersData,
                            "current_turn": self.__game.getCurrentPlayerIndex(),
                            "pawnGrid": self.__game.getPawnGrid(),
                            "mode": self.__config.get("mode", "classic"),
                            "boards": boardsCount,
                            "rotations_applied": rotationsApplied,
                            "seed": gameSeed
                        })

            elif self.__phase == "ORIENTATION":
                if msgType == "TURN_BOARD":
                    if playerId == 0:
                        boardNum = incomingMessage.get("board")
                        isInverse = incomingMessage.get("inverse", False)
                        try:
                            self.__game.turnBoard(boardNum, isInverse)
                        except TypeError:
                            self.__game.turnBoard(boardNum)

                        self.broadcast({"type": "ORIENTATION_UPDATE", "action": "TURN_BOARD", "board_num": boardNum,
                                        "inverse": isInverse})

                elif msgType == "CHANGE_ORIENTATION_BOARD":
                    if playerId == 0:
                        boardNum = incomingMessage.get("board")
                        self.broadcast({"type": "ORIENTATION_UPDATE", "action": "CHANGE_BOARD", "board_num": boardNum})

                elif msgType == "RESET_BOARD":
                    if playerId == 0:
                        boardNum = incomingMessage.get("board")
                        self.__game._Game__boards[boardNum - 1] = Board(boardNum)
                        self.broadcast({"type": "ORIENTATION_UPDATE", "action": "RESET_BOARD", "board_num": boardNum})

                elif msgType == "FINISH_ORIENTATION":
                    if playerId == 0:
                        self.__phase = "SETUP"
                        self.broadcast({
                            "type": "SETUP_START",
                            "pawnGrid": self.__game.getPawnGrid(),
                            "current_turn": self.__game.getCurrentPlayerIndex()
                        })

            elif self.__phase == "SETUP":
                if msgType == "PLACE_PAWN":
                    if playerId == self.__game.getCurrentPlayerIndex():
                        targetLine, targetColumn = tuple(incomingMessage.get("pos"))
                        if self.__game.placePawn(targetLine, targetColumn):
                            self.__pawnsPlaced += 1
                            if self.__pawnsPlaced >= self.__totalPawns:
                                self.__phase = "PLAYING"
                                self.broadcast({
                                    "type": "GAME_START",
                                    "current_turn": self.__game.getCurrentPlayerIndex(),
                                    "pawnGrid": self.__game.getPawnGrid()
                                })
                            else:
                                self.broadcast({
                                    "type": "SETUP_UPDATE",
                                    "pawnGrid": self.__game.getPawnGrid(),
                                    "current_turn": self.__game.getCurrentPlayerIndex()
                                })

            elif self.__phase == "PLAYING":
                if msgType == "DRAW_CARD":
                    if playerId == self.__game.getCurrentPlayerIndex() and not self.__hasDrawn:
                        cardIndex = incomingMessage.get("index")
                        if cardIndex is not None:
                            cardValue = self.__game.drawSpecificCard(cardIndex)
                        else:
                            cardValue = self.__game.drawCard()
                            cardIndex = self.__game.getCurrentCardIndex()

                        self.__hasDrawn = True
                        deck, revealed = self.__game.getPlayerDeck()
                        self.broadcast({
                            "type": "CARD_DRAWN",
                            "player": playerId,
                            "value": cardValue,
                            "index": cardIndex,
                            "deck": deck,
                            "revealed": revealed
                        })

                elif msgType == "MOVE":
                    if playerId == self.__game.getCurrentPlayerIndex() and self.__hasDrawn:
                        startLine, startColumn = tuple(incomingMessage.get("start"))
                        endLine, endColumn = tuple(incomingMessage.get("end"))

                        isHole = (self.__game.getBoardMatrix(self.__game.getCurrentLevel() + 1)[endLine][
                                      endColumn] == 5)

                        if self.__game.movePawn(startLine, startColumn, endLine, endColumn):
                            self.__hasDrawn = False
                            if not self.checkLevelProgression():
                                self.broadcast({
                                    "type": "UPDATE",
                                    "pawnGrid": self.__game.getPawnGrid(),
                                    "current_turn": self.__game.getCurrentPlayerIndex(),
                                    "entered_hole": isHole
                                })

                elif msgType == "PASS_TURN":
                    if playerId == self.__game.getCurrentPlayerIndex() and self.__hasDrawn:
                        if self.__game.canSkipTurn():
                            self.__game.nextTurn()
                            self.__hasDrawn = False
                            self.broadcast({
                                "type": "UPDATE",
                                "pawnGrid": self.__game.getPawnGrid(),
                                "current_turn": self.__game.getCurrentPlayerIndex()
                            })

                elif msgType == "CHEAT_FILL_HOLES":
                    CheatManager(self.__game).fillHoles()

                    self.broadcast({
                        "type": "UPDATE",
                        "pawnGrid": self.__game.getPawnGrid(),
                        "current_turn": self.__game.getCurrentPlayerIndex()
                    })


    def checkLevelProgression(self):
        """
        Évalue les mécaniques du plateau pour déterminer un changement de niveau ou la victoire.

        Returns:
            bool : True si un changement d'état majeur (niveau ou victoire) s'est produit.
        """
        if self.__game.checkHoles():
            pawnsBefore = [len(self.__game._Game__players[p].getPawnList()) for p in range(self.__expectedPlayers)]
            self.__game.checkPawns()
            pawnsAfter = [len(self.__game._Game__players[p].getPawnList()) for p in range(self.__expectedPlayers)]
            eliminationDetected = any(b > 0 and a == 0 for b, a in zip(pawnsBefore, pawnsAfter))
            totalBoards = self.__config.get("boards", 4)
            winnerId = self.__game.winner()

            if winnerId is not False:
                self.__phase = "GAME_OVER"
                self.broadcast({
                    "type": "GAME_OVER",
                    "pawnGrid": self.__game.getPawnGrid(),
                    "winner": winnerId
                })
            elif self.__game.getCurrentLevel() < totalBoards - 1:
                self.__game._Game__currentLevel += 1
                self.__game.playerEliminated()
                self.__hasDrawn = False
                self.broadcast({
                    "type": "LEVEL_UP",
                    "pawnGrid": self.__game.getPawnGrid(),
                    "current_turn": self.__game.getCurrentPlayerIndex(),
                    "player_eliminated": eliminationDetected
                })
            else:
                self.__phase = "GAME_OVER"
                self.broadcast({
                    "type": "GAME_OVER",
                    "pawnGrid": self.__game.getPawnGrid(),
                    "winner": winnerId
                })
            return True
        return False

    def broadcastPresence(self):
        """
        Transmet en continu des paquets d'annonces UDP pour la visibilité sur le réseau local.
        S'arrête naturellement quand self.__broadcasting passe à False.
        """
        playerNames = self.__config.get("playerNames", ["Local"])
        hostName = playerNames[0] if playerNames else "Local"
        serverName = f"{hostName}'s Game"

        payloadBytes = json.dumps({
            "type": "GAME_ANNOUNCEMENT",
            "name": serverName,
            "port": PORT
        }).encode('utf-8')

        self.__broadcasting = True
        while self.__broadcasting:
            localIps = getAllLocalIps()
            for ipAddress in localIps:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udpSocket:
                        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                        udpSocket.bind((ipAddress, 0))
                        udpSocket.sendto(payloadBytes, ('<broadcast>', 5005))
                except Exception:
                    pass
            time.sleep(2)

    def acceptLoop(self):
        """
        Boucle acceptant les nouvelles connexions TCP de clients.
        La boucle suit l'état de self.__phase.
        """
        self.__serverSocket.settimeout(1.0)
        while self.__phase == "WAITING":
            try:
                clientConnection, clientAddress = self.__serverSocket.accept()
                clientConnection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                with self.__lock:
                    if len(self.__clients) >= 4:
                        clientConnection.close()
                    else:
                        playerId = len(self.__clients)
                        self.__clients.append(clientConnection)
                        self.__playerMap[clientConnection] = playerId
                        acceptWorkerThread = threading.Thread(target=self.handleClient,
                                                              args=(clientConnection, playerId), daemon=True)
                        acceptWorkerThread.start()
            except socket.timeout:
                pass
            except Exception:
                self.__phase = "CLOSED"

    def start(self):
        """Ouvre les ports et lance l'architecture réseau principale du serveur."""
        firewall.openFirewallPorts()
        if platform.system() == "Windows":
            ctypes.windll.kernel32.AllocConsole()
        try:
            broadcastThread = threading.Thread(target=self.broadcastPresence, daemon=True)
            broadcastThread.start()
            acceptThread = threading.Thread(target=self.acceptLoop, daemon=True)
            acceptThread.start()

            while self.__phase != "CLOSED":
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
            firewall.closeFirewallPorts()

    def stop(self):
        """Arrête le serveur et clôture proprement les sockets."""
        self.__phase = "CLOSED"
        self.__broadcasting = False
        try:
            self.__serverSocket.close()
        except:
            pass
        for clientConnection in self.__clients:
            try:
                clientConnection.close()
            except:
                pass