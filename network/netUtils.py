import struct
import json


def sendJson(targetSocket, dataObject):
    """
    Sérialise un objet Python en JSON et l'envoie via un socket TCP.

    Pour s'assurer que le destinataire sait exactement combien d'octets il doit lire, cette fonction
    précède le contenu JSON d'un en-tête de 4 octets contenant la longueur du message,
    sous forme d'un entier non signé au format Big-Endian.

    Args:
        targetSocket (socket.socket) : Le socket TCP connecté par lequel envoyer les données.
        dataObject (dict) : Le dictionnaire Python (ou tout autre objet sérialisable) à envoyer.
    """
    jsonBytes = json.dumps(dataObject).encode("utf-8")
    lengthHeader = struct.pack(">I", len(jsonBytes))
    targetSocket.sendall(lengthHeader + jsonBytes)


def recvJson(sourceSocket):
    """
    Reçoit et désérialise un message JSON depuis un socket TCP.

    Cette fonction lit d'abord l'en-tête de 4 octets pour déterminer la taille du contenu entrant.
    Elle lit ensuite exactement ce nombre d'octets pour reconstruire la chaîne JSON complète avant de la décoder.
    Elle inclut une limite de sécurité de 10 Mo pour éviter l'épuisement de la mémoire en cas d'en-têtes corrompus ou malveillants.

    Args:
        sourceSocket (socket.socket) : Le socket TCP connecté depuis lequel lire.

    Returns:
        dict or None : Le dictionnaire Python désérialisé en cas de succès. Retourne
                       None si la connexion du socket est fermée proprement.

    Raises:
        ValueError : Si la longueur calculée du message dépasse la limite de 10 000 000 d'octets.
    """
    lengthHeader = receiveAllBytes(sourceSocket, 4)

    if not lengthHeader:
        return None

    messageLength = struct.unpack(">I", lengthHeader)[0]
    MAX_MESSAGE_SIZE = 10_000_000

    if messageLength > MAX_MESSAGE_SIZE:
        raise ValueError("Message too large")

    jsonBytes = receiveAllBytes(sourceSocket, messageLength)

    if not jsonBytes:
        return None

    return json.loads(jsonBytes.decode("utf-8"))


def receiveAllBytes(sourceSocket, byteCount):
    """
    Garantit la réception d'exactement `byteCount` octets.

    Le protocole TCP fonctionnant comme un flux continu, un unique appel à `sourceSocket.recv(byteCount)` n'est pas
    garanti de renvoyer tous les octets d'un coup. Cette fonction boucle et accumule les données
    jusqu'à ce que la taille exacte demandée soit atteinte.

    Args:
        sourceSocket (socket.socket) : Le socket depuis lequel lire.
        byteCount (int) : Le nombre exact d'octets à recevoir.

    Returns:
        bytearray or None : Le tableau d'octets complet de longueur demandée. Retourne None
                            si le socket se ferme avant que tous les octets ne soient reçus.
    """
    accumulatedBytes = bytearray()

    while len(accumulatedBytes) < byteCount:
        dataChunk = sourceSocket.recv(byteCount - len(accumulatedBytes))
        if not dataChunk:
            return None
        accumulatedBytes.extend(dataChunk)

    return accumulatedBytes