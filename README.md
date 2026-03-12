# Agentic-TARA: Multi-modal AI for ISO/SAE 21434 Compliance

**Created by Komuraiah Poodari, CISSP**

A multi-modal AI agent built on Google's Agent Development Kit (ADK), Vertex AI environment, and Gemini 2.5 Flash, designed to automate Threat Analysis and Risk Assessments (TARA) for automotive cyber-physical systems. This version is a Proof-of-Concept (POC).

## 🎯 Project Overview

The **Automated Threat Analysis and Risk Assessment (TARA) Agent** accelerates the automotive cybersecurity lifecycle by analyzing E/E architecture block diagrams and generating **ISO/SAE 21434** standard-aligned, audit-ready threat models. Unlike standard LLM implementations, this project uses a **hybrid AI-Deterministic approach**:

The goal is to compress time and resources required for TARA by leveraging Google ADK native multi-modal capabilities. This agent eliminates the manual bottleneck of parsing Bills of Materials (BoM) and calculating risk vectors, reducing a weeks-long engineering process down to hours.
* The AI conducts the threat analysis and risk assessment (TARA) based on the instructions provided by the developer.
* The model determines the impact and feasibility ratings.
* The model maps the (asset damage impact rating, feasibility rating) to risk based on ISO/SAE 21434 Annex H. guidance.
* The prescribes security goals and security requirements (engineering controls).



### Key Features

- 👁️ **Multi-modal Ingestion**: Natively processes PDFs, images (e.g., NXP/Texas Instruments block diagrams), or raw text descriptions.
- 🧩 **Automated BoM Extraction**: Visually identifies physical components (MCUs, PMICs) and logical networks (CAN-FD, Automotive Ethernet).
- 🧠 **Chain of Thought (CoT) Reasoning**: Provides explicit, auditable rationales for every Impact and Feasibility score to satisfy compliance audits.
- 🛡️ **Actionable Engineering Controls**: Maps high-risk threat scenarios to specific technical requirements (e.g., SecOC, MACsec, UWB distance bounding).
- 📊 **Dual-Format Output**: Automatically generates human-readable Markdown reports for review and machine-readable JSON payloads for direct MBSE/Jira ingestion.
- 🚀 **Built on Google ADK and Vertex AI environment**: Utilizing standard Python function calling for reliable, local file-system integration.
- 🧠 **STRIDE Threat Modeling**: Every threat scenario is categorized to ensure coverage of Spoofing, Tampering, Repudiation, Info Disclosure, DoS, and Elevation of Privilege.

- 🔝 **Maximum Impact Principle**: Automatically evaluates SFOP (Safety, Financial, Operational, Privacy) and bases the TARA on the highest identified impact level.

---

## Methodology & Standards
### 1. Threat Identification (STRIDE)
The agent uses the STRIDE framework to analyze each asset in the Bill of Materials. This ensures that the generated scenarios meet the requirements for "Threat Scenario Identification" as per ISO 21434 Section 15.
### 2. Risk Determination (Annex H)
To prevent "AI Hallucinations" in safety-critical scoring, the agent passes its findings to a deterministic Python function that enforces the standard risk matrix:


| Impact \ Feasibility | Very Low | Low | Medium | High |
| :--- | :--- | :--- | :--- | :--- |
| Severe | 2 | 3 | 4 | 5 |
| Major | 1 | 2 | 3 | 4 |
| Moderate | 1 | 2 | 2 | 3 |
| Negligible | 1 | 1 | 1 | 1 |

### 3. Feasibility Analysis (Annex G)
Attack feasibility also considers the Attack Vector (Network, Adjacent, Local, Physical).

## 📁 Project Folder Structure

```text
Agent-based-TARA/
├── README.md                      # Project documentation
├── .env                           # GDK environment
├── __init__.py                    # Initialization file
├── agent.py                       # Main TARA orchestrator and tool definitions
├── tara_output.json               # Machine-readable artifact (auto-generated)
└── tara_report.md                 # Human-readable audit report (auto-generated)
```

### File Descriptions

| File | Purpose |
|------|---------|
| **__init__.py** | Simple initialization file to import custom agent for ADK |
| **agent.py** | Contains the system prompt instructions, Chain of Thought constraints, and the custom Python tool for output (JSON and markdown files) generation |
| **tara_output.json** | The strict JSON payload containing the BoM, TARA matrix, Security Goals, and Requirements. Ready for MBSE integration. |
| **tara_report.md** |  A formatted, highly scannable Markdown report with conditional logic (e.g., highlighting Risk Values of 4 or 5). |

---

## 🏗️ Agent Architecture

The system uses a constrained, single-agent architecture optimized for deterministic 
output and local tool execution:

