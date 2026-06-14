import socket
import threading
from network.netUtils import sendJson, recvJson

class NetworkClient:
    """
    Gère la connexion par socket TCP côté client, l'écoute réseau en arrière-plan,
    et l'envoi des paquets d'actions de jeu au serveur.
    """
    def __init__(self, targetHost, targetPort, onMessageReceived):
        """
        Initialise le NetworkClient.

        Args:
            targetHost (str) : L'adresse IP du serveur cible.
            targetPort (int) : Le numéro de port TCP du serveur cible.
            onMessageReceived (callable) : Fonction de rappel exécutée lorsqu'un nouveau contenu JSON arrive.
        """
        self.__host = targetHost
        self.__port = targetPort
        self.__callback = onMessageReceived
        self.__clientSocket = None
        self.__running = False

    def connect(self):
        """
        Établit une connexion avec le serveur et lance un thread en arrière-plan pour écouter les données.

        Returns:
            bool : True si la connexion a réussi, False sinon.
        """
        try:
            self.__clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__clientSocket.settimeout(3.0)
            self.__clientSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.__clientSocket.connect((self.__host, self.__port))
            self.__clientSocket.settimeout(None)

            self.__running = True

            listeningThread = threading.Thread(target=self.listenLoop, daemon=True)
            listeningThread.start()
            return True
        except (ConnectionRefusedError, TimeoutError, OSError) as exceptionError:
            return False

    def listenLoop(self):
        """
        Boucle d'écoute en arrière-plan sans utilisation de 'break'.
        Se termine naturellement lorsque self.__running passe à False et gère les déconnexions.
        """
        while self.__running:
            try:
                receivedMessage = recvJson(self.__clientSocket)
                if receivedMessage is None:
                    self.__running = False
                    self.__callback({"type": "SERVER_CLOSED"})
                else:
                    self.__callback(receivedMessage)
            except (ConnectionResetError, OSError):
                self.__running = False
                self.__callback({"type": "SERVER_CLOSED"})
            except Exception as e:
                pass

    def sendProfile(self, playerName, playerColor):
        """
        Envoie le profil de configuration d'identité du joueur (nom et couleur) au serveur.
        """
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "PROFILE", "name": playerName, "color": playerColor})
            except Exception: pass

    def sendUpdateSettings(self, gameMode, totalBoards):
        """
        Envoie les configurations de match mises à jour au serveur. Uniquement utilisable par l'hôte.
        """
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "UPDATE_SETTINGS", "mode": gameMode, "boards": totalBoards})
            except Exception: pass

    def sendStartGame(self):
        """Ordonne au serveur de verrouiller le salon et de commencer la configuration de partie."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "START_GAME"})
            except Exception: pass

    def sendPlacePawn(self, targetRow, targetColumn):
        """
        Envoie une requête de placement de pion lors de la phase de préparation.
        """
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "PLACE_PAWN", "pos": [targetRow, targetColumn]})
            except Exception: pass

    def sendTurnBoard(self, boardNumber, isInverse=False):
        """
        Demande au serveur de faire pivoter un plateau pendant la phase d'orientation.
        """
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "TURN_BOARD", "board": boardNumber, "inverse": isInverse})
            except Exception: pass

    def sendChangeOrientationBoard(self, boardNumber):
        """Demande au serveur de remplacer la matrice d'un plateau spécifié."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "CHANGE_ORIENTATION_BOARD", "board": boardNumber})
            except Exception: pass

    def sendResetBoard(self, boardNumber):
        """Demande au serveur de réinitialiser un plateau à son état par défaut."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "RESET_BOARD", "board": boardNumber})
            except Exception: pass

    def sendFinishOrientation(self):
        """Signale au serveur que l'hôte a terminé les modifications et verrouille l'orientation."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "FINISH_ORIENTATION"})
            except Exception: pass

    def sendNetworkQuickLaunch(self):
        """Demande au serveur de construire et distribuer instantanément une matrice aléatoire complète."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "NETWORK_QUICK_LAUNCH"})
            except Exception: pass

    def sendDrawCard(self, inventoryIndex=None):
        """Envoie une requête d'action de pioche de carte."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "DRAW_CARD", "index": inventoryIndex})
            except Exception: pass

    def sendMove(self, startCoordinates, endCoordinates):
        """Transmet une action de déplacement de pion validée."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "MOVE", "start": startCoordinates, "end": endCoordinates})
            except Exception: pass

    def sendPassTurn(self):
        """Signale au serveur de passer de force le tour du joueur actuel."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "PASS_TURN"})
            except Exception: pass

    def sendCheat(self):
        """Remplit instantanément les trous de la grille."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "CHEAT_FILL_HOLES"})
            except Exception: pass

    def sendReturnToLobby(self):
        """Demande au serveur d'annuler la partie en cours et de renvoyer tout le monde au salon."""
        if self.__running and self.__clientSocket:
            try: sendJson(self.__clientSocket, {"type": "RETURN_TO_LOBBY"})
            except Exception: pass

    def isRunning(self):
        """Vérifie le statut de la boucle réseau interne du client."""
        return self.__running

    def close(self):
        """Déconnecte proprement la socket TCP active."""
        self.__running = False
        if self.__clientSocket:
            try: self.__clientSocket.close()
            except OSError: pass