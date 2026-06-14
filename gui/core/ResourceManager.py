import os
import json
from audio.audioManager import AudioManager

class ResourceManager:
    """
    Gère les ressources de l'application (textes/traductions, thèmes, textures, sons).
    """

    def __init__(self, guiCore):
        self.guiCore = guiCore
        self.__currentLang = "fr"
        self.__currentThemeName = "meadow"
        self.__soundEnabled = True
        self.__volume = 50
        self.__audioSystem = AudioManager()
        self.__texts = {}
        self.__themes = {}
        self.__guiTextureCache = {}

    def loadResources(self):
        """Charge les fichiers de traduction JSON et les configurations des thèmes visuels."""
        languagePath = os.path.join("assets", "lang", f"{self.__currentLang}.json")
        with open(languagePath, "r", encoding="utf-8") as jsonFile:
            self.__texts = json.load(jsonFile)

        themePath = os.path.join("assets", "themes", "themes.json")
        with open(themePath, "r", encoding="utf-8") as jsonFile:
            self.__themes = json.load(jsonFile)

    def getCurrentLang(self):
        return self.__currentLang

    def setLanguage(self, langCode):
        """Change la langue du jeu et recharge instantanément les textes."""
        if langCode in ["fr", "en", "de", "it", "es"]:
            self.__currentLang = langCode
            self.loadResources()

    def getText(self, targetPage, textKey):
        """Récupère une ligne de texte traduite dans le dictionnaire JSON localisé."""
        return self.__texts.get(targetPage, {}).get(textKey, f"MISSING_{textKey}")

    def getColor(self, elementKey):
        """Récupère un code couleur (HEX ou nom de base) dépendant du thème visuel."""
        return self.__themes.get(self.__currentThemeName, {}).get(elementKey, "red")

    def getThemesList(self):
        return list(self.__themes.keys())

    def getCurrentThemeName(self):
        return self.__currentThemeName

    def setThemeName(self, targetThemeName):
        if targetThemeName in self.__themes:
            self.__currentThemeName = targetThemeName
            self.updateMusic()

    def getTextureFolder(self):
        return self.__themes[self.__currentThemeName]["texture_folder"]

    def getEarthColor(self, levelIndex):
        return self.__themes[self.__currentThemeName]["earth_levels"][str(levelIndex)]

    def getGuiTextureCache(self):
        return self.__guiTextureCache

    def isSoundEnabled(self):
        return self.__soundEnabled

    def setSoundEnabled(self, soundState):
        self.__soundEnabled = soundState
        self.updateMusic()

    def updateMusic(self, forceRestart=False):
        """
        Met à jour la musique de fond en fonction du thème, du niveau actuel et de l'état du son.
        """
        if not self.isSoundEnabled():
            self.__audioSystem.stopMusic()
            return

        isEpicMode = False
        game = self.guiCore.getGame()
        if game:
            try:
                currentLevelIndex = game.getCurrentLevel()
                if self.guiCore.getNetworkClient():
                    totalBoards = self.guiCore.getOnlineLobbyData().get("boards", self.guiCore.getOnlineBoardsCount())
                else:
                    totalBoards = self.guiCore.getLocalBoardsCount()

                if currentLevelIndex >= totalBoards - 1:
                    isEpicMode = True
            except Exception:
                pass

        self.__audioSystem.playMusic(self.getCurrentThemeName(), isEpicMode, forceRestart)

    def playFootstepSound(self):
        """Déclenche l'effet sonore de mouvement approprié au thème si le son est activé."""
        if self.isSoundEnabled():
            self.__audioSystem.playMoveSound(self.getCurrentThemeName())

    def playVoice(self, voiceName):
        """Déclenche une voix d'annonce spécifique si le son est activé."""
        if self.isSoundEnabled():
            self.__audioSystem.playVoice(voiceName)
