import random
from algo.board import Board

class NetworkController:
    """
    Gère la réception et l'interprétation des messages réseau.
    """

    def __init__(self, guiCore):
        self.guiCore = guiCore

    def onNetworkMessageReceived(self, incomingMessage):
        """
        Callback central gérant l'interprétation et la réaction de l'interface aux messages réseau reçus du serveur.
        """
        messageType = incomingMessage.get("type")

        if messageType == "WELCOME":
            networkId = incomingMessage.get("id")
            self.guiCore.setNetworkId(networkId)
            
            if self.guiCore.getPlayerName() == "Player 1" and networkId != 0:
                self.guiCore.setPlayerName(f"Player {networkId + 1}")
                
            networkClient = self.guiCore.getNetworkClient()
            if networkClient:
                networkClient.sendProfile(self.guiCore.getPlayerName(), self.guiCore.getPlayerColor())

        elif messageType == "SERVER_CLOSED":
            self.guiCore.setNetworkClient(None)
            self.guiCore.setOnlineLobbyData({})
            self.guiCore.setGameServer(None)
            self.guiCore.showPageOnline()

        elif messageType == "LOBBY_UPDATE":
            self.guiCore.setOnlineLobbyData(incomingMessage)
            if "mode" in incomingMessage: self.guiCore.setOnlineMode(incomingMessage.get("mode"))
            if "boards" in incomingMessage: self.guiCore.setOnlineBoardsCount(incomingMessage.get("boards"))
            self.guiCore.showPageOnline()

        elif messageType == "RETURN_TO_LOBBY":
            self.guiCore.setGame(None)
            self.guiCore.resetMatchState()
            self.guiCore.showPageOnline()

        elif messageType == "ORIENTATION_START":
            playersData = incomingMessage.get("players_data", {})
            if "0" in playersData: self.guiCore.setPlayerName(playersData["0"]["name"]); self.guiCore.setPlayerColor(playersData["0"]["color"])
            if "1" in playersData: self.guiCore.setPlayer2Name(playersData["1"]["name"]); self.guiCore.setPlayer2Color(playersData["1"]["color"])
            if "2" in playersData: self.guiCore.setPlayer3Name(playersData["2"]["name"]); self.guiCore.setPlayer3Color(playersData["2"]["color"])
            if "3" in playersData: self.guiCore.setPlayer4Name(playersData["3"]["name"]); self.guiCore.setPlayer4Color(playersData["3"]["color"])

            self.guiCore.setOnlinePlayersCount(incomingMessage.get("players", 2))

            if incomingMessage.get("theme"): self.guiCore.setThemeName(incomingMessage.get("theme"))
            if "mode" in incomingMessage: self.guiCore.setOnlineMode(incomingMessage.get("mode"))
            if "boards" in incomingMessage: self.guiCore.setOnlineBoardsCount(incomingMessage.get("boards"))

            if "seed" in incomingMessage:
                random.seed(incomingMessage.get("seed"))

            self.guiCore.startNewGame()
            self.guiCore.setRotateLevel(incomingMessage.get("board_num"))
            self.guiCore.showPageRotate()

        elif messageType == "ORIENTATION_UPDATE":
            orientationAction = incomingMessage.get("action")
            boardNumber = incomingMessage.get("board_num")
            game = self.guiCore.getGame()

            if orientationAction == "TURN_BOARD" and game:
                isInverse = incomingMessage.get("inverse", False)
                game.turnBoard(boardNumber, isInverse)
            elif orientationAction == "RESET_BOARD" and game:
                game._Game__boards[boardNumber - 1] = Board(boardNumber)
            elif orientationAction == "CHANGE_BOARD":
                self.guiCore.setRotateLevel(boardNumber)

            self.guiCore.showPageRotate()

        elif messageType == "SETUP_START":
            if incomingMessage.get("is_initial_start"):
                playersData = incomingMessage.get("players_data", {})
                if "0" in playersData: self.guiCore.setPlayerName(playersData["0"]["name"]); self.guiCore.setPlayerColor(playersData["0"]["color"])
                if "1" in playersData: self.guiCore.setPlayer2Name(playersData["1"]["name"]); self.guiCore.setPlayer2Color(playersData["1"]["color"])
                if "2" in playersData: self.guiCore.setPlayer3Name(playersData["2"]["name"]); self.guiCore.setPlayer3Color(playersData["2"]["color"])
                if "3" in playersData: self.guiCore.setPlayer4Name(playersData["3"]["name"]); self.guiCore.setPlayer4Color(playersData["3"]["color"])

                self.guiCore.setOnlinePlayersCount(incomingMessage.get("players", 2))
                if incomingMessage.get("theme"): self.guiCore.setThemeName(incomingMessage.get("theme"))
                if "mode" in incomingMessage: self.guiCore.setOnlineMode(incomingMessage.get("mode"))
                if "boards" in incomingMessage: self.guiCore.setOnlineBoardsCount(incomingMessage.get("boards"))

                if "seed" in incomingMessage:
                    random.seed(incomingMessage.get("seed"))

                self.guiCore.startNewGame()

                game = self.guiCore.getGame()
                boardMatrices = incomingMessage.get("board_matrices", [])
                if game:
                    for i, currentMatrix in enumerate(boardMatrices):
                        try:
                            game._Game__boards[i]._Board__matrix = currentMatrix
                            game._Game__boards[i]._Board__grid = currentMatrix
                        except Exception:
                            pass

            game = self.guiCore.getGame()
            if game:
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
                game._Game__currentPlayerIndex = incomingMessage.get("current_turn")
            self.guiCore.showPagePlace()

        elif messageType == "SETUP_UPDATE":
            game = self.guiCore.getGame()
            if game:
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
                game._Game__currentPlayerIndex = incomingMessage.get("current_turn")
            self.guiCore.showPagePlace()

        elif messageType == "GAME_START":
            if incomingMessage.get("quick_launch"):
                playersData = incomingMessage.get("players_data", {})
                if "0" in playersData: self.guiCore.setPlayerName(playersData["0"]["name"]); self.guiCore.setPlayerColor(playersData["0"]["color"])
                if "1" in playersData: self.guiCore.setPlayer2Name(playersData["1"]["name"]); self.guiCore.setPlayer2Color(playersData["1"]["color"])
                if "2" in playersData: self.guiCore.setPlayer3Name(playersData["2"]["name"]); self.guiCore.setPlayer3Color(playersData["2"]["color"])
                if "3" in playersData: self.guiCore.setPlayer4Name(playersData["3"]["name"]); self.guiCore.setPlayer4Color(playersData["3"]["color"])

                self.guiCore.setOnlinePlayersCount(incomingMessage.get("players", 2))

                if incomingMessage.get("theme"): self.guiCore.setThemeName(incomingMessage.get("theme"))
                if "mode" in incomingMessage: self.guiCore.setOnlineMode(incomingMessage.get("mode"))
                if "boards" in incomingMessage: self.guiCore.setOnlineBoardsCount(incomingMessage.get("boards"))

                if "seed" in incomingMessage:
                    random.seed(incomingMessage.get("seed"))

                self.guiCore.startNewGame()

                game = self.guiCore.getGame()
                appliedRotations = incomingMessage.get("rotations_applied", {})
                if game:
                    for stringLevel, rotationTurns in appliedRotations.items():
                        try:
                            targetLevel = int(stringLevel)
                            for _ in range(rotationTurns):
                                game.turnBoard(targetLevel)
                        except Exception:
                            pass

            game = self.guiCore.getGame()
            if game:
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
                game._Game__currentPlayerIndex = incomingMessage.get("current_turn", 0)
            self.guiCore.resetMatchState()
            self.guiCore.showPageMatch()
            self.guiCore.updateMusic()

        elif messageType == "CARD_DRAWN":
            game = self.guiCore.getGame()
            if game:
                deck = incomingMessage.get("deck")
                revealed = incomingMessage.get("revealed")
                if deck is not None and revealed is not None:
                    playerIndex = incomingMessage.get("player")
                    game._Game__players[playerIndex].setDeckState(deck, revealed)
                game._Game__currentCardIndex = incomingMessage.get("index")
            self.guiCore.setMatchCurrentCard(incomingMessage.get("value"))
            self.guiCore.showPageMatch()

        elif messageType == "UPDATE":
            game = self.guiCore.getGame()
            if game:
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
                game._Game__currentPlayerIndex = incomingMessage.get("current_turn")
            if incomingMessage.get("entered_hole"):
                self.guiCore.playVoice("area_secured")
            self.guiCore.resetMatchState()
            self.guiCore.showPageMatch()

        elif messageType == "LEVEL_UP":
            if incomingMessage.get("player_eliminated"):
                self.guiCore.playVoice("player_eliminated")
            game = self.guiCore.getGame()
            if game:
                game._Game__currentLevel += 1
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
                game._Game__currentPlayerIndex = incomingMessage.get("current_turn")
            self.guiCore.resetMatchState()
            self.guiCore.showPageMatch()
            self.guiCore.updateMusic()

        elif messageType == "GAME_OVER":
            game = self.guiCore.getGame()
            if game:
                game._Game__pawnGrid = incomingMessage.get("pawnGrid")
            winnerId = incomingMessage.get("winner")
            if not winnerId and game:
                winnerId = game.winner()
            if not winnerId:
                winnerId = 0
            self.guiCore.showPageEnd(winnerId)