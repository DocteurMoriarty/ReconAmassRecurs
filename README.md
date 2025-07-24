# ReconAmassRecurs.py — Découverte récursive de sous-domaines avec Amass

Ce script Python effectue une découverte récursive de sous-domaines en combinant l’outil [Amass](https://github.com/owasp-amass) (mode passif), la résolution DNS classique (`host`) et le reverse DNS (PTR), avec gestion d’une **whitelist** pour exclure certains domaines.

---

## Fonctionnalités principales

- Découverte récursive de sous-domaines via **Amass en mode passif**.
- Résolution DNS (avec `host`) pour récupérer les adresses IP des sous-domaines.
- Recherche inverse (reverse DNS) sur chaque IP, ajout automatique au scope si domaine non whitelisté.
- Gestion d’une **whitelist** pour exclure des domaines et leurs sous-domaines.
- Contrôle de la profondeur de récursion (par défaut 2).
- Affichage console clair avec résumé final des domaines et IPs découverts.

---

## Pré-requis et installation

- Python 3.7+
- Amass installé et accessible dans le PATH
- Outil système `host` disponible

### Installation d’Amass (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install amass
```

### Installation de l’outil `host` (Debian/Ubuntu)

```bash
sudo apt install bind9-host
```

---

## Mise en place de l’environnement Python

Il est recommandé d’utiliser un environnement virtuel Python pour isoler les dépendances :

```bash
python3 -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate
```

Le script a été testé avec **pylint** et obtient une note **10/10** pour la qualité du code.

Pour installer pylint et vérifier toi-même la qualité du script, utilise :

```bash
pip install pylint
```

---

## Utilisation

Lance le script et entre le domaine de départ quand demandé :

```bash
python ReconAmassRecurs.py
```

Exemple :

```
Nom de domaine de départ : exemple.com
```

Le script affichera la découverte récursive des sous-domaines, leurs IPs, les PTR trouvés et un résumé final.

---

## Notes

- Le script évite les domaines présents dans la whitelist définie dans le code (`WHITELIST`).
- Le timeout de la commande Amass est fixé à 120 secondes par domaine.
- Le script utilise les commandes système `amass` et `host`, qui doivent être présentes sur la machine.

---

## Licence

MIT License - libre d’utilisation et modification.

---

DocteurMoriarty
