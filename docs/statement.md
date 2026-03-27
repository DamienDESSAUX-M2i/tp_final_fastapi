# TP – Développer une API sécurisée de gestion de scores de babyfoot avec FastAPI

## Contexte

Vous devez développer une API REST sécurisée permettant de gérer des scores de babyfoot.

L’application devra permettre à des utilisateurs de s’inscrire et de se connecter afin d’obtenir un **JSON Web Token (JWT)**. Une fois authentifiés, ils pourront utiliser les endpoints métier pour gérer :

- des joueurs,
- des équipes,
- des matchs,
- et éventuellement un classement simple.

L’objectif de ce TP est de mettre en pratique :

- la création d’une API avec **FastAPI**,
- le découpage d’une application en plusieurs fichiers,
- la validation des données avec **Pydantic**,
- la sécurisation des endpoints avec **JWT**,
- et la gestion d’un peu de logique métier.

---

## Objectifs pédagogiques

À l’issue du TP, vous devez être capables de :

- créer une API FastAPI structurée en plusieurs fichiers,
- mettre en place une authentification par JWT,
- protéger des endpoints avec des dépendances FastAPI,
- manipuler des entités liées entre elles,
- appliquer des règles métier simples,
- exposer des endpoints cohérents et documentés.

---

## Travail demandé

Vous devez développer une API permettant :

1. à un utilisateur de **s’inscrire** ;
2. à un utilisateur de **se connecter** ;
3. de gérer des **joueurs** ;
4. de gérer des **équipes de deux joueurs** ;
5. d’enregistrer des **matchs** ;
6. de consulter les **matchs enregistrés** ;
7. en bonus, de calculer des **classements**.

---

## Contraintes générales

### Contraintes techniques

Vous devez utiliser :

- **Python**
- **FastAPI**
- **Pydantic**
- une authentification par **JWT**
- un projet **découpé en plusieurs fichiers**

Vous pouvez utiliser :

- soit une persistance **en mémoire**,
- soit une base **SQLite** ou autre SGBD avec **SQLAlchemy**


### Contraintes de structure

Votre projet doit être organisé proprement.  
Vous êtes libres sur le découpage exact, mais vous devez au minimum séparer :

- le point d’entrée de l’application,
- les routes,
- les modèles/schémas,
- la logique de sécurité.


---

## Fonctionnalités attendues

# 1. Authentification

## 1.1 Inscription

L’API doit permettre à un utilisateur de créer un compte.

### Données minimales attendues

* username
* password


### Règles minimales

* le username doit être unique ;
* le mot de passe ne doit **jamais** être stocké en clair ;
* le mot de passe doit être **hashé** avant enregistrement.

### Endpoint attendu

Exemple :

* `POST /auth/register`

### Réponse attendue

Une réponse propre contenant les informations publiques de l’utilisateur créé.

Le mot de passe ne doit jamais être renvoyé.

---

## 1.2 Connexion

L’API doit permettre à un utilisateur de se connecter avec son identifiant et son mot de passe.

### Endpoint attendu

Exemple :

* `POST /auth/login`

### Réponse attendue

La réponse doit contenir au minimum :

* un `access_token`
* un `token_type`

Exemple :

```json
{
  "access_token": "xxxxx",
  "token_type": "bearer"
}
```

---

## 1.3 Endpoint protégé de test

Vous devez prévoir au moins un endpoint protégé permettant de vérifier que l’authentification fonctionne.

### Endpoint attendu

Exemple :

* `GET /auth/me`
* ou `GET /private/me`

### Comportement attendu

* sans token valide : accès refusé ;
* avec token valide : l’utilisateur connecté est renvoyé.

---

# 2. Gestion des joueurs

L’API doit permettre de gérer des joueurs de babyfoot.

## Données minimales d’un joueur

* id
* nickname

Vous pouvez ajouter d’autres champs si vous le souhaitez, par exemple :

* first_name
* last_name

## Fonctionnalités attendues

### Créer un joueur

Exemple :

* `POST /players`

### Lister les joueurs

Exemple :

* `GET /players`

### Consulter un joueur par son identifiant

Exemple :

* `GET /players/{player_id}`

### Facultatif

* modifier un joueur ;
* supprimer un joueur.

---

# 3. Gestion des équipes

L’API doit permettre de créer des équipes composées de **deux joueurs exactement**.

## Données minimales d’une équipe

* id
* name
* player_1_id
* player_2_id

Ou toute autre structure équivalente.

## Règles métier obligatoires

* une équipe doit contenir **exactement 2 joueurs** ;
* les deux joueurs doivent être **différents** ;
* les deux joueurs doivent exister ;
* une équipe ne peut pas contenir deux fois le même joueur.

## Fonctionnalités attendues

### Créer une équipe

Exemple :

* `POST /teams`

### Lister les équipes

Exemple :

* `GET /teams`

### Consulter une équipe

Exemple :

* `GET /teams/{team_id}`

### Facultatif

* modifier une équipe ;
* supprimer une équipe.

---

# 4. Gestion des matchs

L’API doit permettre d’enregistrer des matchs de babyfoot.

Deux types de matchs sont autorisés :

* **joueur contre joueur**
* **équipe contre équipe**

Le mode **équipe contre joueur** n’est pas autorisé.

## Données minimales d’un match

* id
* match_type
* participant_1_id
* participant_2_id
* score_1
* score_2

### Valeurs possibles pour `match_type`

* `single`
* `team`

## Règles métier obligatoires

### Règles générales

