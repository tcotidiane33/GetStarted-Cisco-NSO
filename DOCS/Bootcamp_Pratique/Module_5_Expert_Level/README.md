# Module 5 : Expert Level (Audit & check-sync)

Le summum de l'orchestration, c'est de s'assurer que ce que vous avez déployé hier est toujours en place aujourd'hui.

Dans le vrai monde, des administrateurs se connectent parfois directement sur les équipements en SSH pour faire une modification rapide et "oublient" de prévenir NSO. C'est ce qu'on appelle un **"Out of Band (OOB) change"**.

NSO possède une commande magique : `check-sync`.
Elle interroge le réseau et vous dit immédiatement si la configuration a dérivé.

## 🎯 Exercice Pratique : Simuler un check-sync et un Diff

Dans cet exercice, nous allons utiliser Python pour simuler ce comportement crucial.
Nous avons :
1. Ce que la Base de Données NSO croit être vrai (`cdb_etat.json`).
2. Ce qu'un script Python va lire (simulé) sur le routeur (`routeur_reel.json`).

### 🛠 Pré-requis
1. Python 3
2. Installer DeepDiff :
   ```bash
   pip3 install deepdiff
   ```

### 📝 Cas Pratique
Ouvrez le fichier `check_sync.py` et le fichier `routeur_reel.json`.

**Le Scénario :**
NSO a configuré hier l'interface `GigabitEthernet1` avec l'adresse IP `10.0.0.1` et l'interface `Vlan100` avec la description `PROD_VENTES`.
Cependant, pendant la nuit, un ingénieur a effacé l'IP sur `Gig1` pour faire un test.

**Étape 1 : Lancer l'audit (check-sync)**
```bash
python3 check_sync.py
```

**Résultat attendu :**
Le script doit vous alerter en rouge vif qu'il y a eu une modification "Out of Band" !
Il doit vous montrer exactement :
- Ce qui a été supprimé (L'IP de Gig1).
- Ce qui a été ajouté (L'admin a ajouté une description "TEST").

### 🧪 Le "Sync-from" ou "Sync-to"
C'est ici qu'un expert NSO brille. Face à cette divergence (Diff), il a deux choix en CLI :
- **`sync-from`** : NSO accepte la modification de l'admin et l'intègre dans sa base de données (Il a eu raison).
- **`sync-to`** : NSO écrase violemment la modification de l'admin en renvoyant la commande `ip address 10.0.0.1` sur le routeur (NSO a le dernier mot).