```

┌─────────────────────────────────────────────────────────────────┐
│                    Input Ingestion                              │
│         (PDF Block Diagram, Image, or Text Prompt)              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │    TARA Analyst      │
            │  (Core Logic Engine) │
            │                      │
            │ Model: Gemini 2.5-   │
            │        Flash         │
            │ Task: ISO/SAE 21434  │
            └──────────┬───────────┘
                       │
                       │ 1. Extracts BoM visually
                       │ 2. Computes CIA/SFOP Impact, based on STRIDE threat modeling and 
                       |    ISO/SAE 21434 Table H.8. risk mapping.
                       │ 3. Applies CoT Rationale
                       |
                       ▼
            ┌──────────────────────┐
            │   Tool Execution     │
            │(save_tara_artifacts) │
            └──────────┬───────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
   [tara_report.md]        [tara_output.json]
   (Human Review)          (MBSE Pipeline for future enhancement)
            └──────────────────────┘
```

## 🔧 Tools
```
save_tara_artifacts(json_payload: str)
```
A custom Python function natively bound to the ADK agent. It receives the massive JSON payload generated by the LLM in memory, parses it, and safely writes both the .json and formatted .md files to the local disk. This allows the agent to interact directly with the development environment without user copy-pasting.



## 🔄 Workflow
**1. Upload**: A systems engineer uploads an E/E architecture PDF to the ADK web interface.

**2. Vision Parsing**: The model "reads" the diagram, extracting components like the processor, network interfaces, or logical functional blocks.

**3. Threat Modeling**: The agent maps known automotive attack vectors (e.g., Remote OTA compromise, CAN spoofing) to the identified BoM.

**4. CoT Scoring**: The model calculates Risk Values (1-5) and documents the exact engineering rationale for the score using chain of thought(COT).

**5. Tool Trigger**: The agent automatically calls the Python script to save the files locally.


## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud Account with Vertex AI access
- Required libraries: `google-adk`

---

### Installation
```
1. git clone https://github.com/komer/tara.git)
2. source .venv/bin/activate  #in the parent directory
3. pip install google-adk
```

## 💬 Example Execution: NXP Gateway reference platform

### Scenario: Multi-modal Ingestion of an Automotive Gateway Architecture
**Input:** A PDF block diagram of the NXP Gateway reference platform with introduction and architecture block diagram
**Prompt:** "Perform a full TARA and generate security requirements based on this uploaded architecture diagram."




## 📊 Sample Output (abridged)

### Threat Analysis & Risk Matrix with STRIDE
| Asset | CIA | Damage Scenario | Impact | Impact Rationale | Threat Scenario | Feasibility | Feasibility Rationale | Risk |
|---|---|---|---|---|---|---|---|---|
| MCU/MPU | Integrity, Availability | Malicious code injected into MCU/MPU firmware, leading to incorrect data routing, manipulation, or denial of service for critical vehicle functions. | Severe | *The MCU/MPU is the central processing unit of the gateway. A compromise of its integrity or availability would directly lead to critical safety functions being bypassed or manipulated (S), rendering the vehicle inoperable (O), and potentially incurring significant repair costs and reputational damage (F). Therefore, the maximum impact is Severe. (Category: S, O)* | An attacker exploits a vulnerability in the gateway's network stack or an unpatched vulnerability in the MCU/MPU's bootloader/firmware update mechanism to remotely flash malicious firmware onto the MCU/MPU. | Medium | *This attack requires advanced technical skills and potentially remote access to the vehicle's network (e.g., via infotainment, cellular, or diagnostics). Exploiting an MCU/MPU bootloader involves specialized knowledge, but is plausible given time and resources, especially if known vulnerabilities exist or physical access allows for side-channel attacks. The presence of OTA updates indicates a possible remote vector for firmware manipulation. (STRIDE: Tampering, Spoofing)* | **4** 🚨 |
| OTA Firmware Update Functionality | Integrity, Authenticity | An attacker delivers a malicious OTA firmware update to ECUs through the gateway, compromising their functionality, safety, or privacy. | Severe | *Compromised OTA updates could lead to widespread installation of malicious software across multiple ECUs, directly impacting vehicle safety (S) by causing malfunctions or unintended behavior. This could also lead to severe operational failures (O) and significant financial repercussions for recalls, repairs, and legal liabilities (F). The maximum impact is Severe. (Category: S, O)* | An attacker intercepts or spoofs the OTA update server, or gains control over the gateway's update mechanism, to push unauthorized or malicious firmware packages to connected ECUs. | Medium | *Exploiting OTA update mechanisms requires sophisticated knowledge of cryptographic protocols, server infrastructure, or specific gateway vulnerabilities. While challenging, known vulnerabilities in update processes have been demonstrated. This could involve network-based attacks (e.g., DNS spoofing, man-in-the-middle) or exploiting vulnerabilities in the gateway's update client. (STRIDE: Spoofing, Tampering)* | **4** 🚨 |
| Data Filtering Functionality | Integrity, Availability | The gateway's data filtering rules are bypassed or altered, allowing unauthorized and potentially malicious data packets to traverse between vehicle networks, leading to compromise of connected ECUs. | Major | *Bypassing data filtering could enable an attacker to reach and compromise safety-critical ECUs, leading to unintended vehicle behavior (S) or operational failures (O). While not directly manipulating core gateway functions, it facilitates attacks on other critical components. The financial impact (F) could be substantial due to potential repairs and liabilities. The maximum impact is Major. (Category: S, O)* | An attacker exploits a vulnerability in the gateway's firewall or filtering software to inject crafted packets that bypass filtering rules, or modifies the rules themselves, allowing unauthorized network traffic. | High | *Exploiting network filtering rules often involves sophisticated network penetration techniques, fuzzing, or exploiting known vulnerabilities in the filtering software. If the gateway provides diagnostic access, this could be a vector. Such attacks often require prior knowledge of the network protocols and filtering logic. (STRIDE: Tampering, Bypass of Security Features)* | **4** 🚨 |
| Vehicle Data (on Buses) | Confidentiality, Integrity, Availability | Sensitive vehicle data (e.g., sensor readings, control commands) is intercepted, modified, or replayed by an attacker on CAN, LIN, FlexRay, or Ethernet buses, causing incorrect vehicle behavior or data leakage. | Severe | *Manipulation of critical vehicle data directly impacts safety (S) by causing erroneous control commands or sensor readings, potentially leading to accidents. Data leakage could expose sensitive operational information (P). Disruption of data flow causes severe operational impact (O). Financial implications (F) could be substantial. The maximum impact is Severe. (Category: S, P, O)* | An attacker with physical access to the vehicle (e.g., via OBD-II port, exposed wiring) or having compromised an ECU connected to the bus, injects malicious messages, or eavesdrops on communications. | Low | *Attacks on in-vehicle buses (CAN, LIN) often require physical access to the network or a compromised ECU connected to the network. While physical access lowers the technical barrier, it is still a specific requirement. Eavesdropping and injection on these buses with physical access is well-documented and relatively straightforward with off-the-shelf tools. Ethernet buses might allow for more complex remote attacks if not properly secured. (STRIDE: Tampering, Spoofing, Information Disclosure)* | 3 |

