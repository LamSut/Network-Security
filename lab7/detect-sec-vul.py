import nmap
import re

def scan_all_ports(ip):
    scanner = nmap.PortScanner()
    print(f"Scanning all ports on {ip}...")

    # Scan all ports with service detection and vulnerability scripts
    scanner.scan(ip, "1-65535", arguments="-sV --script vuln")

    open_ports = []
    for host in scanner.all_hosts():
        for port, port_info in scanner[host].get("tcp", {}).items():
            if port_info.get("state") == "open":
                open_ports.append({
                    "port": port,
                    "service": port_info.get("name", "unknown"),
                    "version": port_info.get("version", "unknown"),
                    "vulnerabilities": port_info.get("script", {})
                })

    return open_ports

def analyze_vulnerabilities(port_data):
    risk_level = "Low"
    vulnerabilities = port_data.get("vulnerabilities", {})

    if vulnerabilities:
        for script, output in vulnerabilities.items():
            if re.search(r"vulnerable|CVE-\d{4}-\d+", output, re.IGNORECASE):
                risk_level = "High"
                break
            elif "potential" in output.lower():
                risk_level = "Medium"

    return risk_level

if __name__ == "__main__":
    target_ip = "127.0.0.1"
    
    results = scan_all_ports(target_ip)

    if results:
        print("\n🔎 Open Ports and Security Assessment:")
        for port_info in results:
            port = port_info["port"]
            service = port_info["service"]
            version = port_info["version"]
            risk = analyze_vulnerabilities(port_info)

            print(f"➡ Port {port} ({service} - {version}): Risk Level: {risk}")
            
            if risk == "High":
                print("   ⚠️  Immediate action required: Check for security patches.")
            elif risk == "Medium":
                print("   🟠 Review security settings and restrict access if necessary.")
            else:
                print("   ✅ No major vulnerabilities detected.")
    else:
        print("✅ No open ports detected.")

