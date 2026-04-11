TP5 - Chat en raw socket

J'ai été bloqué pendant 1 semaine à debugger et refaire de A à Z 3 serveurs differents alors qu'en faite le problème venait à 100% uniquement du MacOS qui tolère très mal les sockets RAW pour des raisons que vous connaissez sans doute déjà (sécurité, proctection, etc)

J'ai donc eu l'idée d'envoyer exactement les mêmes mauvais programmes que je pensais défaillant par mail et installer une vm linux sur lequel je me logue en SSH sur des terminaux parallèles de mon mac. Ensuite je lances des flux de commandes en shell et je constate 0 ERREUR. les programmes étaient bons depuis le début. Ils n'arrivaient pas à communiquer simplement à cause du mac.
Dans ce TP, le but etait de reprendre mon ancien mini chat fait avec des sockets classiques (`sock_stream`) et d'essayer de refaire le meme principe en raw socket.

J'ai donc garde l'idee generale du TP precedent :

- un client s'identifie au debut ;
- le serveur garde la liste des clients connectes ;
- un client peut choisir un autre client ;
- les messages sont ensuite transmis par le serveur.

Au debut, l'identification est envoyee en XML, puis le reste passe en JSON.

Le programme permet :

- d'envoyer une identification de debut en XML ;
- de recevoir la liste des autres clients connectes ;
- de choisir un destinataire avec son id ;
- d'envoyer un message ;
- d'afficher des notifications comme `CONNEXION`, `DECONNEXION`, `ECRITURE`, `ETAT` et `CHAT`.

- `server-complet-raw.py` est comme d'habitude le serveur principal ;
- `client-complet-raw.py`, le client principal ;
- `iptcp_header.py` est une extension modulaire de fichier que j'ai créé pour regrouper toutes les fonctions de traitement TCP/IP. Je les ai separé pour une lisibilité plus claire


Le code reste entierement en raw socket, car c'est ce qui est demande dans le TP.
Par contre, sur macOS, ce type de test peut etre sensible et il faut en general lancer le programme avec `sudo`.

Pour le Serveur

cd /Users/alykouma/TPs-Python/TP5
sudo python3 server-complet-raw.py --hote 192.0.0.2


Dans deux autres terminaux :

cd /Users/alykouma/TPs-Python/TP5
sudo python3 client-complet-raw.py --hote 192.0.0.2 --nom Aly --lieu Paris



cd /Users/alykouma/TPs-Python/TP5
sudo python3 client-complet-raw.py --hote 192.0.0.2 --nom Aly2 --lieu Orsay

Le tp ne change rien à la logique fonctionnel du précédent mais je suis maintenant en mesure de faire : 
- la construction manuelle des entetes IP et TCP pour la partie raw ;
- une gestion plus claire des etats des clients ;
- des messages d'erreur plus lisibles.

Conclusion

Ce TP m'a surtout permis de voir la difference entre une utilisation classique des sockets et une utilisation beaucoup plus bas niveau avec les raw sockets. La partie raw est plus proche du fonctionnement reseau reel, mais elle est aussi plus delicate a faire marcher correctement selon le systeme d'exploitation.

Coding:
Exo1 de conversion entier bit avec le nombre de 1 trivial car il y a dejà des fonctions natives pythons pour ça
Exo2 Il y a une erreur dans l'enoncé qui est importante car 73 commence par 1 et non 0. Le 0 devant n'a aucune importance tout comme il n'était pas indiqué pour le binaire du 7:1101 . Donc c'est donc logique que la reponse du swap de mon programme sera differente.
Fichier : 'coding.py'