## 3. Security Goals (Risk Treatment)
**Asset:** MCU/MPU
> The gateway MCU/MPU shall ensure the integrity and authenticity of its software to prevent unauthorized execution of malicious code.

**Asset:** OTA Firmware Update Functionality
> The OTA firmware update mechanism shall ensure the integrity and authenticity of all updates delivered to connected ECUs to prevent malicious software deployment.

**Asset:** Data Filtering Functionality
> The gateway's data filtering functionality shall maintain the integrity and availability of its rules to prevent unauthorized data flow between vehicle networks.

**Asset:** Vehicle Data (on Buses)
> The confidentiality, integrity, and availability of vehicle data communicated via in-vehicle buses (CAN, LIN, FlexRay, Ethernet) shall be protected against unauthorized access or modification.

## 4. Security Requirements (Engineering Controls)
**Maps to Goal:** The gateway MCU/MPU shall ensure the integrity and authenticity of its software to prevent unauthorized execution of malicious code.

## 📦 Configuration

The agent's parameters can be modified directly in the `tara/agent.py` file. 

To change the underlying reasoning engine or adjust constraints:
```python
root_agent = Agent(
    name='tara_analyst',
    model='gemini-2.5-flash', # Can be upgraded to 'gemini-2.5-pro' for deeper reasoning
    # ...
)
```
## 📄 License

Licensed under the Apache License 2.0. See LICENSE file for details.

---

## 🤝 Contributing

1. Contributions to improve the agent's architectural recognition or ISO/SAE 21434 compliance logic are **highly appreciated!**

2. Fork the repository

3. Create a feature branch (git checkout -b feature/enhanced-cot-logic)

5. Commit your changes (git commit -m 'Add detailed SecOC requirement rationale')

6. Push to the branch (git push origin feature/enhanced-cot-logic)

7. Open a Pull Request

---

## 📚 References
1. ISO/SAE 21434: Road vehicles — Cybersecurity engineering

2. Google Agent Development Kit (ADK)

3. Gemini Multi-modal API Documentation


## ⚠️ Disclaimer

This tool is a **Proof of Concept (POC)** designed to accelerate the threat modeling process. LLMs are probabilistic systems. All AI-generated Threat Analysis and Risk Assessments (TARAs), Security Goals, and Engineering Requirements must be rigorously reviewed and verified by a qualified Human-in-the-Loop (HITL) before being applied to safety-critical cyber-physical systems. This tool in its current state shall not be used for production system assessments. It is work-in-progress.