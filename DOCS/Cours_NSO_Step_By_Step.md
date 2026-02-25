# Bootcamp Cisco NSO : Le Guide Pratique (Step-by-Step)

Ce guide est un apprentissage séquentiel. Ne sautez pas d'étapes. Chaque module s'appuie sur le précédent pour vous emmener d'une simple installation à une orchestration complexe.

---

## 🎯 Module 1 : Les Fondations & L'Installation (Le "Hello World" de NSO)

**Objectif :** Obtenir un NSO fonctionnel et comprendre comment il interagit avec le monde extérieur.

### Étape 1 : Comprendre System vs Local Install
NSO peut s'installer de deux façons :
- **System Install** (`/opt/ncs`): Pour la production. Utilise des daemons système.
- **Local Install** (dans votre répertoire `~/nso-instance`): Pour les développeurs. C'est ce que nous allons utiliser. Vous pouvez avoir autant d'instances locales que vous voulez.

### Étape 2 : Créer votre première instance
1. Vous avez besoin du binaire d'installation NSO (ex: `nso-5.7.linux.x86_64.installer.bin`).
2. Installez le logiciel de base : `sh nso-5.7.linux.x86_64.installer.bin ~/nso-install`
3. Sourcez l'environnement : `source ~/nso-install/ncsrc`
4. Créez votre projet de travail (l'instance locale) : `ncs-setup --dest ~/mon-premier-nso`
5. Allez dans ce dossier : `cd ~/mon-premier-nso`
6. Démarrez NSO : `ncs`

### Étape 3 : Vérifier que NSO tourne
- Tapez `ncs_cli -C -u admin` (Le `-C` force le mode Cisco-like. Le `-u admin` vous log en administrateur).
- Vous êtes maintenant dans le "cerveau" de NSO. Tapez `show ncs-state version`. Si ça répond, bravo !

---

## 🎯 Module 2 : Le Device Manager (Parler avec les équipements réseau)

**Objectif :** NSO est inutile sans équipements. Nous allons simuler des routeurs et les brancher à NSO.

### Étape 1 : Lancer des routeurs virtuels (netsim)
Cisco fournit `ncs-netsim` pour créer de faux routeurs qui parlent CLI ou NETCONF, idéal pour tester sans casser un vrai réseau.
1. Depuis votre terminal Linux (pas la CLI NSO) :
   `ncs-netsim create-network cisco-ios-cli-3.8 3 mon_lab_ios`
   *(Ceci crée 3 faux routeurs IOS appelés ex0, ex1, ex2).*
2. Lancez les routeurs : `ncs-netsim start`

### Étape 2 : Déclarer les équipements dans NSO
Il faut dire à NSO que ces équipements existent et comment s'y connecter (IP, Port, Driver NED, Credentials).
1. Heureusement, `ncs-netsim` a généré un fichier XML avec toute la configuration.
2. Injectez-le dans NSO : `ncs-netsim ncs-xml-init > lab-devices.xml`
3. Chargez-le depuis la CLI Linux : `ncs_load -l -m lab-devices.xml`

### Étape 3 : Le Rituel d'Alignement (Sync-From)
NSO sait maintenant comment contacter les équipements, mais sa base de données (CDB) est vide.
1. Allez dans la CLI NSO : `ncs_cli -C -u admin`
2. Testez la connexion : `devices device * ping`
3. Récupérez la configuration du réseau : **`devices sync-from`**
   *(C'est l'opération la plus importante dans l'exploitation de NSO. NSO télécharge la config de tous les routeurs et peuple sa CDB).*
4. Tapez `show running-config devices device ex0 config`. Vous voyez la configuration du faux routeur IOS !

---

## 🎯 Module 3 : Le Service Manager & FASTMAP (Créer son premier Service Modélisé)

**Objectif :** Fini le CLI manuel. Nous allons créer un Service abstrait (un "VLAN") qui configurera de multiples routeurs automatiquement.

### Étape 1 : Générer le squelette du Service (Template pur)
Nous voulons créer un service où l'utilisateur ne rentre que ça :
- Nom du VPN
- L'ID du VLAN (ex: 100)
- Une liste de routeurs où le déployer

Sortez de NSO et allez dans le dossier `packages` de votre instance locale (`~/mon-premier-nso/packages`).
1. Tapez : `ncs-make-package --service-skeleton template vlan_service`
2. Cela crée un dossier `vlan_service` avec deux dossiers critiques : `src` (pour le modèle YANG) et `templates` (pour le XML).

### Étape 2 : Le Modèle YANG (`src/yang/vlan_service.yang`)
Ouvrez ce fichier. Supprimez les trucs compliqués générés par défaut et mettez ça :
```yang
module vlan_service {
  namespace "http://com/example/vlan_service";
  prefix vlan_service;
  import tailf-common { prefix tailf; }
  import tailf-ncs { prefix ncs; }

  list vlan {
    key name;
    leaf name { type string; }
    leaf vlan-id { type uint32; }
    // Liste des routeurs sur lesquels appliquer ce VLAN
    leaf-list router {
      type leafref {
        path "/ncs:devices/ncs:device/ncs:name";
      }
    }
  }
}
```
*Le `leafref` est magique : il crée une liste déroulante dynamique dans l'interface NSO qui ne propose que les routeurs existants.*

### Étape 3 : Le Template XML (`templates/vlan_service-template.xml`)
C'est ici qu'on fait correspondre notre YANG à la vraie CLI des routeurs IOS.
```xml
<config-template xmlns="http://tail-f.com/ns/config/1.0">
  <devices xmlns="http://tail-f.com/ns/ncs">
    <!-- Pour chaque routeur selectionné dans notre service... -->
    <device>
      <name>{/router}</name>
      <config>
        <!-- ... on applique des commandes IOS CLI -->
        <interface xmlns="urn:ios">
          <!-- Créer l'interface Vlan -->
          <Vlan>
            <name>{/vlan-id}</name>
            <!-- Allumer l'interface -->
            <no>
               <shutdown/>
            </no>
          </Vlan>
        </interface>
      </config>
    </device>
  </devices>
</config-template>
```

### Étape 4 : Compiler et Charger
- Dans `vlan_service/src`, tapez `make`.
- Allez dans la NSO CLI : `packages reload`. NSO découvre votre nouveau service.

### Étape 5 : La Magie (Test du service)
Dans la NSO CLI :
1. `config`
2. `vlan SALES vlan-id 100 router [ ex0 ex1 ]`
3. Définitivement la commande la plus importante : **`commit dry-run outformat native`**
   *(NSO vous montre les commandes CLI IOS exactes qu'il va pousser sur ex0 et ex1 pour créer ce VLAN. C'est l'instant "Waouh").*
4. `commit`. La configuration est poussée.

Pour tester le FASTMAP :
1. `no vlan SALES`
2. `commit dry-run outformat native`
*(NSO a deviné tout seul qu'il devait envoyer `no interface Vlan 100` aux routeurs ! Vous n'avez jamais codé comment supprimer le service, le FASTMAP l'a déduit).*

---

## 🎯 Module 4 : Puissance et Logique (Ajouter du Python)

**Objectif :** Un template XML c'est bien, mais on ne peut pas faire de conditions complexes (if/else), de boucles dynamiques, ou d'appels à des bases de données externes externes (IPAM, ServiceNow). C'est là que le Python entre en jeu.

### Étape 1 : Créer un package Python/Template
1. Dans `packages/` : `ncs-make-package --service-skeleton python-and-template python_vlan`
2. Modifiez le YANG (`python_vlan.yang`) pour ajouter des champs si besoin. On garde la structure similaire.

### Étape 2 : Le hook Python (cb_create)
Ouvrez le fichier généré dans `python/python_vlan/main.py`.
Repérez la fonction `cb_create`. C'est le code qui s'exécute quand un utilisateur tape "commit".
```python
@Service.create
def cb_create(self, tctx, root, service, proplist):
    self.log.info('Service create(service=', service._path, ')')

    # Logique métier en Python !
    # Exemple : Empêcher de configurer le VLAN 1, car c'est interdit
    if service.vlan_id == 1:
        raise Exception("Interdiction d'utiliser le VLAN 1 !")

    # On peut créer des variables de contexte pour notre template XML
    vars = ncs.template.Variables()
    vars.add('DESCRIPTION', f"VLAN généré par NSO le {datetime.now()}")

    # Appliquer le template XML 
    template = ncs.template.Template(service)
    template.apply('python_vlan-template', vars)
```

Maintenant, votre template XML (`python_vlan-template.xml`) peut récupérer la variable `$DESCRIPTION` calculée dynamiquement par le script Python pour remplir le `description` d'une interface sur le switch !

### Étape 3 : Gagner du temps (Les Actions)
Faire de la config ce n'est pas tout. Parfois, il faut lire l'état du réseau ou exécuter une commande non-configuration.
Dans YANG, au lieu d'une `list`, créez une "action" (un bouton "Play") :
```yang
rpc ping-all-devices {
    tailf:actionpoint ping-action;
    output {
        leaf result { type string; }
    }
}
```
Puis dans Python vous liez cette action à une fonction qui va lancer un `devices device * ping` et vous formater le résultat de manière lisible.

---

## 🎯 Module 5 : Expert Level (Résilience et Audit)

**Objectif :** Comprendre les mécanismes fondamentaux pour les réseaux à très haute échelle (Service Provider ou Data Center).

### Les mécanismes essentiels d'audit à comprendre
- **check-sync** :
  Si vous tapez `devices check-sync`, NSO calcule le hash (signature) de la configuration des routeurs réels et le compare avec sa CDB en mémoire sans télécharger toute la config. Si quelqu'un s'est connecté en console sur le routeur pour désactiver un port (Out of Band change), NSO détectera que le hash est "out-of-sync".
- **compare-config** :
  Permet de voir exactement les champs, ligne par ligne, qui ont été modifés manuellement et divergent de la CDB.
- **Rollback de transactions** :
  Si vous modifiez un routeur, que cela foire le réseau et que le NOC vous hurle dessus, dans la CLI NSO tapez :
  `show rollbacks` (trouvez le numéro de la transaction `ID`)
  `rollback configuration <ID>`
  NSO remettra le système *exactement* dans l'état de l'instant T.

### Où aller plus loin (Lectures supplémentaires de niveau Architecte) 
Pour continuer l'apprentissage "Expert", il vous faudra fouiller la documentation Cisco NSO officielle sur :
1. **HA (High Availability)** : Comment monter un NSO "Primary" et "Secondary" qui répliquent la CDB en temps réel (via le namespace `tailf-hcc` dans YANG).
2. **Kickers** : Exécuter un script Python non pas par une action, avec un abonnement de mise à jour. (Ex: "Si quelqu'un change un mot de passe dans un tenant, envoie un log par API sur un webhook").
3. **Layered Services Architecture (LSA)** : Un nœud NSO au-dessus (CFS - Customer Facing Service) qui dispatch la configuration abstraite vers 5 nœuds NSO d'exécution en bas (RFS - Resource Facing Service).
4. **Reactive FASTMAP** et **Nano Services** : Orchestrer des services qui "prennent du temps", comme réagir en plusieurs étapes (Deployer le firewall ➡️ Attendre 5 minutes le temps qu'il boot ➡️ Allumer le BGP).

---
*Fin du Guide. Practice makes perfect : n'hésitez pas à relancer un ncs-netsim de 10 routeurs et à casser la configuration exprès en direct pour voir NSO la corriger automatiquement.*