* un match doit avoir un type ;
* un match doit avoir deux participants ;
* un score doit être renseigné pour chaque participant ;
* un participant ne peut pas jouer contre lui-même ;
* les scores doivent être des entiers positifs ou nuls.

### Si `match_type = single`

* `participant_1_id` et `participant_2_id` représentent des joueurs ;
* les deux joueurs doivent exister ;
* les deux joueurs doivent être différents.

### Si `match_type = team`

* `participant_1_id` et `participant_2_id` représentent des équipes ;
* les deux équipes doivent exister ;
* les deux équipes doivent être différentes.

## Fonctionnalités attendues

### Créer un match

Exemple :

* `POST /matches`

### Lister les matchs

Exemple :

* `GET /matches`

### Consulter un match par identifiant

Exemple :

* `GET /matches/{match_id}`

### Facultatif

* supprimer un match.

---

# 5. Sécurisation des endpoints

Tous les endpoints métier doivent être protégés.

Cela signifie que les endpoints suivants doivent nécessiter un token valide :

* `/players`
* `/teams`
* `/matches`
* et tout endpoint équivalent

Seuls les endpoints liés à l’authentification peuvent rester publics, par exemple :

* `POST /auth/register`
* `POST /auth/login`

Vous pouvez également prévoir un endpoint public simple de test, par exemple :

* `GET /public/ping`

---

## Exemple de répartition

### Endpoints publics

* `POST /auth/register`
* `POST /auth/login`
* `GET /public/ping`

### Endpoints protégés

* `GET /private/me`
* `POST /players`
* `GET /players`
* `POST /teams`
* `GET /teams`
* `POST /matches`
* `GET /matches`

---

# 6. Bonus : classements

Si vous terminez la partie principale, vous pouvez ajouter un système de classement simple.

## 6.1 Classement des joueurs

Exemple d’endpoint :

* `GET /rankings/players`

Vous pouvez calculer, par exemple :

* nombre de matchs joués,
* nombre de victoires,
* nombre de défaites,
* différence de buts.

## 6.2 Classement des équipes

Exemple d’endpoint :

* `GET /rankings/teams`

Même principe :

* matchs joués,
* victoires,
* défaites,
* différence de buts.

## Remarque

Un classement simple est suffisant.
Il n’est pas demandé de mettre en place un système complexe de type Elo ou championnat complet.

---

## Règles de validation attendues

Votre API devra refuser les cas incohérents, par exemple :

* création d’un utilisateur avec un username déjà utilisé ;
* création d’une équipe avec le même joueur deux fois ;
* création d’une équipe avec un joueur inexistant ;
* création d’un match `single` avec deux fois le même joueur ;
* création d’un match `team` avec deux fois la même équipe ;
* création d’un match avec un type invalide ;
* création d’un match avec des scores négatifs.

---

## Exemples de scénarios à tester

Vous devez être capables de démontrer au minimum les scénarios suivants :

### Scénario 1 – Authentification

1. créer un utilisateur ;
2. se connecter ;
3. récupérer un token ;
4. appeler un endpoint protégé avec ce token.

### Scénario 2 – Joueurs

1. créer deux joueurs ;
2. lister les joueurs ;
3. consulter un joueur.

### Scénario 3 – Équipes

1. créer deux joueurs ;
2. créer une équipe avec ces deux joueurs ;
3. vérifier que la création échoue si le même joueur est utilisé deux fois.

### Scénario 4 – Match joueur contre joueur

1. créer deux joueurs ;
2. créer un match `single` entre eux ;
3. vérifier que le match apparaît dans la liste.

### Scénario 5 – Match équipe contre équipe

1. créer quatre joueurs ;
2. créer deux équipes ;
3. créer un match `team` ;
4. vérifier que le match apparaît dans la liste.

---

## Travail minimum attendu

Pour que le TP soit considéré comme terminé, il faut au minimum :

* une inscription utilisateur ;
* une connexion utilisateur ;
* un JWT fonctionnel ;
* un endpoint protégé ;
* un CRUD minimal sur les joueurs ;
* la création d’équipes de 2 joueurs ;
* la création de matchs `single` et `team` ;
* la liste des matchs ;
* un projet découpé en plusieurs fichiers.

---

## Bonus possibles

Si vous allez plus vite, vous pouvez ajouter :

* suppression d’un joueur ;
* suppression d’une équipe ;
* suppression d’un match ;
* rôles utilisateurs ;
* endpoints réservés à un administrateur ;
* refresh token ;
* classement joueurs ;
* classement équipes ;
* documentation enrichie ;
* jeux de données d’exemple.

---

## Livrables attendus

Vous devez rendre :

1. le code source complet du projet ;
2. un fichier `requirements.txt` ;
3. un fichier `README.md` expliquant :

   * comment installer les dépendances ;
   * comment lancer le projet ;
   * comment tester les endpoints ;
4. éventuellement une collection Postman ou des exemples de requêtes.

---

## Conseils

* commencez par l’authentification ;
* vérifiez d’abord que le JWT fonctionne ;
* créez ensuite les joueurs ;
* puis les équipes ;
* puis les matchs ;
* ajoutez les validations métier progressivement ;
* ne cherchez pas à tout faire d’un coup.


---

## Résultat attendu

À la fin du TP, vous devez disposer d’une API sécurisée permettant :

* à un utilisateur de s’inscrire et se connecter ;
* de créer et consulter des joueurs ;
* de créer et consulter des équipes de 2 joueurs ;
* d’enregistrer des matchs de babyfoot ;
* de consulter ces matchs ;
* et éventuellement d’obtenir des classements simples.


 