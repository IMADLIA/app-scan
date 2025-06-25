import asyncio
from typing import List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import random

from ..database.models import Scan, Vulnerability

class ScanService:
    """Service pour gérer les scans de vulnérabilités"""

    async def launch_scan(self, db: AsyncSession, scan: Scan) -> Dict:
        """
        Lance un scan de vulnérabilités (simulé) et enregistre les résultats.
        Args:
            db: Session de base de données
            scan: Instance du scan à exécuter
        Returns:
            Dictionnaire contenant les résultats du scan
        """
        # Mettre à jour le statut du scan
        scan.status = "running"
        scan.started_at = datetime.utcnow()
        await db.commit()
        await db.refresh(scan)

        # Simuler un scan (délai pour imiter une opération longue)
        await asyncio.sleep(5)  # Simulation d'un scan de 5 secondes

        # Générer des vulnérabilités fictives
        vulnerabilities = self._generate_mock_vulnerabilities(scan.target_url)

        # Enregistrer les vulnérabilités dans la base de données
        for vuln_data in vulnerabilities:
            vulnerability = Vulnerability(
                scan_id=scan.id,
                severity=vuln_data["severity"],
                title=vuln_data["title"],
                description=vuln_data.get("description"),
                cve_id=vuln_data.get("cve_id"),
                solution=vuln_data.get("solution"),
                url=vuln_data.get("url"),
                parameter=vuln_data.get("parameter"),
                evidence=vuln_data.get("evidence"),
                created_at=datetime.utcnow()
            )
            db.add(vulnerability)

        # Mettre à jour le scan avec les résultats
        scan.status = "completed"
        scan.completed_at = datetime.utcnow()
        scan.results = {"vulnerabilities_count": len(vulnerabilities)}
        await db.commit()
        await db.refresh(scan)

        return {
            "scan_id": scan.id,
            "status": scan.status,
            "vulnerabilities_count": len(vulnerabilities),
            "vulnerabilities": vulnerabilities
        }

    def _generate_mock_vulnerabilities(self, target_url: str) -> List[Dict]:
        """
        Génère des vulnérabilités fictives pour simuler un scan.
        Args:
            target_url: URL cible du scan
        Returns:
            Liste de dictionnaires représentant les vulnérabilités
        """
        severities = ["Low", "Medium", "High", "Critical"]
        titles = [
            "Cross-Site Scripting (XSS)",
            "SQL Injection",
            "Insecure Direct Object Reference (IDOR)",
            "Broken Authentication",
            "Server Misconfiguration"
        ]
        descriptions = [
            "Potential vulnerability allowing an attacker to inject malicious scripts.",
            "Improper SQL query handling may allow unauthorized database access.",
            "Access to unauthorized resources due to insufficient validation.",
            "Weak authentication mechanisms that can be bypassed.",
            "Server settings expose sensitive information."
        ]

        # Générer entre 0 et 5 vulnérabilités aléatoires
        num_vulns = random.randint(0, 5)
        vulnerabilities = []

        for _ in range(num_vulns):
            vuln = {
                "severity": random.choice(severities),
                "title": random.choice(titles),
                "description": random.choice(descriptions),
                "cve_id": f"CVE-2025-{random.randint(1000, 9999)}",
                "solution": "Apply input validation and sanitize user inputs.",
                "url": target_url,
                "parameter": "id" if random.choice([True, False]) else None,
                "evidence": "Detected via simulated scan."
            }
            vulnerabilities.append(vuln)

        return vulnerabilities