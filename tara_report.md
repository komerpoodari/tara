# ISO/SAE 21434 TARA & Requirements Report

## 1. Target of Evaluation (BoM)
* MCU/MPU (NXP S32G2 Processors, NXP MPC574xB-C-G)
* PMIC and CAN/LIN SBC (NXP VR5510)
* CAN Transceiver
* LIN Transceiver
* FlexRay Transceiver
* Ethernet PHY (NXP TJA1100HN, NXP TJA1102/TJA1102A)
* Ethernet Switch (NXP SJA1105EL, NXP SJA1105TEL, NXP SJA1105PEL/QEL/REL/SEL Series, NXP SJA1110)
* CAN Networks (Bus)
* LIN Networks (Bus)
* FlexRay Network (Bus)
* Ethernet Network(s) (Bus)
* VBAT (Power Supply)

## 2. Threat Analysis & Risk Matrix
| Asset | CIA | Damage Scenario | Impact | Threat Scenario | Feasibility | Risk Value |
|---|---|---|---|---|---|---|
| MCU/MPU | Integrity | Malicious firmware update causing incorrect routing or control commands, leading to loss of vehicle control or unexpected behavior. | Severe | Remote attacker compromises an attached ECU or the OTA update mechanism, flashing unauthorized/malicious firmware to the gateway MCU. | High | **5** 🚨 |
| MCU/MPU | Confidentiality | Unauthorized access to sensitive vehicle data (e.g., driver behavior, location, diagnostic data) processed or stored by the gateway. | Major | Insider threat or remote attacker exploiting vulnerabilities in gateway software to exfiltrate data. | Medium | **4** 🚨 |
| MCU/MPU | Availability | Denial of Service (DoS) attack on the gateway, preventing critical communication between vehicle domains. | Severe | Malicious messages flooding the gateway interfaces or exploiting software vulnerabilities to crash the MCU/MPU. | High | **5** 🚨 |
| CAN Networks | Integrity | Injection of malicious CAN messages (e.g., fake speed signals, brake commands) leading to unintended vehicle behavior. | Severe | Attacker with physical access or through a compromised ECU on the CAN bus injects forged messages. | High | **5** 🚨 |
| LIN Networks | Integrity | Manipulation of LIN messages controlling less critical functions (e.g., window control, climate). | Moderate | Attacker with physical access or through a compromised ECU on the LIN bus injects forged messages. | Medium | 3 |
| Ethernet Network(s) | Integrity | Manipulation or spoofing of Ethernet frames, leading to incorrect data exchange for safety-critical functions (e.g., ADAS sensor data, vehicle control commands). | Severe | Attacker gains access to the Ethernet network and injects malicious packets, or performs ARP spoofing/MAC spoofing. | High | **5** 🚨 |
| Ethernet Network(s) | Confidentiality | Eavesdropping on unencrypted vehicle data transmitted over Automotive Ethernet. | Major | Attacker with network access monitors traffic. | Medium | **4** 🚨 |
| Ethernet Switch (SJA1105/SJA1110) | Integrity/Availability | Manipulation of switch configuration (e.g., VLANs, filtering rules) or flooding, leading to misrouting of critical data or network DoS. | Severe | Attacker exploits vulnerabilities in switch management interface or sends malformed packets to disrupt its operation. | Medium | **4** 🚨 |
| PMIC and CAN/LIN SBC (VR5510) | Availability | Malicious manipulation of power supply settings or fault injection, leading to system instability or shutdown. | Severe | Attacker with physical access or via compromised MCU gains control of SBC features and disrupts power management. | Medium | **4** 🚨 |

## 3. Security Goals (Risk Treatment)
**Asset:** MCU/MPU
> Ensure the integrity and authenticity of all software and configuration data loaded and executed on the MCU/MPU.

**Asset:** MCU/MPU
> Prevent unauthorized access to sensitive data stored or processed by the MCU/MPU.

**Asset:** MCU/MPU
> Ensure the continuous availability and proper functioning of the MCU/MPU and its critical communication services.

**Asset:** CAN Networks
> Prevent the injection, modification, or replay of unauthorized messages on the CAN networks.

**Asset:** Ethernet Network(s)
> Prevent the injection, modification, or replay of unauthorized messages on the Ethernet networks.

