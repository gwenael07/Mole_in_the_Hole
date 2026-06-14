import tkinter as tk
from PIL import Image, ImageTk
from PIL.ImageColor import colormap


class UIFactory:
    """
    S'occupe de la création et du rendu de tous les éléments d'interface utilisateur (boutons, textes, champs).
    """

    def __init__(self, guiCore):
        self.guiCore = guiCore
        self.__bgImageTk = None

    def clearCanvas(self):
        """Supprime tous les éléments visuels actuellement dessinés sur le Canvas."""
        canvas = self.guiCore.getCanvas()
        canvas.delete("all")
        for childWidget in canvas.winfo_children():
            childWidget.destroy()

    def drawBackground(self):
        """Dessine l'image d'arrière-plan adaptée au thème sélectionné."""
        canvas = self.guiCore.getCanvas()
        backgroundImagePath = self.guiCore.getColor("bgImage")
        loadedImage = Image.open(backgroundImagePath)
        scaledImage = loadedImage.resize((self.guiCore.getScreenWidth(), self.guiCore.getScreenHeight()), Image.Resampling.LANCZOS)
        self.__bgImageTk = ImageTk.PhotoImage(scaledImage)
        canvas.create_image(0, 0, image=self.__bgImageTk, anchor="nw")

    def createTitle(self, positionY, titleText, fontSize=70):
        """Crée et affiche un titre de page textuel."""
        canvas = self.guiCore.getCanvas()
        centerX = self.guiCore.getScreenWidth() // 2
        return canvas.create_text(
            centerX, positionY, text=titleText, font=("Helvetica", fontSize, "bold"), fill=self.guiCore.getColor("titleColor")
        )

    def createButton(self, positionX, positionY, buttonText, onClickCommand, fontSize=35):
        """Crée un bouton interactif textuel doté d'effets de survol (hover)."""
        canvas = self.guiCore.getCanvas()
        buttonElement = canvas.create_text(
            positionX, positionY, text=buttonText, font=("Helvetica", fontSize, "bold"), fill=self.guiCore.getColor("btnNormal")
        )

        def onEnter(event):
            canvas.itemconfig(buttonElement, fill=self.guiCore.getColor("btnHover"))
            canvas.config(cursor="hand2")

        def onLeave(event):
            canvas.itemconfig(buttonElement, fill=self.guiCore.getColor("btnNormal"))
            canvas.config(cursor="")

        def onClick(event):
            canvas.config(cursor="")
            onClickCommand()

        canvas.tag_bind(buttonElement, "<Enter>", onEnter)
        canvas.tag_bind(buttonElement, "<Leave>", onLeave)
        canvas.tag_bind(buttonElement, "<Button-1>", onClick)
        return buttonElement

    def createLabel(self, positionX, positionY, labelText, fontSize=30):
        """Affiche un simple texte descriptif."""
        canvas = self.guiCore.getCanvas()
        return canvas.create_text(positionX, positionY, text=labelText, font=("Helvetica", fontSize),
                                  fill=self.guiCore.getColor("titleColor"))

    def createEntry(self, positionX, positionY, defaultText="", maxLength=12):
        """
        Crée un champ de saisie de texte modifiable par l'utilisateur avec validation.
        Restreint la longueur maximale et bloque les caractères spéciaux.
        """
        canvas = self.guiCore.getCanvas()
        rootWindow = self.guiCore.getRootWindow()

        def validateInput(proposedText):
            if len(proposedText) > maxLength:
                return False
            for char in proposedText:
                if not (char.isalnum() or char == " " or char == "_"):
                    return False
            return True

        validationCommand = (rootWindow.register(validateInput), '%P')
        inputField = tk.Entry(
            canvas,
            font=("Helvetica", 25),
            justify="center",
            validate="key",
            validatecommand=validationCommand
        )

        inputField.insert(0, defaultText)
        canvas.create_window(positionX, positionY, window=inputField)
        return inputField

    def createColorSquare(self, positionX, positionY, squareSize, squareColor, onClickCommand, isSelected=False):
        """Dessine un carré de couleur interactif, souvent utilisé pour la sélection."""

        colorMap = {
            "light_green": "#B4E046",
            "shocking_pink": "#FA0080"
        }
        fillColor = colorMap.get(squareColor, squareColor)
        canvas = self.guiCore.getCanvas()
        halfSize = squareSize // 2
        outlineColor = "gold" if isSelected else "white"
        borderWidth = 5 if isSelected else 2
        squareElement = canvas.create_rectangle(
            positionX - halfSize, positionY - halfSize, positionX + halfSize, positionY + halfSize,
            fill=fillColor, outline=outlineColor, width=borderWidth
        )

        def onEnter(event):
            canvas.config(cursor="hand2")
            if not isSelected: canvas.itemconfig(squareElement, width=4)

        def onLeave(event):
            canvas.config(cursor="")
            if not isSelected: canvas.itemconfig(squareElement, width=2)

        def onClick(event):
            canvas.config(cursor="")
            onClickCommand()

        canvas.tag_bind(squareElement, "<Enter>", onEnter)
        canvas.tag_bind(squareElement, "<Leave>", onLeave)
        canvas.tag_bind(squareElement, "<Button-1>", onClick)
        return squareElement

    def createPlayerBox(self, positionX, positionY, titleText, defaultName, currentColor, onColorCycle, onRemove=None,
                        isAddBox=False, onAdd=None):
        """Crée un panneau structuré contenant les détails et réglages d'un joueur."""
        canvas = self.guiCore.getCanvas()
        boxWidth = 260
        boxHeight = 350
        canvas.create_rectangle(
            positionX - boxWidth // 2, positionY - boxHeight // 2,
            positionX + boxWidth // 2, positionY + boxHeight // 2,
            fill=self.guiCore.getColor("boxBg"), outline=self.guiCore.getColor("boxOutline"), width=3
        )
        if isAddBox and onAdd:
            self.createButton(positionX, positionY, "+", onAdd, fontSize=80)
            return None

        self.createLabel(positionX, positionY - 130, titleText, fontSize=25)
        inputField = self.createEntry(positionX, positionY - 50, defaultName)
        inputField.config(width=12)

        self.createLabel(positionX, positionY + 30, self.guiCore.getText("local", "colorClick"), fontSize=15)
        self.createColorSquare(positionX, positionY + 80, 60, currentColor, onColorCycle)

        if onRemove:
            self.createButton(positionX, positionY + 140, self.guiCore.getText("local", "btnRemove"), onRemove, fontSize=20)
        return inputField
