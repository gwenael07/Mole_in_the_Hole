def draw(launcher):
    """
    Dessine la page des paramètres. Le bouton de langue bascule vers la langue suivante.
    On peut choisir son thème ou bien activer/désactiver la musique, les effets sonores et les cheats
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    launcher.clearCanvas()
    launcher.drawBackground()

    launcher.createTitle(centerY - 250, launcher.getText("options", "title"))

    launcher.createLabel(centerX, centerY - 150, launcher.getText("options", "langLabel"))

    supportedLanguages = ["fr", "en", "de", "it", "es"]
    langDisplayNames = {
        "fr": "FRANÇAIS",
        "en": "ENGLISH",
        "de": "DEUTSCH",
        "it": "ITALIANO",
        "es": "ESPAÑOL"
    }

    def cycleLanguage():
        """
        Détermine la langue actuelle, trouve la suivante,
        met à jour le lanceur et redessine la page.
        """
        current = launcher.getCurrentLang()
        currentIndex = supportedLanguages.index(current)
        nextIndex = (currentIndex + 1) % len(supportedLanguages)

        newLang = supportedLanguages[nextIndex]
        launcher.setLanguage(newLang)
        launcher.showPageOptions()

    btnText = langDisplayNames.get(launcher.getCurrentLang(), "ERROR")

    launcher.createButton(centerX, centerY - 90, btnText, cycleLanguage, fontSize=25)

    themeY = centerY + 40
    launcher.createLabel(centerX, themeY, launcher.getText("options", "themeLabel"))

    availableThemes = launcher.getThemesList()
    spacingX = 250
    startX = centerX - ((len(availableThemes) - 1) * spacingX) // 2

    for i, themeKey in enumerate(availableThemes):
        posX = startX + (i * spacingX)
        displayName = launcher.getText("options", f"theme_{themeKey}")

        if themeKey == launcher.getCurrentThemeName():
            displayName = f"► {displayName} ◄"

        launcher.createButton(posX, themeY + 60, displayName,
                              lambda t=themeKey: launcher.setThemeName(t) or launcher.showPageOptions(), fontSize=25)

    # AUDIO & TRICHE
    controlY = themeY + 160

    # Section Audio
    launcher.createLabel(centerX - 200, controlY, launcher.getText("options", "soundLabel"))

    soundText = launcher.getText("options", "soundOn") if launcher.isSoundEnabled() else launcher.getText("options",
                                                                                                          "soundOff")
    launcher.createButton(centerX - 200, controlY + 60, soundText,
                          lambda: launcher.setSoundEnabled(not launcher.isSoundEnabled()) or launcher.showPageOptions(),
                          fontSize=30)

    # Section Triche
    launcher.createLabel(centerX + 200, controlY, launcher.getText("options", "cheatLabel"))

    cheatText = launcher.getText("options", "cheatOn") if launcher.isCheatsEnabled() else launcher.getText("options",
                                                                                                           "cheatOff")
    launcher.createButton(centerX + 200, controlY + 60, cheatText,
                          lambda: launcher.setCheatsEnabled(
                              not launcher.isCheatsEnabled()) or launcher.showPageOptions(),
                          fontSize=30)

    # RETOUR
    launcher.createButton(centerX, centerY + 300, launcher.getText("options", "btnBack"),
                          lambda: launcher.showPageMain(), fontSize=30)