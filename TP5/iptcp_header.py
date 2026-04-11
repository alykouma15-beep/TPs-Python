import os
import socket
import subprocess
import sys
from struct import pack, unpack


FENETRE_PAR_DEFAUT = 5840


class SocketEnvoiBrut:
    def __init__(self, sock, avec_entete_ip):
        self.sock = sock
        self.avec_entete_ip = avec_entete_ip


def trouver_ip_locale():
    try:
        liste = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET, socket.SOCK_DGRAM)
        for element in liste:
            ip = element[4][0]
            if ip and not ip.startswith("127."):
                return ip
    except OSError:
        pass

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sonde:
            sonde.connect(("8.8.8.8", 80))
            ip = sonde.getsockname()[0]
            if ip and not ip.startswith("127."):
                return ip
    except OSError:
        pass

    try:
        sortie = subprocess.check_output(["ifconfig"], text=True)
        for ligne in sortie.splitlines():
            ligne = ligne.strip()
            if ligne.startswith("inet "):
                ip = ligne.split()[1]
                if ip and not ip.startswith("127."):
                    return ip
    except (OSError, subprocess.CalledProcessError, IndexError):
        pass

    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip and not ip.startswith("127."):
            return ip
    except OSError:
        pass

    return "127.0.0.1"


def somme_controle(donnees):
    if len(donnees) % 2:
        donnees += b"\x00"

    total = 0
    for i in range(0, len(donnees), 2):
        total += (donnees[i] << 8) + donnees[i + 1]
        total = (total & 0xFFFF) + (total >> 16)

    return (~total) & 0xFFFF


def creer_entete_ip(ip_source, ip_destination, longueur_message, identifiant=54321):
    version = 4
    longueur_entete = 5
    version_et_longueur = (version << 4) + longueur_entete
    type_service = 0
    longueur_totale = 20 + longueur_message
    fragment = 0
    ttl = 64
    protocole = socket.IPPROTO_TCP
    checksum_ip = 0
    adresse_source = socket.inet_aton(ip_source)
    adresse_destination = socket.inet_aton(ip_destination)

    entete_sans_checksum = pack(
        "!BBHHHBBH4s4s",
        version_et_longueur,
        type_service,
        longueur_totale,
        identifiant & 0xFFFF,
        fragment,
        ttl,
        protocole,
        checksum_ip,
        adresse_source,
        adresse_destination,
    )
    checksum_ip = somme_controle(entete_sans_checksum)

    return pack(
        "!BBHHHBBH4s4s",
        version_et_longueur,
        type_service,
        longueur_totale,
        identifiant & 0xFFFF,
        fragment,
        ttl,
        protocole,
        checksum_ip,
        adresse_source,
        adresse_destination,
    )


def creer_entete_tcp(
    message,
    ip_source,
    ip_destination,
    port_source,
    port_destination,
    numero_sequence=454,
    numero_ack=0,
    syn=1,
    ack=0,
    psh=1,
    fin=0,
    rst=0,
    urg=0,
):
    decalage = 5
    offset_reserve = (decalage << 4) + 0
    drapeaux = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
    fenetre = FENETRE_PAR_DEFAUT
    checksum_tcp = 0
    pointeur_urgence = 0

    entete_sans_checksum = pack(
        "!HHLLBBHHH",
        port_source,
        port_destination,
        numero_sequence,
        numero_ack,
        offset_reserve,
        drapeaux,
        fenetre,
        checksum_tcp,
        pointeur_urgence,
    )

    pseudo_entete = pack(
        "!4s4sBBH",
        socket.inet_aton(ip_source),
        socket.inet_aton(ip_destination),
        0,
        socket.IPPROTO_TCP,
        len(entete_sans_checksum) + len(message),
    )
    checksum_tcp = somme_controle(pseudo_entete + entete_sans_checksum + message)

    return pack(
        "!HHLLBBHHH",
        port_source,
        port_destination,
        numero_sequence,
        numero_ack,
        offset_reserve,
        drapeaux,
        fenetre,
        checksum_tcp,
        pointeur_urgence,
    )


def creer_paquet(entete_ip, entete_tcp, message):
    return entete_ip + entete_tcp + message


def construire_segment_tcp(ip_source, ip_destination, port_source, port_destination, message, numero_sequence=454):
    return (
        creer_entete_tcp(
            message,
            ip_source,
            ip_destination,
            port_source,
            port_destination,
            numero_sequence=numero_sequence,
            syn=0,
            ack=0,
            psh=1,
        )
        + message
    )


def construire_paquet_brut(ip_source, ip_destination, port_source, port_destination, message, numero_sequence=454):
    entete_tcp = creer_entete_tcp(
        message,
        ip_source,
        ip_destination,
        port_source,
        port_destination,
        numero_sequence=numero_sequence,
        syn=0,
        ack=0,
        psh=1,
    )
    entete_ip = creer_entete_ip(
        ip_source,
        ip_destination,
        len(entete_tcp) + len(message),
        identifiant=numero_sequence,
    )
    return creer_paquet(entete_ip, entete_tcp, message)


def construire_paquet_a_envoyer(socket_envoi, ip_source, ip_destination, port_source, port_destination, message, numero_sequence=454):
    if socket_envoi.avec_entete_ip:
        return construire_paquet_brut(
            ip_source,
            ip_destination,
            port_source,
            port_destination,
            message,
            numero_sequence=numero_sequence,
        )

    return construire_segment_tcp(
        ip_source,
        ip_destination,
        port_source,
        port_destination,
        message,
        numero_sequence=numero_sequence,
    )


def envoyer_paquet(socket_envoi, ip_source, ip_destination, port_source, port_destination, message, numero_sequence=454):
    paquet = construire_paquet_a_envoyer(
        socket_envoi,
        ip_source,
        ip_destination,
        port_source,
        port_destination,
        message,
        numero_sequence=numero_sequence,
    )
    socket_envoi.sock.sendto(paquet, (ip_destination, 0))


def lire_paquet_brut(paquet):
    if len(paquet) < 40:
        return None

    version_ihl = paquet[0]
    version = version_ihl >> 4
    taille_ip = (version_ihl & 0x0F) * 4

    if version != 4 or len(paquet) < taille_ip + 20:
        return None

    entete_ip = unpack("!BBHHHBBH4s4s", paquet[:20])
    ip_source = socket.inet_ntoa(entete_ip[8])
    ip_destination = socket.inet_ntoa(entete_ip[9])

    debut_tcp = taille_ip
    if len(paquet) < debut_tcp + 20:
        return None

    entete_tcp = unpack("!HHLLBBHHH", paquet[debut_tcp:debut_tcp + 20])
    port_source, port_destination, sequence, ack, offset_reserve, drapeaux, fenetre, checksum_tcp, urgence = entete_tcp
    taille_tcp = (offset_reserve >> 4) * 4
    donnees = paquet[debut_tcp + taille_tcp:]

    return {
        "ip_source": ip_source,
        "ip_destination": ip_destination,
        "port_source": port_source,
        "port_destination": port_destination,
        "sequence": sequence,
        "ack": ack,
        "drapeaux": drapeaux,
        "donnees": donnees,
    }


def ouvrir_socket_envoi_brut():
    if sys.platform == "darwin":
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        return SocketEnvoiBrut(sock, False)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        return SocketEnvoiBrut(sock, True)
    except PermissionError:
        raise
    except OSError:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        return SocketEnvoiBrut(sock, False)


def ouvrir_socket_reception_brut():
    return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)


def choisir_port_client():
    morceau_pid = os.getpid() % 10000
    return 20000 + morceau_pid
