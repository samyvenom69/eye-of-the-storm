"""
Port Scanning Module — Phase: RECON
WARNING: Only scan systems you own or have written permission to scan.
Uses python-nmap as a wrapper around the nmap tool.
"""
import nmap
from modules import BaseModule
from utils.banner import print_result

class PortScanModule(BaseModule):
    """TCP/UDP port scanning via Nmap — authorized targets only."""
    DEFAULT_PORTS = "21,22,25,53,80,443,3306,3389,8080,8443"
    def run(self) -> dict:
        results = {"target": self.target, "open_ports": [], "scan_info": {}}
        self.info(f"[PORTSCAN] Target: {self.target} (authorized scan only)")
        try:
            nm = nmap.PortScanner()
            nm.scan(self.target, self.DEFAULT_PORTS, arguments="-sV --open -T3")
            for host in nm.all_hosts():
                results["scan_info"]["host"]   = host
                results["scan_info"]["state"]  = nm[host].state()
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto]:
                        svc = nm[host][proto][port]
                        if svc["state"] == "open":
                            entry = {
                                "port":    port,
                                "proto":   proto,
                                "service": svc.get("name", ""),
                                "version": svc.get("version", ""),
                            }
                            results["open_ports"].append(entry)
                            print_result(f"{proto}/{port}", f"{entry['service']} {entry['version']}", color="yellow")
        except Exception as e:
            self.error(f"Nmap error: {e}")
            results["error"] = str(e)
        return results
