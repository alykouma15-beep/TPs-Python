import argparse
import datetime
import json
import threading
import time

from iptcp_header import (
    choisir_port_client,
    envoyer_paquet,
    lire_paquet_brut,
    ouvrir_socket_envoi_brut,
    ouvrir_socket_reception_brut,
    trouver_ip_locale,
)


class ClientBrut:
    def __init__(self, hote, port, nom, lieu):
        self.hote = hote
        self.port = port
        self.nom = nom
        self.lieu = lieu
        self.ip_locale = trouver_ip_locale() if hote != "127.0.0.1" else "127.0.0.1"
        self.port_local = choisir_port_client()
        self.socket_reception = ouvrir_socket_reception_brut()
        self.socket_envoi = ouvrir_socket_envoi_brut()
        self.menu = None
        self.demande_choix = None
        self.demande_continuer = None
        self.dernier_message_serveur = None
        self.tampon = ""
        self.sequence = 1

    def envoyer_texte(self, texte):
        message = texte.encode("utf-8")
        envoyer_paquet(
            self.socket_envoi,
            self.ip_locale,
            self.hote,
            self.port_local,
            self.port,
            message,
            numero_sequence=self.sequence,
        )
        self.sequence += max(1, len(message))

    def envoyer_json(self, message):
        self.envoyer_texte(json.dumps(message) + "\n")

    def envoyer_identite_xml(self):
        xml_a_envoyer = f"""
<client>
    <nom>{self.nom}</nom>
    <date_connexion>{datetime.date.today()}</date_connexion>
    <lieu>{self.lieu}</lieu>
</client>
""".strip()
        self.envoyer_texte(xml_a_envoyer)

    def attendre_paquet(self, timeout=None):
        ancien_timeout = self.socket_reception.gettimeout()
        self.socket_reception.settimeout(timeout)

        try:
            while True:
                paquet, _ = self.socket_reception.recvfrom(65535)
                infos_paquet = lire_paquet_brut(paquet)

                if not infos_paquet:
                    continue

                if infos_paquet["ip_source"] != self.hote or infos_paquet["port_source"] != self.port:
                    continue

                if infos_paquet["ip_destination"] != self.ip_locale or infos_paquet["port_destination"] != self.port_local:
                    continue

                return infos_paquet["donnees"].decode("utf-8", errors="ignore")
        finally:
            self.socket_reception.settimeout(ancien_timeout)

    def recevoir_json(self, timeout=None):
        while True:
            if "\n" not in self.tampon:
                self.tampon += self.attendre_paquet(timeout=timeout)
                continue

            ligne, self.tampon = self.tampon.split("\n", 1)
            ligne = ligne.strip()
            if not ligne:
                continue

            try:
                return json.loads(ligne)
            except json.JSONDecodeError:
                print("message ignore:", ligne)

    def ecouter_messages(self):
        while True:
            message = self.recevoir_json()
            type_message = message.get("type")

            if type_message == "ECRITURE":
                print(f"Client {message['idClient']} est en train d'ecrire...")
                continue

            if type_message == "MENU":
                self.menu = message
                continue

            if type_message == "CHOISISSEZ":
                self.demande_choix = message
                continue

            if type_message == "CONTINUER":
                self.demande_continuer = message
                continue

            if type_message == "MESSAGE":
                self.dernier_message_serveur = message["contenu"]
                print("nouveau message recu:", message["contenu"])
                continue

            if type_message in ["ETAT", "CONNEXION", "DECONNEXION"]:
                print(message)
                continue

            if type_message == "CHAT":
                print(f"Client {message['emetteur']} dit -> {message['contenu']}")


def recuperer_arguments():
    analyseur = argparse.ArgumentParser(description="Client de chat en raw socket")
    analyseur.add_argument("--hote", "--host", dest="hote", default=trouver_ip_locale())
    analyseur.add_argument("--port", type=int, default=12345)
    analyseur.add_argument("--nom", default="Aly")
    analyseur.add_argument("--lieu", default="Paris")
    return analyseur.parse_args()


def lancer_client_brut(args):
    client = ClientBrut(args.hote, args.port, args.nom, args.lieu)

    print(f"connexion raw vers {client.hote}:{client.port} depuis {client.ip_locale}:{client.port_local}")
    client.envoyer_identite_xml()
    message_depart = client.recevoir_json(timeout=5)

    if message_depart and str(message_depart.get("type", "")).startswith("informations sur"):
        autres_clients = {}
        for cle, valeur in message_depart.items():
            if cle != "type":
                autres_clients[cle] = valeur

        if autres_clients:
            print(f"les autres clients connectes sont : \n{autres_clients}")
        else:
            print("Pas d'autres clients connectes pour le moment")

    client.envoyer_json({"type": "HELLO"})
    thread = threading.Thread(target=client.ecouter_messages, daemon=True)
    thread.start()

    while True:
        while not client.menu:
            time.sleep(0.1)
        print(f"Clients dispo pour chatter: {client.menu}")
        client.menu = None

        while not client.demande_choix:
            time.sleep(0.1)
        print(client.demande_choix)
        client.demande_choix = None

        texte_id = input().strip()
        if not texte_id:
            print("aucun id saisi, fermeture du client")
            return

        try:
            id_client = int(texte_id)
        except ValueError:
            print("merci de saisir un id numerique")
            continue

        client.dernier_message_serveur = None
        client.envoyer_json({"type": "CHOIX", "idClient": id_client})

        while client.dernier_message_serveur is None:
            time.sleep(0.1)

        if client.dernier_message_serveur != "parfait ecrivez votre message":
            client.dernier_message_serveur = None
            continue

        client.dernier_message_serveur = None
        client.envoyer_json({"type": "ETAT", "changement": "OCCUPE"})
        print("choix envoye au serveur")

        texte = input()
        client.envoyer_json({"type": "CHAT", "contenu": texte})
        print("message envoye au serveur")

        while not client.demande_continuer:
            time.sleep(0.1)
        print(client.demande_continuer)
        client.demande_continuer = None

        choix = input().strip().lower()
        if choix == "n":
            client.envoyer_json({"type": "CONTINUER", "choix": choix})
            print("saisie envoyee au serveur")
            print("deconnexion...")
            return

        client.envoyer_json({"type": "ETAT", "changement": "LIBRE"})
        client.envoyer_json({"type": "CONTINUER", "choix": choix})
        print("saisie envoyee au serveur")


def lancer_client(args):
    try:
        lancer_client_brut(args)
    except PermissionError:
        print("Les raw sockets necessitent les droits administrateur.")
        print("Relance par exemple avec : sudo python3 client-complet-raw.py --nom Aly")
    except TimeoutError:
        print("erreur raw socket: timed out")
        print("sur macOS, le raw socket entre processus sur la meme machine peut ne jamais repondre")
    except OSError as erreur:
        print(f"erreur raw socket: {erreur}")


def main():
    args = recuperer_arguments()

    try:
        lancer_client(args)
    except KeyboardInterrupt:
        print("\narret du client")
    except ConnectionRefusedError:
        print("serveur introuvable: lance d'abord python3 server-complet-raw.py")


if __name__ == "__main__":
    main()
