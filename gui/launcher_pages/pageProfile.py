def draw(launcher):
    """
    Affiche l'interface de personnalisation du profil utilisateur, permettant de modifier le nom et la couleur du joueur principal.
    """
    centerX = launcher.getCenterX()
    centerY = launcher.getCenterY()

    launcher.createTitle(centerY - 280, launcher.getText("profile", "title"))

    launcher.createLabel(centerX, centerY - 160, launcher.getText("profile", "nameLabel"))
    nameInputEntry = launcher.createEntry(centerX, centerY - 100, launcher.getPlayerName())

    launcher.createLabel(centerX, centerY - 10, launcher.getText("profile", "colorLabel"))

    availableColors = [
        "red", "blue", "green", "yellow",
        "orange", "pink", "purple", "gray",
        "light_green", "shocking_pink", "brown", "cyan"
    ]

    columnCount = 4
    squareSize = 50
    spacingX = 80
    spacingY = 70

    startX = centerX - ((columnCount - 1) * spacingX) // 2
    startY = centerY + 60

    def onColorClick(clickedColor):
        """Met à jour la couleur sélectionnée par le joueur et rafraîchit la page."""
        launcher.setPlayerName(nameInputEntry.get())
        launcher.setPlayerColor(clickedColor)
        launcher.showPageProfile()

    for i in range(len(availableColors)):
        targetColor = availableColors[i]
        columnIndex = i % columnCount
        rowIndex = i // columnCount

        positionX = startX + (columnIndex * spacingX)
        positionY = startY + (rowIndex * spacingY)

        isSelected = (targetColor == launcher.getPlayerColor())

        launcher.createColorSquare(
            positionX,
            positionY,
            squareSize,
            targetColor,
            lambda colClick=targetColor: onColorClick(colClick),
            isSelected
        )

    def saveAndGoBack():
        """Enregistre le nom saisi et retourne au menu principal."""
        launcher.setPlayerName(nameInputEntry.get())
        launcher.showPageMain()

    launcher.createButton(centerX, centerY + 320, launcher.getText("profile", "btnSave"), saveAndGoBack, fontSize=30)