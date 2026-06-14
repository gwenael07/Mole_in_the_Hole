import math
import os
from PIL import Image, ImageTk


class BaseBoard:
    """
    Classe responsable du rendu graphique du plateau de jeu.
    Elle gère le calcul mathématique de la grille hexagonale,
    l'affichage des textures (trous, bonus, taupes) et les bordures de sélection.
    """

    def __init__(self, launcher):
        self.__launcher = launcher
        self.__textures = self.__launcher.getGuiTextureCache()

    def getTexture(self, relative_path, size):
        """Charge et met en cache une image."""
        path = f"assets/textures/{relative_path}.png"
        key = (relative_path, size)

        if key not in self.__textures:
            if not os.path.exists(path):
                return None

            img = Image.open(path).convert("RGBA")
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            self.__textures[key] = ImageTk.PhotoImage(img)

        return self.__textures[key]

    def getHexagonPoints(self, xCenter, yCenter, radius):
        """Calcule les 6 sommets d'un hexagone pointant vers le haut."""
        points = []
        for i in range(6):
            angleRad = math.radians(60 * i - 30)
            points.append(xCenter + radius * math.cos(angleRad))
            points.append(yCenter + radius * math.sin(angleRad))
        return points

    def drawHexagon(self, canvas, hexagonMap, xCenter, yCenter,
                    radius, row, col, fillColor, outlineColor, outlineWidth):
        """Dessine un polygone sur le Canvas et l'enregistre dans la map de collision."""
        points = self.getHexagonPoints(xCenter, yCenter, radius)

        hexId = canvas.create_polygon(
            points,
            fill=fillColor,
            outline=outlineColor,
            width=outlineWidth
        )

        hexagonMap[hexId] = (row, col)
        return hexId

    def drawPawn(self, canvas, x, y, radius, playerIndex, theme_folder):
        """Dessine la taupe correspondant au joueur donné."""
        colors = [
            self.__launcher.getPlayerColor(),
            self.__launcher.getPlayer2Color(),
            self.__launcher.getPlayer3Color(),
            self.__launcher.getPlayer4Color()
        ]

        color = colors[playerIndex - 1] if 1 <= playerIndex <= 4 else "white"

        texturePath = f"{theme_folder}/pawns/pawn_{color}"
        img = self.getTexture(texturePath, int(radius * 1.6))

        colorMap = {
            "light_green": "#B4E046",
            "shocking_pink": "#FA0080"
        }
        fallbackColor = colorMap.get(color, color)

        if img:
            canvas.create_image(x, y, image=img)
        else:
            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=fallbackColor, outline="white", width=2)

    def draw(self, canvas, hexagonMap: dict, boardMatrix: list,
             pawnGrid: list = None, selectedHex: tuple = None, level: int = 1):
        """
        Commande le dessin du plateau complet.
        Parcourt la matrice de l'algorithme et dessine les hexagones, trous et pions.
        """
        radius = 40
        step = radius * 2
        hexRatio = math.sqrt(3) / 2
        hStep = step * hexRatio

        # Calcul du décalage pour centrer le plateau à l'écran
        cx = self.__launcher.getCenterX()
        cy = self.__launcher.getCenterY()
        offsetX = cx - (4 * step) - (4 * step / 2)
        offsetY = cy - (4 * hStep)

        theme_folder = self.__launcher.getTextureFolder()
        base_color = self.__launcher.getEarthColor(level)
        barriersToDraw = []

        for l in range(9):
            for c in range(9):
                if boardMatrix[l][c] is not None:

                    x = (c * step) + (l * step / 2) + offsetX
                    y = (l * hStep) + offsetY
                    cell = boardMatrix[l][c]

                    if cell == 5:  # Trou
                        hex_fill = ""
                        outline_color = ""
                    else:  # Terre normale ou Bonus
                        hex_fill = base_color
                        outline_color = self.__launcher.getColor("earthOutline")

                    # Dessin de la base
                    self.drawHexagon(canvas, hexagonMap, x, y, radius, l, c,
                                     fillColor=hex_fill, outlineColor=outline_color, outlineWidth=1)

                    # Dessin des Textures de sol
                    if cell in [5, 6]:
                        if cell == 5:
                            tex_path = f"{theme_folder}/hole"
                            img_size = int(radius * 2)
                            fallback_color = "black"
                        else:
                            tex_path = f"{theme_folder}/bonus"
                            img_size = int(radius * 1.4)
                            fallback_color = "yellow"

                        img = self.getTexture(tex_path, img_size)

                        if img:
                            canvas.create_image(x, y, image=img)
                        else:
                            canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=fallback_color, outline="")

                        if cell == 5 and level == 4:
                            isOnline = self.__launcher.getNetworkClient() is not None
                            activeMode = self.__launcher.getOnlineMode() if isOnline else self.__launcher.getLocalMode()

                            if activeMode == "classic":
                                game = self.__launcher.getGame()
                                if game and game.playerCanPlay() == 2:
                                    barriersToDraw.append((x, y, radius))

                    # Bordure de Sélection
                    if selectedHex == (l, c):
                        points = self.getHexagonPoints(x, y, radius)
                        canvas.create_polygon(points, fill="", outline=self.__launcher.getColor("btnHover"), width=4)

                    # Dessin des Taupes
                    if pawnGrid and pawnGrid[l][c]:
                        self.drawPawn(canvas, x, y, radius, pawnGrid[l][c], theme_folder)

        # Dessin des barrières
        for (xCenter, yCenter, r) in barriersToDraw:
            borderColor = self.__launcher.getColor("barrierColor")
            borderWidth = 8
            offset = 6

            dx1 = offset * math.cos(math.radians(240))
            dy1 = offset * math.sin(math.radians(240))
            ptsTL = self.getHexagonPoints(xCenter + dx1, yCenter + dy1, r)
            canvas.create_line(ptsTL[8], ptsTL[9], ptsTL[10], ptsTL[11], fill=borderColor, width=borderWidth,
                               capstyle="round")

            dx2 = offset * math.cos(math.radians(0))
            dy2 = offset * math.sin(math.radians(0))
            ptsR = self.getHexagonPoints(xCenter + dx2, yCenter + dy2, r)
            canvas.create_line(ptsR[0], ptsR[1], ptsR[2], ptsR[3], fill=borderColor, width=borderWidth,
                               capstyle="round")

            dx3 = offset * math.cos(math.radians(120))
            dy3 = offset * math.sin(math.radians(120))
            ptsBL = self.getHexagonPoints(xCenter + dx3, yCenter + dy3, r)
            canvas.create_line(ptsBL[4], ptsBL[5], ptsBL[6], ptsBL[7], fill=borderColor, width=borderWidth,
                               capstyle="round")