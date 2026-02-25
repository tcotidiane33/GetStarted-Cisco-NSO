from netmiko import ConnectHandler
import re

# Simulation des identifiants (DevNet Sandbox Cisco IOS XE)
cible = {
    'device_type': 'cisco_ios',
    'host':   'sandbox-iosxe-recomm-1.cisco.com',
    'username': 'developer',
    'password': 'C1sco12345',
    'port': 22,
    'global_delay_factor': 2, # Parfois la sandbox est lente
}

print(f"🌍 Connexion à l'équipement réseau (simulation du Device Manager NSO) vers {cible['host']}...")

try:
    with ConnectHandler(**cible) as net_connect:
        print("✅ Connecté avec succès !")
        
        # 1. Équivalent d'un 'sync-from' partiel dans NSO
        print("\n📥 Récupération de l'état actuel (show interfaces description)...")
        output = net_connect.send_command('show interfaces description')
        print(output)
        
        # 2. Équivalent d'un 'commit' (Envoyer une config)
        print("\n🚀 Poussée d'une nouvelle configuration d'interface Loopback...")
        config_commands = [
            'interface Loopback999',
            'description Configured by OpenSource NSO Mini-Simulator',
            'ip address 192.168.99.99 255.255.255.255'
        ]
        
        # Netmiko entre automatiqement en mode config (conf t)
        result = net_connect.send_config_set(config_commands)
        print("📝 Résultat de la configuration :")
        print(result)
        
        # 3. Vérification post-commit
        verify = net_connect.send_command('show ip interface brief | include Loopback999')
        print(f"\n🔍 Vérification finale sur le routeur : {verify}")

except Exception as e:
    print(f"❌ Erreur de connexion au routeur : {e}")
    print("💡 Astuce: Si la sandbox cisco est injoignable (timeout), modifiez le dictionnaire 'cible' pour pointer vers un routeur GNS3/EVE-NG local.")
