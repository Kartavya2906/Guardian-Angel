#  Guardian Angel  
**Preventive Security for Open-Source Software Supply Chains**

## Overview
Modern software relies heavily on open-source libraries, creating a large and often invisible attack surface. Recent incidents such as Log4j, the XZ Utils backdoor, typosquatting attacks, and maintainer compromise show that attackers now target the software supply chain rather than applications directly.

Guardian Angel is a preventive security system that monitors open-source repositories, detects anomalous and malicious behavior, and alerts developers before compromised code reaches production.

---

## Problem
Most existing supply-chain security tools are reactive and signature-based. They focus on known vulnerabilities (CVEs) and often fail to detect:
- Logic-level backdoors
- Obfuscated or encrypted malicious payloads
- Maintainer account compromise
- Subtle behavioral changes across versions

---

## Solution
Guardian Angel uses behavior-based analysis to proactively identify supply-chain threats by monitoring repository activity and code changes in real time.

---

## High-Level Architecture

## High-Level Architecture

```text
GitHub Repository
        ↓
Commit & Release Monitor
        ↓
Static Code Analysis
        ↓
Behavioral Anomaly Detection
        ↓
Cryptanalysis & Obfuscation Scan
        ↓
Risk Scoring Engine
        ↓
Alerts & Dashboard



---

## Key Features
- Real-time monitoring of open-source repositories
- Detection of suspicious code changes and behavior drift
- Identification of encrypted or obfuscated payloads
- Maintainer behavior anomaly detection
- Early risk alerts before production integration

---

## Tech Stack
- Python
- GitHub API
- Machine Learning (Anomaly Detection)
- Power BI (Visualization)
- Azure (Deployment)

---

## Project Status
🚧 Work in progress — modular and extensible by design.

---

## One-Line Summary
An AI-driven guardian that protects open-source software from supply-chain attacks.
