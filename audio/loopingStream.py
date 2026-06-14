import miniaudio


class LoopingStream:
    """
    Un flux audio personnalisé conçu pour intercepter la fin d'un fichier (StopIteration)
    et relancer automatiquement la lecture en boucle infinie avec miniaudio.
    """
    def __init__(self, filepath):
        """
        Initialise le flux en boucle pour un fichier audio donné.

        Args:
            filepath (str) : Le chemin d'accès vers le fichier audio à lire en boucle.
        """
        self.filepath = filepath
        self.stream = miniaudio.stream_file(filepath)

    def send(self, framecount):
        """
        Envoie la quantité exacte de frames audio demandée par le périphérique de lecture.
        Si la fin du fichier est atteinte, le flux actuel est fermé et un nouveau est ouvert instantanément.

        Args:
            framecount (int) : Le nombre de frames audio requis par miniaudio.

        Returns:
            bytes : Les données audio brutes lues à envoyer aux haut-parleurs.
        """
        try:
            return self.stream.send(framecount)
        except StopIteration:
            if hasattr(self.stream, 'close'):
                self.stream.close()
            self.stream = miniaudio.stream_file(self.filepath)
            try:
                return self.stream.send(framecount)
            except Exception:
                return b""

    def close(self):
        """
        Ferme proprement le flux audio interne s'il est ouvert.
        """
        if hasattr(self.stream, 'close'):
            self.stream.close()