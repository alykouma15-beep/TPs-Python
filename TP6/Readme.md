1) premier et deuxième exo de création de requêtes et reponses effectués et injectés dans le fichier modulaire "Exo1_2requete_response.py"

2) troisième exo du petit serveur et petit client opérationnel. Pour exécuter, lancer le serveur "exo3-petit-serveur.py" puis en BONUS j'ai rajouté la possibilité à l'utilisateur de decider en ligne de commande la route qu'il veut aller chercher. exemple en ligne de commande python3 exo3-petit-client.py /home pour effectuer une requête GET pour la route /home qui fonctionnera.

Le serveur n'heberge pour l'instant que la route /home donc toute autre requête echouera en 404 NOT FOUND.

3) Vous pouvez observer que ça marche egalement sur le navigateur. J'ai inseré une exception d'erreur pouvant gerer les navigateurs car ils ne pourront pas envoyer en json comme un client interne.

4)Création de l'application terminé. l'adresse IP:Port simple vous dirigera vers la page d'accueil du serveur sur laquelle vous pouvez vous loguer sur l'application g40aChat avec le login "test" et le mot de passe "test"

5) j'ai pris du temps pour rajouter les fonctionnalités suivantes inspiré de nos cours de G50A en sécurité. Car en effet j'ai constaté des failles de type "PATH Traversal" qui me permet par exemple à un utilisateur non-authentifié d'acceder directement à la page de l'utilisateur via le chemin injecté dans le navigateur "/accounts/profile" ce qui permet d'outrepasser la connexion et l'authentification. J'ai donc rajouté des clés dans settings.py avec le LOGIN_URL et LOGIN_REDIRECT_URL qui permettent déjà de structurer les accès mais ensuite le plus important c'est de rajouter le decorateur @login_required avant les vues de pages authentifié ce qui empèche donc l'accès à ces pages sans authentification préalable.

Vous pouvez testez cela en essayant via un navigateur incognito ou une nouvelle session de path traverser en injectant une route avant connexion et vous serez redirigé vers la page de connexion automatiquement.


6) exercices de coding:
exos d'escaliers:
J'ai décidé de rajouté une autre couche de complexité dans cet exo en rajoutant une deuxième possibilité où on ne se limite pas à 2 marches max. J'extraits donc toutes les possibilités de séquences de marches possibles via un backtracking (algo de fonctions recursifs).

Voir fichier "coding.py"

pour le nombre de mots j'ai effectué à la fois un algo personnel et l'option toute simple en utilisant tout simplement split qui est déjà connu en python.


