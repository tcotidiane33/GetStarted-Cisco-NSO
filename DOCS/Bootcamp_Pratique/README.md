# 🚀 Bootcamp Cisco NSO : Projet Pratique Intégral (Open Source)

Ce dossier contient des exercices pratiques et complets pour chaque module de votre apprentissage Cisco NSO.
Puisque Cisco NSO est un produit propriétaire (nécessitant un compte Cisco pour le télécharger), les cas pratiques ici **simulent** son orchestration ou utilisent les outils open source intégrés/compatibles de son écosystème quand c'est possible.

## 🎯 L'Environnement de Laboratoire Open Source

Pour réaliser ce bootcamp sans équipement physique ni licence NSO complexe, nous utilisons une stack 100% open source/virtuelle :
1. **Containerlab** (Open Source) : Pour simuler le réseau physique (routeurs virtuels).
2. **YANG Suite / pyang** (Open Source) : Pour manipuler et comprendre les modèles YANG au cœur de NSO.
3. **Python (Netmiko/NAPALM/ncclient)** : Pour simuler les interactions du *Device Manager* et du *Service Manager* de NSO vers le réseau.
4. *(Optionnel)* **Cisco DevNet Sandbox (NSO Reservable)** : Si vous voulez le vrai NSO gratuitement pour valider vos scripts.

## 📁 Structure du Projet

* `Module_1_Fondations/` : Comprendre YANG (le langage de NSO) via `pyang`.
* `Module_2_Device_Manager/` : Simuler l'inventaire et la connexion (NETCONF/CLI) vers des nœuds Containerlab.
* `Module_3_Service_Manager/` : Le "FASTMAP" simulé : d'un fichier YAML intentionnel (« Je veux un VLAN ») vers l'application réseau.
* `Module_4_Python_Logic/` : Ajouter de la validation et des calculs (ex: allocation IP) en Python pur.
* `Module_5_Expert_Level/` : Audit de configuration (`check-sync` open source) et idempotence.

---
**Commencez par ouvrir le dossier `Module_1_Fondations/` et suivez le `README.md` à l'intérieur !**
