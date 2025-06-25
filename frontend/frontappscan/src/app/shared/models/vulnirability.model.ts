export interface Scan {
  id: number;
  name: string;
  target: string;
  type: string;
  status: string;
  createdAt: string;
  vulnerabilitiesCount: number;
  severityCounts: Record<string, number>;
  duration: number;
}

export interface Vulnerability {
  id: string;
  scanId: string;
  title: string;
  description: string;
  severity: string;
  category: string;
  status: string;
  remediation: string;
  target: string;
  detectedAt: string;
}
