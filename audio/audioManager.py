import miniaudio
import os
import threading
from audio.loopingStream import LoopingStream

class AudioManager:
    """
    Gestionnaire audio principal de l'application chargé de la musique de fond en boucle,
    des effets sonores de pas et de la diffusion des voix d'annonces.
    """
    def __init__(self):
        """
        Initialise le gestionnaire audio avec trois périphériques de lecture distincts
        pour permettre la superposition de la musique, des bruitages et des voix sans coupure.
        """
        self.__musicDevice = miniaudio.PlaybackDevice()
        self.__sfxDevice = miniaudio.PlaybackDevice()
        self.__voiceDevice = miniaudio.PlaybackDevice()
        self.__musicGenerator = None
        self.__sfxStream = None
        self.__voiceStream = None
        self.__currentFile = None
        self.__themeMap = {
            "iceflow": "ice_floe",
            "volcano": "volcano",
            "desert": "desert",
            "meadow": "meadow"
        }

    def playMusic(self, themeName, isEpic, forceRestart=False):
        """
        Lance ou met à jour la musique de fond en boucle correspondant au thème visuel actif.

        Args:
            themeName (str) : Le nom du thème sélectionné (ex: "meadow", "desert").
            isEpic (bool) : Si True, charge la variante épique du morceau (utilisée pour les derniers plateaux).
            forceRestart (bool) : Si True, force le morceau à recommencer du début même s'il est déjà en cours de lecture.
        """
        folder = self.__themeMap.get(themeName, themeName)
        suffix = "_epic" if isEpic else ""
        filepath = os.path.join("audio", "music", folder, f"{folder}{suffix}.mp3")

        if not os.path.exists(filepath):
            return

        if self.__currentFile == filepath and self.__musicDevice.running and not forceRestart:
            return

        self.__currentFile = filepath

        if self.__musicDevice.running:
            self.__musicDevice.close()

        self.__musicDevice = miniaudio.PlaybackDevice()
        self.__musicGenerator = LoopingStream(filepath)
        self.__musicDevice.start(self.__musicGenerator)

    def stopMusic(self):
        """
        Arrête immédiatement la musique de fond en coupant son périphérique de lecture dédié.
        """
        if self.__musicDevice.running:
            self.__musicDevice.close()

    def playMoveSound(self, themeName):
        """
        Déclenche l'effet sonore des pas d'un pion dans un thread séparé en fonction du thème de plateau actuel.

        Args:
            themeName (str) : Le nom du thème actif pour charger le bruit de pas correspondant (ex: "iceflow", "volcano").
        """
        def _play_sound():
            folder = self.__themeMap.get(themeName, themeName)
            filepath = os.path.join("audio", "sound_effects", "footsteps", folder, f"footsteps_{folder}.mp3")

            if not os.path.exists(filepath):
                return

            if self.__sfxDevice.running:
                self.__sfxDevice.close()

            self.__sfxDevice = miniaudio.PlaybackDevice()
            self.__sfxStream = miniaudio.stream_file(filepath)
            self.__sfxDevice.start(self.__sfxStream)

        threading.Thread(target=_play_sound, daemon=True).start()

    def playVoice(self, voiceName):
        """
        Joue une annonce vocale spécifique (ex: victoire, élimination) dans un thread asynchrone dédié.

        Args:
            voiceName (str) : Le nom du fichier audio de la voix à jouer (sans l'extension .mp3).
        """
        def _play_voice():
            filepath = os.path.join("audio", "sound_effects", "voices", f"{voiceName}.mp3")

            if not os.path.exists(filepath):
                print(f"[AUDIO] Voice not found: {filepath}")
                return

            if self.__voiceDevice.running:
                self.__voiceDevice.close()

            self.__voiceDevice = miniaudio.PlaybackDevice()
            self.__voiceStream = miniaudio.stream_file(filepath)
            self.__voiceDevice.start(self.__voiceStream)

        threading.Thread(target=_play_voice, daemon=True).start()