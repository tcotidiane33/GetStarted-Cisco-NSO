# Module 2 : Le Device Manager (Python & Netmiko)

NSO excelle grâce à ses NEDs (Network Element Drivers) qui lui permettent de parler CLI à n'importe quel équipement comme si c'était une API.

## 🎯 Exercice Pratique : Simuler un NED basique avec Netmiko

Puisque nous n'avons pas de NED propriétaire sous la main, nous allons construire un mini "Device Manager" en Python. Netmiko est la librairie open-source la plus proche de ce que fait un CLI NED Cisco NSO sous le capot.

### 🛠 Pré-requis
1. Avoir Docker installé (pour simuler un vrai routeur Cisco IOS).
2. Installer Netmiko :
   ```bash
   pip3 install netmiko
   ```

### 📝 Cas Pratique
**Étape 1 : Démarrer un routeur de test (Optionnel si vous avez déjà un Lab GNS3/EVE-NG)**
Ici, nous simulons la présence d'un routeur via internet ou un conteneur local. Pour la simplicité de l'exercice open-source, nous utiliserons le bac à sable DevNet gratuit de Cisco (Always-On) :
* Host : `sandbox-iosxe-recomm-1.cisco.com`
* Port : `22`
* User : `developer`
* Pass : `C1sco12345`

**Étape 2 : Lancer le script "Mini-Device-Manager"**
Ouvrez le fichier `mini_ned.py` et observez comment on se connecte, comment on envoie une commande (équivalent du `sync-from` de NSO) et comment on pousse une configuration (équivalent du `commit`).

Exécutez le script :
```bash
python3 mini_ned.py
```

### 🧪 Ce que fait NSO en mieux :
Notre script Python pousse une commande de force. NSO, lui :
1. Calcule la différence (diff) entre ce que vous voulez et ce qui est déjà sur le routeur.
2. N'envoie *que* ce qui manque.
3. Si la ligne 2 échoue, NSO efface automatiquement la ligne 1 qu'il venait d'envoyer (Transaction).
