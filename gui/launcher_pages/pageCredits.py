def draw(launcher):
    """
    Dessine la page des crédits en utilisant les textes localisés dans le JSON.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    launcher.createTitle(centerY - 250, launcher.getText("credits", "title"), fontSize=50)

    creditKeys = ["algo", "gui", "network", "music/sfx", "basedOn"]

    for i, key in enumerate(creditKeys):
        creditText = launcher.getText("credits", key)
        launcher.createLabel(centerX, centerY - 100 + (i * 60), creditText, fontSize=25)

    launcher.createButton(centerX, centerY + 250, launcher.getText("options", "btnBack"),
                          lambda: launcher.showPageMain(), fontSize=30)