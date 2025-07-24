"""
ReconAmassRecurs.py - Script de découverte de sous-domaines récursive
utilisant amass, host, et reverse DNS, avec gestion de whitelist.
"""


import subprocess

seen_domains = set()
seen_ips = set()

WHITELIST = {
    "exemple.com",
}


def is_whitelisted(domain):
    """Check if a domain is whitelisted (including subdomains)."""
    return any(domain == w or domain.endswith(f".{w}") for w in WHITELIST)


def run_amass(domain):
    """
    Run the Amass tool in passive mode on the given domain.
    Returns a set of discovered subdomains.
    """
    if is_whitelisted(domain):
        print(f"[!] Domaine épargné par la whitelist : {domain}")
        return set()
    try:
        print(f"[+] Amass pour {domain}")
        result = subprocess.run(["amass", "enum", "-passive", "-d", domain],
            capture_output=True,
            text=True,
            timeout=120,
	    check=False
        )
        return set(line.strip() for line in result.stdout.splitlines() if line.strip())
    except subprocess.TimeoutExpired:
        print(f"[-] Timeout amass sur {domain}")
        return set()


def resolve_ip(domain):
    """
    Resolve a domain to a list of IP addresses using the 'host' command.
    """
    result = subprocess.run(
	["host", domain],
	capture_output=True,
	text=True,
	timeout=5,
	check=False
	)
    ips = []
    for line in result.stdout.splitlines():
        if "has address" in line:
            ips.append(line.split()[-1])
    return ips


def reverse_lookup(ip):
    """
    Perform reverse DNS lookup on the given IP.
    Returns the resolved domain name if found, else None.
    """
    result = subprocess.run(["host", ip], capture_output=True, text=True, timeout=5, check=False)
    for line in result.stdout.splitlines():
        if "domain name pointer" in line:
            return line.split()[-1].strip(".")
    return None


def recursive_discovery(domain, depth=2):
    """
    Recursively discover subdomains and their IPs from a starting domain.
    Uses Amass, DNS resolution, and reverse lookups.
    """
    queue = [(domain, 0)]

    while queue:
        current_domain, level = queue.pop(0)
        if level > depth or current_domain in seen_domains:
            continue

        seen_domains.add(current_domain)
        subdomains = run_amass(current_domain)

        for sub in subdomains:
            if sub in seen_domains:
                continue

            seen_domains.add(sub)
            print(f"[+] Résolution IP de {sub}")
            ips = resolve_ip(sub)

            for ip in ips:
                if ip not in seen_ips:
                    seen_ips.add(ip)
                    print(f"    - IP trouvée: {ip}")

                    rev = reverse_lookup(ip)
                    if rev and rev not in seen_domains:
                        print(f"      ↳ PTR trouvé : {rev}")
                        queue.append((rev, level + 1))

            queue.append((sub, level + 1))

    print("\n=== Résumé ===")
    print(f"{len(seen_domains)} domaines découverts :")
    for d in seen_domains:
        print(f" - {d}")
    print(f"\n{len(seen_ips)} IPs uniques :")
    for ip in seen_ips:
        print(f" - {ip}")


if __name__ == "__main__":
    start_domain = input("Nom de domaine de départ : ").strip()
    recursive_discovery(start_domain)
