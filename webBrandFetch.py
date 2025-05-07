import subprocess
import re

def extract_brand(domain):
    try:
        result = subprocess.run(['whois', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        org_match = re.search(r'Registrant Organization:\s*(.+)', output, re.IGNORECASE)
        if org_match:
            return org_match.group(1).strip()

        name_match = re.search(r'Registrant Contact Name:\s*(.+)', output, re.IGNORECASE)
        if name_match:
            return name_match.group(1).strip()

        return "Brand not found"

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    domain = input("Enter a domain (e.g., mcdonalds.com): ").strip()
    brand = extract_brand(domain)
    print(f"Extracted Brand: {brand}")
