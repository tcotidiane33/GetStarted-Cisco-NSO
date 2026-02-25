# 🚀 Bootcamp Cisco NSO : De Zéro à Expert (Guide Pédagogique)

Ce guide est conçu pour vous prendre par la main et vous emmener d'une compréhension débutante jusqu'au niveau d'expert sur **Cisco Network Services Orchestrator (NSO)**. L'approche ici est *pédagogique* : nous allons d'abord comprendre le **pourquoi**, ensuite le **comment**, et enfin les **concepts avancés**.

---

## 1. Introduction & Philosophie (Le "Pourquoi ?")

### Le problème
Historiquement, gérer un réseau signifiait se connecter en SSH sur chaque équipement (Cisco, Juniper, Arista, firewall, load balancer) et taper des commandes CLI.
- C'est **lent** et sujet aux **erreurs humaines**.
- Difficile de savoir ce qui est *réellement* configuré sur le réseau (dérive de configuration).
- Si on doit configurer 5 équipements pour un seul "Service" (ex: un VPN L3), et que le 4ème échoue, comment fait-on un **rollback** propre des 3 premiers ?

### La solution : Cisco NSO
NSO est une plateforme d'orchestration qui agit comme un **pont** entre l'intention métier ("Je veux un VPN entre le Site A et B") et la réalité du réseau (les lignes de commandes CLI ou requêtes API sur les équipements).

**Les super-pouvoirs de NSO :**
1. **Multivendeurs** : Il parle à n'importe quel équipement grâce à des drivers (NEDs).
2. **Transactions ACID** : Comme une base de données. Si vous déployez un service sur 5 routeurs, soit tout passe, soit rien ne passe (rollback automatique).
3. **Configuration Déclarative** : Vous dites "Je veux que le port 1 soit dans le VLAN 10". NSO calcule lui-même ce qu'il faut envoyer au switch pour atteindre cet état, qu'il soit Cisco ou Juniper.

---

## 2. L'Architecture sous le capot (Les 4 Piliers)

Pour devenir expert, il faut visualiser comment NSO est construit :

1. **CDB (Configuration Database)** :
   Une base de données hiérarchique en mémoire (très rapide). Elle contient 100% de la configuration souhaitée du réseau. C'est la **Source de Vérité**.
2. **Device Manager** :
   Le module qui gère la connexion aux équipements réseau. Il gère les clés SSH, le pooling de connexion, et la comparaison entre la CDB et l'équipement réel.
3. **NEDs (Network Element Drivers)** :
   Ce sont les "traducteurs".
   - *CLI NEDs* : Traduisent le modèle NSO en commandes CLI classiques. NSO est le seul outil au monde à pouvoir faire du vrai transactionnel sur de vieux équipements CLI.
   - *NETCONF NEDs* : Pour les équipements modernes qui parlent XML/JSON natif.
4. **Service Manager** :
   Le module où vous vivrez en tant que développeur NSO. Il prend les entrées de l'utilisateur (le "Service") et les transforme en configurations ("Device").

---

## 3. L'Interface et la Prise en Main

NSO propose plusieurs interfaces, mais la plus importante pour comprendre l'outil est la **CLI NSO**.
Elle ressemble beaucoup au style *Juniper* (J-style) ou *XR* (C-style).

### Les commandes vitales à connaître par cœur :
- `show configuration` : Voir la configuration dans la CDB.
- `devices device <nom> sync-from` : Demande à NSO de lire la conf de l'équipement réel et de mettre à jour sa propre CDB. (Alignement NSO -> Réseau).
- `devices device <nom> sync-to` : Force l'équipement réel à correspondre à la CDB (Alignement Réseau -> NSO). Idéal si quelqu'un a fait une modif CLI manuelle dans le dos de NSO (Out-of-band change).
- `commit dry-run outformat native` : L'arme secrète. Avant d'appliquer un service, NSO vous montre *exactement* quelles lignes de commandes CLI il va envoyer aux équipements.
- `commit` : Applique la transaction.

---

## 4. Créer un Service : Le Coeur du Métier (La méthode en 3 étapes)

Le travail quotidien d'un développeur NSO est de créer des **Services**. Un service NSO repose sur le concept du **FASTMAP**. NSO est magique : vous lui dites comment *créer* le service, et il déduit automatiquement comment le *modifier* ou le *supprimer* !

### Étape 1 : Le Modèle de données (YANG)
YANG est le langage de modélisation de NSO. Il définit les champs de votre service.
*Exemple pédagogique : "Pour mon service VLAN, j'ai besoin d'un nom de VLAN, d'un ID de VLAN, et d'une liste de routeurs cibles."*