**Asset:** Ethernet Network(s)
> Protect the confidentiality of sensitive data transmitted over the Ethernet networks.

**Asset:** Ethernet Switch (SJA1105/SJA1110)
> Prevent unauthorized configuration changes or disruption of the Ethernet switch's operation.

**Asset:** PMIC and CAN/LIN SBC (VR5510)
> Prevent unauthorized manipulation of power management and bus control functions of the PMIC/SBC.

## 4. Security Requirements (Engineering Controls)
**Maps to Goal:** Ensure the integrity and authenticity of all software and configuration data loaded and executed on the MCU/MPU.
* **Control:** Implement secure boot and authenticated firmware updates using cryptographic signatures (e.g., RSA or ECC) to verify software integrity before execution.

**Maps to Goal:** Ensure the integrity and authenticity of all software and configuration data loaded and executed on the MCU/MPU.
* **Control:** Implement a hardware security module (HSM) or secure element for cryptographic operations and secure key storage.

**Maps to Goal:** Prevent unauthorized access to sensitive data stored or processed by the MCU/MPU.
* **Control:** Enforce strict access control mechanisms (e.g., memory protection unit, privilege levels) within the MCU/MPU to isolate sensitive data and code.

**Maps to Goal:** Prevent unauthorized access to sensitive data stored or processed by the MCU/MPU.
* **Control:** Encrypt sensitive data at rest and in transit within the gateway.

**Maps to Goal:** Ensure the continuous availability and proper functioning of the MCU/MPU and its critical communication services.
* **Control:** Implement robust input validation and message filtering mechanisms on all network interfaces to prevent malformed or malicious messages from causing DoS.

**Maps to Goal:** Ensure the continuous availability and proper functioning of the MCU/MPU and its critical communication services.
* **Control:** Incorporate watchdog timers and fault detection/recovery mechanisms to ensure system resilience.

**Maps to Goal:** Prevent the injection, modification, or replay of unauthorized messages on the CAN networks.
* **Control:** Implement in-vehicle network intrusion detection/prevention systems (IDS/IPS) capable of anomaly detection and filtering on CAN messages.

**Maps to Goal:** Prevent the injection, modification, or replay of unauthorized messages on the CAN networks.
* **Control:** Employ Message Authentication Codes (MACs) or cryptographic checksums for critical CAN messages, where feasible, to verify authenticity and integrity.

**Maps to Goal:** Prevent the injection, modification, or replay of unauthorized messages on the Ethernet networks.
* **Control:** Implement secure onboard communication protocols (e.g., MACsec, TLS over IPsec) for all critical data transmitted over Automotive Ethernet.

**Maps to Goal:** Prevent the injection, modification, or replay of unauthorized messages on the Ethernet networks.
* **Control:** Employ packet filtering and firewall rules at the gateway's Ethernet interfaces to restrict unauthorized traffic.

**Maps to Goal:** Protect the confidentiality of sensitive data transmitted over the Ethernet networks.
* **Control:** Encrypt all sensitive data transmitted over Automotive Ethernet using strong cryptographic algorithms (e.g., AES-256).

**Maps to Goal:** Protect the confidentiality of sensitive data transmitted over the Ethernet networks.
* **Control:** Implement secure key management and exchange protocols for encryption keys.

**Maps to Goal:** Prevent unauthorized configuration changes or disruption of the Ethernet switch's operation.
* **Control:** Securely configure the Ethernet switch with robust access controls for its management interface, preventing unauthorized modification of VLANs, QoS, or filtering rules.

**Maps to Goal:** Prevent unauthorized configuration changes or disruption of the Ethernet switch's operation.
* **Control:** Implement port security features (e.g., MAC address filtering) on the Ethernet switch to prevent unauthorized devices from connecting.

**Maps to Goal:** Prevent unauthorized manipulation of power management and bus control functions of the PMIC/SBC.
* **Control:** Implement hardware-based write protection or access control for critical PMIC/SBC registers and configuration settings, accessible only by authenticated gateway software.

**Maps to Goal:** Prevent unauthorized manipulation of power management and bus control functions of the PMIC/SBC.
* **Control:** Monitor PMIC/SBC operational parameters for anomalies indicating tampering or malfunction.

