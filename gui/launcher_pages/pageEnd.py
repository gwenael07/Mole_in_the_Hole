import os
from PIL import Image, ImageTk

def draw(launcher, winnerId: int):
    """
    Vue graphique de l'écran de fin de partie (Page de Victoire).
    Affiche le nom et la couleur du gagnant de la partie avec une illustration de pion,
    et propose de rejouer, de retourner au lobby ou de quitter.

    Args:
        launcher (Launcher) : L'instance principale de l'application.
        winnerId (int) : L'identifiant (1 à 4) du joueur ayant remporté la victoire.
    """
    canvas = launcher.getCanvas()
    screenHeight = launcher.getScreenHeight()
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    # RÉCUPERATION DU GAGNANT
    playerNames = [
        launcher.getPlayerName(), launcher.getPlayer2Name(),
        launcher.getPlayer3Name(), launcher.getPlayer4Name()
    ]
    playerColors = [
        launcher.getPlayerColor(), launcher.getPlayer2Color(),
        launcher.getPlayer3Color(), launcher.getPlayer4Color()
    ]

    winnerName = playerNames[winnerId - 1]
    winnerColor = playerColors[winnerId - 1]

    colorMap = {
        "light_green": "#B4E046",
        "shocking_pink": "#FA0080"
    }
    tkWinnerColor = colorMap.get(winnerColor, winnerColor)

    # TITRES ET TEXTES
    launcher.createTitle(80, launcher.getText("end", "title"), fontSize=60)

    winnerText = launcher.getText("end", "winner").format(winnerName.upper())
    canvas.create_text(centerX, 160, text=winnerText, font=("Helvetica", 35, "bold"), fill=tkWinnerColor)

    # DESSIN DU GROS PION
    themeFolder = launcher.getTextureFolder()
    texturePath = f"assets/textures/{themeFolder}/pawns/pawn_{winnerColor}.png"
    textureCache = launcher.getGuiTextureCache()
    imageSize = 220
    cacheKey = (f"BIG_PAWN_{winnerColor}", imageSize)

    if cacheKey not in textureCache:
        if os.path.exists(texturePath):
            loadedImage = Image.open(texturePath).convert("RGBA")
            loadedImage = loadedImage.resize((imageSize, imageSize), Image.Resampling.LANCZOS)
            textureCache[cacheKey] = ImageTk.PhotoImage(loadedImage)
        else:
            textureCache[cacheKey] = None

    bigPawnImage = textureCache.get(cacheKey)
    canvas.create_image(centerX, centerY - 30, image=bigPawnImage)

    # BOUTONS D'ACTION
    def doReplay():
        """Relance une nouvelle partie de la bonne façon selon le mode."""
        client = launcher.getNetworkClient()
        if client and client.isRunning():
            doLobby()
            return

        launcher.startNewGame()

        if launcher.isQuickLaunch():
            gameInstance = launcher.getGame()
            gameInstance.quickLaunch()
            launcher.setLocalRotated(True)
            launcher.setLocalPlaced(True)
            launcher.showPageMatch()
            return

        launcher.setLocalPlaced(False)

        if launcher.getLocalMode() == "classic":
            launcher.setLocalRotated(False)
            launcher.showPageRotate()
        else:
            launcher.setLocalRotated(True)
            launcher.showPagePlace()

    def doLobby():
        """Réinitialise les états locaux et retourne au salon de configuration."""
        launcher.setLocalRotated(False)
        launcher.setLocalPlaced(False)
        launcher.showPageLocal()

    def doQuit():
        """Ferme l'application de jeu de manière sécurisée."""
        launcher.quitGame()

    buttonYPosition = screenHeight - 220
    launcher.createButton(centerX, buttonYPosition, launcher.getText("end", "btnReplay"), doReplay, fontSize=30)
    launcher.createButton(centerX, buttonYPosition + 70, launcher.getText("end", "btnLobby"), doLobby, fontSize=30)
    launcher.createButton(centerX, buttonYPosition + 140, launcher.getText("end", "btnQuit"), doQuit, fontSize=30)