```yang
module mon-vlan {
  list vlan-service {
    key name;
    leaf name { type string; }
    leaf vlan-id { type uint16; }
    leaf-list device { type leafref { path "/ncs:devices/ncs:device/ncs:name"; } }
  }
}
```

### Étape 2 : Le Template (XML)
Le template XML est le squelette de configuration. Il mappe les variables de votre modèle YANG vers la configuration de l'équipement.
*Exemple : Remplacer le VLAN ID fixe par la variable `$VLAN_ID` définie dans le YANG.*

### Étape 3 : La Logique (Python / Java) - *Optionnel*
Si votre service est complexe (ex: aller chercher une IP dans un IPAM externe tiers, faire des calculs de sous-réseaux, vérifier la santé d'un lien avant de l'allumer), vous utilisez du code Python. Ce code intercepte la création du service (FASTMAP callback) et prépare les variables pour le Template XML.

---

## 5. Les Concepts Avancés (Le parcours de l'Expert 🌟)

Pour vous démarquer et être un vrai expert, voici ce qu'il faut maîtriser :

### A. Reactive FASTMAP (RFM)
Parfois, un service prend du temps à s'installer (ex: allumer une VM, attendre un reboot). RFM est un patron de conception (design pattern) où le service s'exécute en plusieurs phases. On écrit des "plans" (PlanData) qui disent où en est le service (Init, Deploying, Ready). Le service se réveille tout seul ("re-deploy") dès qu'une condition externe est remplie.

### B. Nano Services
L'évolution de RFM. Au lieu d'écrire beaucoup de code Python pour gérer les états multiples, Nano Services utilise du pur YANG pour définir une machine à états (State Machine). Extrêmement puissant pour l'orchestration de bout en bout.

### C. Actions et Kickers
- **Action** : Un script Python exécutable à la demande via un bouton sur l'UI ou l'API (ex: `ping`, `traceroute`, `clear counters`). Ce n'est pas de la configuration pure.
- **Kicker** : Un déclencheur ("trigger"). "Si la valeur `X` dans la base de données change, lance le script Python `Y`". Très utile pour l'auto-réparation.

### D. Layered Service Architecture (LSA)
Si vous gérez 100 000 routeurs, un seul nœud NSO va s'effondrer. LSA permet d'avoir des "CFS" (Customer Facing Services - NSO du haut) qui distribuent le travail à de multiples "RFS" (Resource Facing Services - NSO du bas). C'est le Graal de la scalabilité.

---

## 6. Roadmap Pratique à suivre (Plan d'action de l'étudiant)

Pour acquérir de l'expertise, ne lisez pas seulement, **pratiquez** dans cet ordre strict :

1. **Semaine 1 (Fondations et CLI)**
   - Installez une version locale de NSO (System Install vs Local Install : préférez Local Install pour les développeurs).
   - Lancez les routeurs simulés inclus avec NSO (`ncs-netsim`).
   - Pratiquez l'ajout de devices à NSO, faites manuellement des `sync-from`, changez une valeur sur l'équipement lui-même, et voyez NSO détecter la désynchronisation avec `check-sync`.

2. **Semaine 2 (L'art du pur YANG et Template)**
   - Utilisez le générateur de NSO pour créer un package de base : `ncs-make-package --service-skeleton template mon_premier_service`.
   - Modifiez le fichier YANG et le fichier XML. Ciblez des routeurs virtuels (netsim) et appliquez.
   - Supprimez le service depuis la CLI NSO et validez le miracle du FASTMAP (la configuration est supprimée proprement sur l'équipement).

3. **Semaine 3 (Injection de Python)**
   - Recréez un package mais avec Python : `ncs-make-package --service-skeleton python-and-template mon_service_python`.
   - Ouvrez le script Python (le bloc `cb_create`) et manipulez les variables contextuelles avant de les appliquer au template d'équipement.
   - Tentez d'importer la librairie `requests` pour faire un appel banal vers une API publique simulée (simuler un requêtage IPAM).

4. **Semaine 4 (S'attaquer aux Monstres)**
   - Créez des règles de validation (Validation Callbacks) en Python pour empêcher un utilisateur d'entrer un VLAN ID erroné.
   - Codez une Action Python (ex: récupérer la table ARP d'un device et la traiter).
   - *Optionnel mais recommandé pour les pros* : Étudiez et testez un Nano Service simple fourni dans la documentation Cisco (`$NCS_DIR/examples.ncs/`).

---

**Le mot de la fin pour votre parcours :**
L'apprentissage de NSO est une courbe logarithmique. Le début est un peu raide (comprendre YANG, comprendre le transactionnel, comprendre la compilation des packages), mais une fois le "déclic" du FASTMAP passé, vous verrez l'automatisation réseau sous un jour entièrement nouveau. Bon courage futur expert !
