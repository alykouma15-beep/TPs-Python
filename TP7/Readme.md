1) TP7 Les APIs REST.
2) Pour utiliser le projet il faut se mettre dans le dossier TP7.
3) Pour activer l'environnement virtuel je fais source TP7/bin/activate.

4) Avec Postman on peut refaire une requête GET vers http://www.google.com et regarder les headers et le body. Pour OpenWeatherMap il faut créer un compte et récupérer une clé API. Pour tester la météo je lance python client_meteo.py.
5) Le programme demande la clé API puis le nom de la ville. Le programme affiche la température, la description du temps et l'humidité. Pour lancer le serveur Django je fais python manage.py runserver.
6) L'adresse de l'API est http://127.0.0.1:8000/. L'adresse de l'admin est http://127.0.0.1:8000/admin/. J'ai créé un compte admin local avec login admin et mot de passe admin.
7) Pour voir les messages je vais sur http://127.0.0.1:8000/api/messages/. Pour ajouter un message je fais une requête POST sur http://127.0.0.1:8000/api/messages/. Le json pour ajouter un message ressemble à {"expediteur":"aly","destinataire":"mohamed","message":"bonjour"}.
8) On peut donc réaliser tout type d'echange
9) Pour voir un seul message je vais sur http://127.0.0.1:8000/api/messages/1/. Pour modifier un message je fais une requête PUT sur http://127.0.0.1:8000/api/messages/1/.  Pour supprimer un message je fais une requête DELETE sur http://127.0.0.1:8000/api/messages/1/.
10) Pour voir les utilisateurs connectés je vais sur http://127.0.0.1:8000/utilisateurs/. Pour ajouter un utilisateur connecté je fais une requête POST sur http://127.0.0.1:8000/api/utilisateurs/. Les modèles Django sont Message et Utilisateur. Les serializers transforment les objets Django en JSON.
11) Les vues dans myapi/views.py gèrent les méthodes GET, POST, PUT et DELETE. Les urls de l'API sont dans myapi/urls.py.
12) La base de données utilisée est db.sqlite3. Pour refaire les migrations je fais python manage.py makemigrations puis python manage.py migrate. Pour lancer les tests je fais python manage.py test. Pour l'exercice des tableaux je lance python fusion_tableaux.py.
13) Exo de coding:

 Pour la fonction de trie. Je stocke chaque variable du tableau b dans une variable temporaire "temp" ensuite je supprime l'element du tableau b pour ne pas depasser la memoire et donc avoir à tout instant une occupation de mémoire exactement pareil et ensuite je rajoute le temp dans le tableau a proprement.
Ensuite après la boucle j'effectue trivialement une fonction de trie et on obtient le resultat.