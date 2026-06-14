def draw(launcher):
    """
    Dessine la page de sélection du mode de jeu, permettant à l'utilisateur de choisir entre une partie locale et une partie en ligne.

    Args:
        launcher (Launcher) : L'instance principale de l'application.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    launcher.createTitle(centerY - 200, launcher.getText("play", "title"))

    launcher.createButton(centerX - 190, centerY, launcher.getText("play", "btnLocal"), lambda: launcher.showPageLocal())

    launcher.createButton(centerX + 190, centerY, launcher.getText("play", "btnOnline"), lambda: launcher.showPageOnline())

    launcher.createButton(centerX, centerY + 150, launcher.getText("play", "btnBack"), lambda: launcher.showPageMain(), fontSize=25)