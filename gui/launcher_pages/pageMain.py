def draw(launcher):
    """
    Dessine le menu principal du jeu avec les options de navigation de base (Jouer, Options, Quitter, Profil).

    Args:
        launcher (Launcher) : L'instance principale de l'application gérant l'interface.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    screenWidth = launcher.getScreenWidth()
    screenHeight = launcher.getScreenHeight()

    launcher.createTitle(screenHeight // 6, launcher.getText("main", "title"))

    launcher.createButton(centerX, centerY, launcher.getText("main", "btnStart"), lambda: launcher.showPagePlay())
    launcher.createButton(centerX, centerY + 80, launcher.getText("main", "btnOptions"), lambda: launcher.showPageOptions())
    launcher.createButton(centerX, centerY + 160, launcher.getText("main", "btnCredits"), lambda: launcher.showPageCredits())
    launcher.createButton(centerX, centerY + 240, launcher.getText("main", "btnQuit"), lambda: launcher.quitGame())

    launcher.createButton(screenWidth - 100, screenHeight - 50, launcher.getText("main", "btnProfile"), lambda: launcher.showPageProfile(), fontSize=25)