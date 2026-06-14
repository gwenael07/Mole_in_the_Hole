import socket

def getAllLocalIps():
    """
    Récupère la liste de toutes les adresses IPv4 locales attribuées à la machine actuelle.

    Cette fonction utilise deux méthodes :
    Méthode 1 :
        Elle crée une communication UDP factice vers un DNS public et ajoute l'IP locale correspondante à la liste.
    Méthode 2 :
        Elle résout le nom d'hôte (hostname) local pour découvrir d'autres interfaces IPv4 actives.

    Elle filtre les adresses IPv6, l'adresse de bouclage locale (127.0.0.1) et les doublons.

    Returns:
        list : Une liste de chaînes de caractères contenant toutes les adresses IPv4 attribuées à la machine.
               Si aucune adresse n'est trouvée, elle retourne ['127.0.0.1'] (localhost).
    """
    localIpAddresses = []

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dummySocket:
            dummySocket.connect(("8.8.8.8", 80))
            localIpAddresses.append(dummySocket.getsockname()[0])
    except Exception:
        pass

    try:
        localHostname = socket.gethostname()
        for addressInfo in socket.getaddrinfo(localHostname, None):
            extractedIp = addressInfo[4][0]
            if "." in extractedIp and extractedIp != "127.0.0.1" and extractedIp not in localIpAddresses:
                localIpAddresses.append(extractedIp)
    except Exception:
        pass

    return localIpAddresses if localIpAddresses else ["127.0.0.1"]