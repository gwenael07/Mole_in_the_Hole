import socket
import threading
import json
import time


class LANDiscoverer:
    """
    Écoute les paquets de diffusion (broadcast) UDP sur le réseau local pour découvrir les serveurs de jeu actifs.

    Cette classe exécute un thread en arrière-plan qui écoute en continu sur un port UDP spécifique (5005).
    Lorsqu'elle reçoit une annonce de jeu valide de la part d'un hôte, elle analyse le contenu JSON
    et déclenche une fonction de rappel (callback) pour notifier l'application cliente.
    """

    def __init__(self, onGameDiscoveredCallback):
        """
        Initialise le LANDiscoverer.

        Args:
            onGameDiscoveredCallback (callable) : Une fonction de rappel qui prend deux arguments
                                          (senderIp (str), gameAnnouncement (dict)) et se déclenche chaque fois qu'un nouveau
                                          serveur de jeu est découvert sur le réseau.
        """
        self.__onGameDiscoveredCallback = onGameDiscoveredCallback
        self.__isListening = False
        self.__discoveredGames = {}

    def startListening(self):
        """
        Démarre le thread d'écoute UDP en arrière-plan.

        Cette méthode réinitialise également le cache des parties précédemment découvertes afin que le redémarrage
        de l'écoute fournisse une liste fraîche des serveurs actifs.
        """
        if self.__isListening:
            return
        self.__isListening = True
        self.__discoveredGames.clear()

        listeningThread = threading.Thread(target=self.listenLoop, daemon=True)
        listeningThread.start()

    def stopListening(self):
        """
        Arrête le thread d'écoute UDP en arrière-plan.
        """
        self.__isListening = False

    def listenLoop(self):
        """
        Une boucle qui crée un socket UDP lié au port 5005, active la réutilisation du port, et écoute en continu
        les datagrammes entrants. Lorsqu'un datagramme est reçu, elle tente de le décoder en JSON.
        S'il s'agit d'une annonce valide ('GAME_ANNOUNCEMENT') provenant d'une adresse IP encore inconnue,
        elle enregistre la partie et déclenche la fonction de rappel.
        """
        discoverySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discoverySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        discoverySocket.bind(('', 5005))
        discoverySocket.settimeout(2.0)

        while self.__isListening:
            try:
                receivedData, senderAddress = discoverySocket.recvfrom(1024)
                senderIp = senderAddress[0]

                gameAnnouncement = json.loads(receivedData.decode('utf-8'))

                if gameAnnouncement.get("type") == "GAME_ANNOUNCEMENT":

                    if senderIp not in self.__discoveredGames:
                        self.__discoveredGames[senderIp] = gameAnnouncement
                        self.__onGameDiscoveredCallback(senderIp, gameAnnouncement)

            except socket.timeout:
                continue

            except json.JSONDecodeError:
                continue

            except Exception as exceptionError:
                time.sleep(1)
                continue

        discoverySocket.close()