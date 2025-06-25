from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from fastapi.responses import FileResponse
import os
from fpdf import FPDF
import random

router = APIRouter()


#  Modèles de données

class ScanRequest(BaseModel):
    url: str
    name: Optional[str] = None
    scan_type: Optional[str] = "passif"

class Vulnerability(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    category: str
    detected_at: datetime

class Scan(BaseModel):
    id: int
    name: str
    target: str
    type: str
    status: str
    createdAt: datetime
    vulnerabilitiesCount: int
    severityCounts: dict
    duration: int


# Données en mémoire

scans: List[Scan] = []
vulnerabilities_by_scan = {}
scan_counter = 1


#  Génération de vulnérabilités dynamiques

def generate_fake_vulns(url: str) -> List[Vulnerability]:
    now = datetime.utcnow()
    base = [
        {"title": "SQL Injection", "description": "Entrée non échappée détectée", "severity": "High", "category": "Injection"},
        {"title": "XSS", "description": "Cross-site scripting détecté", "severity": "Medium", "category": "XSS"},
        {"title": "Directory Traversal", "description": "Fuite possible de fichiers sensibles", "severity": "Low", "category": "Path"},
        {"title": "CSRF", "description": "Absence de token CSRF", "severity": "High", "category": "Session"},
        {"title": "Clickjacking", "description": "Absence d'en-tête X-Frame-Options", "severity": "Medium", "category": "Headers"},
    ]
    selected = random.sample(base, random.randint(1, 3))
    return [
        Vulnerability(
            id=i + 1,
            title=v["title"],
            description=v["description"],
            severity=v["severity"],
            category=v["category"],
            detected_at=now
        ) for i, v in enumerate(selected)
    ]


# Créer un nouveau scan

@router.post("/scan", response_model=Scan)
def start_scan(scan_request: ScanRequest):
    global scan_counter
    scan_id = scan_counter
    scan_counter += 1

    created_at = datetime.utcnow()
    vulns = generate_fake_vulns(scan_request.url)
    vulnerabilities_by_scan[scan_id] = vulns

    # Compter les niveaux de sévérité
    severity_count = {
        "critical": 0,
        "high": sum(1 for v in vulns if v.severity == "High"),
        "medium": sum(1 for v in vulns if v.severity == "Medium"),
        "low": sum(1 for v in vulns if v.severity == "Low"),
    }

    scan_data = Scan(
        id=scan_id,
        name=scan_request.name or f"Scan {scan_id}",
        target=scan_request.url,
        type=scan_request.scan_type,
        status="completed",
        createdAt=created_at,
        vulnerabilitiesCount=len(vulns),
        severityCounts=severity_count,
        duration=random.randint(3, 10)
    )

    scans.append(scan_data)
    return scan_data

# ----------------------
# 📄 Obtenir tous les scans
# ----------------------
@router.get("/scan", response_model=List[Scan])
def get_scans():
    return scans


#  Obtenir les détails d’un scan

@router.get("/scan/{scan_id}")
def get_scan_details(scan_id: int):
    scan = next((s for s in scans if s.id == scan_id), None)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan non trouvé")

    return {
        "scan": scan,
        "vulnerabilities": vulnerabilities_by_scan.get(scan_id, [])
    }


#  Télécharger le rapport PDF

def generate_pdf_report(scan, vulnerabilities, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Rapport de Scan #{scan.id}", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Nom: {scan.name}", ln=True)
    pdf.cell(0, 10, f"URL: {scan.target}", ln=True)
    pdf.cell(0, 10, f"Type: {scan.type}", ln=True)
    pdf.cell(0, 10, f"Statut: {scan.status}", ln=True)
    pdf.cell(0, 10, f"Durée: {scan.duration} secondes", ln=True)
    pdf.cell(0, 10, f"Vulnérabilités détectées: {len(vulnerabilities)}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Détails des vulnérabilités :", ln=True)
    pdf.set_font("Arial", size=12)

    if not vulnerabilities:
        pdf.cell(0, 10, "Aucune vulnérabilité détectée.", ln=True)
    else:
        for vuln in vulnerabilities:
            pdf.ln(5)
            pdf.cell(0, 10, f"ID: {vuln.id}", ln=True)
            pdf.cell(0, 10, f"Titre: {vuln.title}", ln=True)
            pdf.cell(0, 10, f"Description: {vuln.description}", ln=True)
            pdf.cell(0, 10, f"Sévérité: {vuln.severity}", ln=True)
            pdf.cell(0, 10, f"Catégorie: {vuln.category}", ln=True)
            pdf.cell(0, 10, f"Date détectée: {vuln.detected_at.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.output(pdf_path)

@router.get("/scan/{scan_id}/report")
def download_report(scan_id: int):
    # Récupérer scan et vulnérabilités
    scan = next((s for s in scans if s.id == scan_id), None)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan non trouvé")
    vulns = vulnerabilities_by_scan.get(scan_id, [])

    pdf_path = f"rapport_scan_{scan_id}.pdf"
    generate_pdf_report(scan, vulns, pdf_path)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Rapport PDF non généré")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"rapport_{scan_id}.pdf",
        headers={"Content-Disposition": f"attachment; filename=rapport_{scan_id}.pdf"}
    )