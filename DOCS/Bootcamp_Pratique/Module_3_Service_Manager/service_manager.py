import yaml
from jinja2 import Template

# 1. Lire l'intention de l'utilisateur (La donnée YANG "instanciée" en JSON/YAML dans NSO)
print("📥 1. Lecture de l'intention métier depuis intention-utilisateur.yaml...")
with open("intention-utilisateur.yaml", "r") as f:
    service_data = yaml.safe_load(f)

# 2. Lire le Template XML/Texte (Le squelette de configuration)
print("🏗  2. Chargement du Template d'équipement vlan-template.j2...")
with open("vlan-template.j2", "r") as f:
    template_content = f.read()

jinja_template = Template(template_content)

# 3. La VM FASTMAP de NSO (Fusion Donnée + Template)
print("🚀 3. Génération de la configuration (simili 'commit dry-run output native')...")
print("-" * 50)

# Pour chaque VLAN défini par l'utilisateur...
for vlan in service_data['vlans']:
    # Et pour chaque équipement cible de ce VLAN...
    for device in vlan['devices']:
        # On injecte les variables dans le template
        rendered_config = jinja_template.render(
            vlan_id=vlan['id'],
            vlan_name=vlan['name'],
            device_name=device
        )
        print(rendered_config.strip() + "\n")

print("-" * 50)
print("✨ Dans la réalité, NSO prendrait ce texte et utiliserait le NED (Module 2) pour l'envoyer au routeur.")
