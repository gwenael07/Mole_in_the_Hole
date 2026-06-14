import platform
import subprocess

def openFirewallPorts():
    """
    Ouvre les ports du pare-feu sur la machine serveur pour permettre de jouer en réseau local (uniquement sur Windows).
    """
    if platform.system() != "Windows":
        return

    tcpRuleCommand = 'netsh advfirewall firewall add rule name="TempPythonGame_TCP" dir=in action=allow protocol=TCP localport=5000 profile=any'
    udpRuleCommand = 'netsh advfirewall firewall add rule name="TempPythonGame_UDP" dir=in action=allow protocol=UDP localport=5005 profile=any'

    try:
        subprocess.run(tcpRuleCommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(udpRuleCommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass


def closeFirewallPorts():
    """
    Ferme les ports du pare-feu précédemment ouverts (uniquement sur Windows).
    """
    if platform.system() != "Windows":
        return

    tcpRuleCommand = 'netsh advfirewall firewall delete rule name="TempPythonGame_TCP"'
    udpRuleCommand = 'netsh advfirewall firewall delete rule name="TempPythonGame_UDP"'

    try:
        subprocess.run(tcpRuleCommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(udpRuleCommand, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass