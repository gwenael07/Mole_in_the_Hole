from gui.launcher_pages import pageMain, pagePlay, pageProfile, pageOptions, pageLocal, pageEnd, pageOnline, pageCredits
from gui.board_views import viewRotate, viewPlace, viewMatch

class Navigator:
    """
    S'occupe de la navigation et de l'affichage des différentes pages/vues du jeu.
    """

    def __init__(self, guiCore):
        self.guiCore = guiCore

    def showPageMain(self):
        """Efface le Canvas et affiche la page du Menu Principal."""
        self.guiCore.setGame(None)
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageMain.draw(self.guiCore)

    def showPageCredits(self):
        """Efface le Canvas et affiche le credits."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageCredits.draw(self.guiCore)

    def showPagePlay(self):
        """Efface le Canvas et affiche le menu de sélection de mode de jeu."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pagePlay.draw(self.guiCore)

    def showPageProfile(self):
        """Efface le Canvas et affiche le menu de profil."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageProfile.draw(self.guiCore)

    def showPageOptions(self):
        """Efface le Canvas et affiche le menu des options et paramètres."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageOptions.draw(self.guiCore)

    def showPageLocal(self):
        """
        Affiche le salon local.
        Si on est en ligne, vérifie si une partie est réellement en cours.
        """
        networkClient = self.guiCore.getNetworkClient()
        game = self.guiCore.getGame()

        if networkClient and networkClient.isRunning() and game is not None:
            self.guiCore.clearCanvas()
            self.guiCore.drawBackground()
            self.guiCore.createTitle(self.guiCore.getCenterY(), "Waiting for players...", fontSize=40)
            return

        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageLocal.draw(self.guiCore)

    def showPageOnline(self):
        """Efface le Canvas et affiche la fenêtre réseau/lobby."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageOnline.draw(self.guiCore)

    def showPageRotate(self):
        """Efface le Canvas et affiche la vue spécifique de préparation/rotation des plateaux."""
        if self.guiCore.getNetworkClient() is None and self.guiCore.getLocalMode() == "custom":
            self.showPagePlace()
            return

        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        viewRotate.draw(self.guiCore)

    def showPagePlace(self):
        """Efface le Canvas et affiche la vue de positionnement initial des pions."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        viewPlace.draw(self.guiCore)

    def showPageMatch(self):
        """Efface le Canvas et affiche le plateau de jeu principal du match en cours."""
        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        viewMatch.draw(self.guiCore)

    def showPageEnd(self, winnerId):
        """Efface le Canvas, coupe la session de jeu, et affiche l'écran de fin de partie."""
        self.guiCore.setGame(None)
        self.guiCore.updateMusic(forceRestart=True)
        self.guiCore.playVoice("victory")

        self.guiCore.clearCanvas()
        self.guiCore.drawBackground()
        pageEnd.draw(self.guiCore, winnerId)
