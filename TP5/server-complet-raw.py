import argparse
import json
import xml.etree.ElementTree as ET

from iptcp_header import envoyer_paquet, lire_paquet_brut, ouvrir_socket_envoi_brut, ouvrir_socket_reception_brut, trouver_ip_locale


class ServeurBrut:
    def __init__(self, hote, port):
        self.hote = hote
        self.port = port
        self.socket_reception = ouvrir_socket_reception_brut()
        self.socket_envoi = ouvrir_socket_envoi_brut()
        self.clients = {}
        self.ids_clients = {}
        self.prochain_id = 1

    def envoyer_texte(self, cle_client, texte):
        infos = self.clients[cle_client]
        message = texte.encode("utf-8")
        envoyer_paquet(
            self.socket_envoi,
            self.hote,
            infos["ip"],
            self.port,
            infos["port"],
            message,
            numero_sequence=infos["sequence"],
        )
        infos["sequence"] += max(1, len(message))

    def envoyer_json(self, cle_client, message):
        self.envoyer_texte(cle_client, json.dumps(message) + "\n")

    def diffuser_json(self, message, exclure=None):
        for cle_client, infos in list(self.clients.items()):
            if cle_client != exclure and infos["pret"]:
                self.envoyer_json(cle_client, message)

    def envoyer_menu(self, cle_client):
        if not self.clients[cle_client]["pret"]:
            return

        menu = {"type": "MENU"}
        for autre_cle, autre_client in self.clients.items():
            if autre_cle == cle_client or not autre_client["pret"]:
                continue
            menu[f"clientid{autre_client['id']}"] = {
                "nom": autre_client["nom"],
                "etat": autre_client["etat"],
                "adresse": [autre_client["ip"], autre_client["port"]],
            }

        self.envoyer_json(cle_client, menu)
        self.envoyer_json(
            cle_client,
            {
                "type": "CHOISISSEZ",
                "contenu": "choisissez le client avec qui vous voulez communiquer en tapant son id",
            },
        )

    def envoyer_infos_depart(self, cle_client):
        infos_depart = {"type": "informations sur le nombre de clients connectes"}
        for autre_cle, autre_client in self.clients.items():
            if autre_cle == cle_client or not autre_client["pret"]:
                continue
            infos_depart[f"clientid{autre_client['id']}"] = {
                "nom": autre_client["nom"],
                "etat": autre_client["etat"],
                "adresse": [autre_client["ip"], autre_client["port"]],
            }

        self.envoyer_json(cle_client, infos_depart)

    def recuperer_clients_prets(self):
        liste = []
        for cle_client, infos in self.clients.items():
            if infos["pret"]:
                liste.append(cle_client)
        return liste

    def mettre_a_jour_les_menus(self):
        liste = self.recuperer_clients_prets()
        if len(liste) < 2:
            for cle_client in liste:
                self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": "Le serveur attend minimum 2 clients"})
            return

        for cle_client in liste:
            self.envoyer_menu(cle_client)

    def enregistrer_client(self, cle_client, xml_recu):
        racine = ET.fromstring(xml_recu)
        id_client = self.prochain_id
        self.prochain_id += 1

        infos = self.clients[cle_client]
        infos["id"] = id_client
        infos["nom"] = racine.findtext("nom", default=f"client{id_client}")
        infos["date_connexion"] = racine.findtext("date_connexion", default="")
        infos["lieu"] = racine.findtext("lieu", default="")
        infos["identifie"] = True
        infos["pret"] = False
        self.ids_clients[id_client] = cle_client

        print(
            f"connecte au client {infos['nom']} ({infos['ip']}:{infos['port']}) "
            f"le {infos['date_connexion']} a {infos['lieu']}"
        )
        self.envoyer_infos_depart(cle_client)

    def supprimer_client(self, cle_client):
        infos = self.clients.pop(cle_client, None)
        if not infos:
            return

        self.ids_clients.pop(infos["id"], None)

        if infos["pret"]:
            self.diffuser_json({"type": "DECONNEXION", "idClient": infos["id"]})
            self.mettre_a_jour_les_menus()

        print(f"client {infos['id']} deconnecte")

    def traiter_message_json(self, cle_client, message):
        infos_client = self.clients[cle_client]
        type_message = message.get("type")

        if type_message == "HELLO":
            if not infos_client["pret"]:
                infos_client["pret"] = True
                self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": "Welcome"})
                self.diffuser_json({"type": "CONNEXION", "idClient": infos_client["id"]}, exclure=cle_client)
            self.mettre_a_jour_les_menus()
            return

        if type_message == "CHOIX":
            id_cible = message.get("idClient")
            cle_cible = self.ids_clients.get(id_cible)

            if not cle_cible or cle_cible == cle_client or not self.clients[cle_cible]["pret"]:
                self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": "client inexistant"})
                self.mettre_a_jour_les_menus()
                return

            infos_client["id_cible"] = id_cible
            self.envoyer_json(cle_cible, {"type": "ECRITURE", "idClient": infos_client["id"]})
            self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": "parfait ecrivez votre message"})
            return

        if type_message == "CHAT":
            id_cible = infos_client.get("id_cible")
            cle_cible = self.ids_clients.get(id_cible)

            if not cle_cible:
                self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": "client inexistant"})
                self.mettre_a_jour_les_menus()
                return

            contenu = message.get("contenu", "")
            self.envoyer_json(cle_cible, {"type": "CHAT", "emetteur": infos_client["id"], "contenu": contenu})
            self.envoyer_json(cle_client, {"type": "CONTINUER", "contenu": "distribuee ! voulez vous rester? y/n"})
            return

        if type_message == "CONTINUER":
            choix = str(message.get("choix", "")).strip().lower()
            infos_client["id_cible"] = None
            if choix == "n":
                self.supprimer_client(cle_client)
                return
            self.mettre_a_jour_les_menus()
            return

        if type_message == "ETAT":
            changement = message.get("changement", "INCONNU")
            infos_client["etat"] = changement
            self.diffuser_json({"type": "ETAT", "idClient": infos_client["id"], "changement": changement})
            return

        self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": f"type ignore: {type_message}"})

    def lancer(self):
        print(f"socket raw serveur en ecoute sur {self.hote}:{self.port}")

        while True:
            paquet, _ = self.socket_reception.recvfrom(65535)
            infos_paquet = lire_paquet_brut(paquet)

            if not infos_paquet:
                continue

            if infos_paquet["port_destination"] != self.port or infos_paquet["ip_destination"] != self.hote:
                continue

            texte = infos_paquet["donnees"].decode("utf-8", errors="ignore")
            if not texte.strip():
                continue

            cle_client = (infos_paquet["ip_source"], infos_paquet["port_source"])

            if cle_client not in self.clients:
                self.clients[cle_client] = {
                    "ip": infos_paquet["ip_source"],
                    "port": infos_paquet["port_source"],
                    "id": None,
                    "nom": "",
                    "date_connexion": "",
                    "lieu": "",
                    "identifie": False,
                    "pret": False,
                    "id_cible": None,
                    "etat": "LIBRE",
                    "sequence": 1000,
                }

            infos_client = self.clients[cle_client]

            if not infos_client["identifie"]:
                try:
                    self.enregistrer_client(cle_client, texte)
                except ET.ParseError:
                    self.clients.pop(cle_client, None)
                continue

            for ligne in texte.splitlines():
                ligne = ligne.strip()
                if not ligne:
                    continue

                try:
                    message = json.loads(ligne)
                except json.JSONDecodeError:
                    self.envoyer_json(cle_client, {"type": "MESSAGE", "contenu": f"message ignore: {ligne}"})
                    continue

                self.traiter_message_json(cle_client, message)


def recuperer_arguments():
    analyseur = argparse.ArgumentParser(description="Serveur de chat en raw socket")
    analyseur.add_argument("--hote", "--host", dest="hote", default=trouver_ip_locale())
    analyseur.add_argument("--port", type=int, default=12345)
    return analyseur.parse_args()


def lancer_serveur_brut(hote, port):
    ServeurBrut(hote, port).lancer()


def lancer_serveur(args):
    try:
        lancer_serveur_brut(args.hote, args.port)
    except PermissionError:
        print("Les raw sockets necessitent les droits administrateur.")
        print("Relance par exemple avec : sudo python3 server-complet-raw.py")
    except OSError as erreur:
        print(f"erreur raw socket: {erreur}")


def main():
    args = recuperer_arguments()

    try:
        lancer_serveur(args)
    except KeyboardInterrupt:
        print("\narret du serveur")


if __name__ == "__main__":
    main()
