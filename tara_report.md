# ISO/SAE 21434 TARA & Requirements Report

## 1. Target of Evaluation (BoM)
* Gateway Module (physical device)
* MCU/MPU
* PMIC and CAN/LIN SBC
* CAN Interface (transceivers)
* LIN Interface (transceivers)
* FlexRay Transceivers
* Ethernet PHY
* Ethernet Switch
* CAN Networks (internal to vehicle)
* LIN Networks (internal to vehicle)
* FlexRay Network (internal to vehicle)
* Ethernet Network(s) (internal to vehicle)
* Data Filtering / Secure Interconnection Functionality
* OTA Firmware Update Functionality
* Vehicle Network Data (from powertrain, chassis, safety, body control, infotainment, telematics, ADAS)
* Firmware Images (for OTA updates)
* Configuration Data

## 2. Threat Analysis & Risk Matrix with STRIDE
| Asset | CIA | Damage Scenario | Impact | Impact Rationale | Threat Scenario | Feasibility | Feasibility Rationale | Risk |
|---|---|---|---|---|---|---|---|---|
| Gateway Module (MCU/MPU) | Integrity, Authenticity, Availability | Compromise of the Gateway's MCU/MPU leading to arbitrary code execution, allowing an attacker to bypass data filtering, inject malicious commands, or take control of vehicle functions. | Severe | *Safety (S) is Severe - The Gateway connects to safety-critical domains (powertrain, chassis, safety, ADAS). Compromise could lead to loss of vehicle control, malfunction of safety features, or unintended vehicle behavior, directly causing accidents or harm. Financial (F) is Severe - Vehicle damage, theft, recall costs, reputational damage. Operational (O) is Severe - Vehicle rendered inoperable, unreliable, or unsafe. Privacy (P) is Moderate - Potential access to aggregated vehicle usage data or location data flowing through the gateway. Therefore, the maximum impact is Severe (S, F, O).* | An attacker exploits a vulnerability in the Gateway's software/firmware (e.g., buffer overflow, unhandled input) via connected networks or interfaces to achieve remote code execution on the MCU/MPU. | Medium | *This threat involves Elevation of Privilege, Tampering, Denial of Service, Information Disclosure. It requires knowledge of the Gateway's specific vulnerabilities, potentially complex exploit development. Could originate from external interfaces (e.g., telematics, infotainment, if connected through the gateway) or internal vehicle networks if an adjacent ECU is compromised. This results in Medium feasibility.* | **4** 🚨 |
| Data Filtering / Secure Interconnection Functionality | Integrity, Authenticity, Confidentiality, Availability | Bypass of data filtering rules, allowing malicious or malformed data to pass between vehicle networks, leading to compromise of connected ECUs or unintended vehicle behavior. | Severe | *Safety (S) is Severe - If malicious data reaches safety-critical ECUs (e.g., powertrain, brakes), it could directly cause accidents or loss of control. Financial (F) is Severe - Vehicle damage, recall costs, legal liabilities. Operational (O) is Severe - Vehicle rendered unreliable, unsafe, or inoperable. Privacy (P) is Moderate - Malicious data flow could exfiltrate sensitive data. Therefore, the maximum impact is Severe (S, F, O).* | An attacker crafts malformed packets or exploits a logic flaw in the Gateway's filtering software to circumvent the intended security policies and inject unauthorized messages onto a different network domain. | Medium | *This threat involves Tampering (with data flow), Spoofing (of legitimate messages), Elevation of Privilege (to bypass security controls). It requires detailed knowledge of the gateway's filtering logic, network protocols, and potential vulnerabilities. Could be achieved through reverse engineering or exploiting known weaknesses. This often requires access to the network connected to the gateway. This results in Medium feasibility.* | **4** 🚨 |
| OTA Firmware Update Functionality | Integrity, Authenticity, Availability | Injection of malicious or unauthorized firmware updates to the Gateway or other ECUs, leading to full vehicle compromise or bricking of ECUs. | Severe | *Safety (S) is Severe - Malicious firmware can take complete control of vehicle functions, disable safety systems, or introduce dangerous behavior, directly leading to accidents or harm. Financial (F) is Severe - Bricked ECUs, vehicle repair/replacement costs, potential for mass recalls, reputational damage. Operational (O) is Severe - Vehicle rendered inoperable, unreliable, or unsafe. Privacy (P) is Moderate - Malicious firmware could exfiltrate data. Therefore, the maximum impact is Severe (S, F, O).* | An attacker intercepts the OTA update process or compromises the update server to deliver malicious firmware to the gateway or downstream ECUs. This could also involve exploiting vulnerabilities in the gateway's update client. | High | *This threat involves Tampering (with firmware), Spoofing (of update server), Elevation of Privilege (to flash unauthorized code), Denial of Service (bricking). While OTA systems are designed with security, vulnerabilities in the update server, communication channel, or the client-side update verification (e.g., weak crypto, implementation flaws) have been observed in other systems. A sophisticated attacker could target these weaknesses. The gateway is a central point for updates, making this a High feasibility attack due to the potential attack surface.* | **5** 🚨 |
| Vehicle Network Data (across CAN, LIN, FlexRay, Ethernet) | Confidentiality, Integrity, Authenticity | Eavesdropping on vehicle network data to gather sensitive information (e.g., location, driving habits, personal settings) or unauthorized injection of messages to manipulate vehicle behavior. | Severe | *Safety (S) is Severe - Injection of malicious commands onto critical networks (e.g., braking, steering) can cause immediate loss of control or accidents. Financial (F) is Major - Vehicle damage if manipulated, potential for data theft. Operational (O) is Major - Vehicle malfunction, unreliable operation. Privacy (P) is Severe - Comprehensive data about driver behavior, location, and potentially passenger information could be exposed. This impacts a large number of vehicle functions listed (infotainment, telematics, ADAS). Therefore, the maximum impact is Severe (S, P).* | An attacker gains access to any of the vehicle networks (CAN, LIN, FlexRay, Ethernet) directly or indirectly (e.g., via a compromised ECU) and intercepts or injects data. | Medium | *This threat involves Information Disclosure, Tampering, Spoofing. It requires physical access to the network (e.g., OBD-II port, tapping wires) or exploiting a vulnerability in a connected ECU to gain network access. Reverse engineering of network protocols (e.g., CAN IDs) is often needed. However, general tools for network analysis and injection are common, making this a Medium feasibility attack.* | **4** 🚨 |

## 3. Security Goals (Risk Treatment)
**Asset:** Gateway Module (MCU/MPU)
> The Gateway's MCU/MPU and its software shall be protected against unauthorized code execution and malicious control.

**Asset:** Data Filtering / Secure Interconnection Functionality
> The Gateway's data filtering and secure interconnection functionality shall maintain integrity and prevent unauthorized data flow between vehicle networks.

**Asset:** OTA Firmware Update Functionality
> The OTA firmware update mechanism shall ensure the authenticity and integrity of all firmware delivered to the Gateway and connected ECUs.

**Asset:** Vehicle Network Data (across CAN, LIN, FlexRay, Ethernet)
> The confidentiality, integrity, and authenticity of data communicated across vehicle networks (CAN, LIN, FlexRay, Ethernet) shall be protected.

## 4. Security Requirements (Engineering Controls)
**Maps to Goal:** The Gateway's MCU/MPU and its software shall be protected against unauthorized code execution and malicious control.
* **Control:** The Gateway MCU/MPU shall implement hardware-enforced secure boot, memory protection units (MPU/MMU), and runtime integrity monitoring.
  * **Rationale:** *This directly mitigates Elevation of Privilege, Tampering, and Denial of Service by ensuring only trusted code executes at startup, isolating critical processes, and detecting unauthorized changes during operation, making it harder for an attacker to achieve arbitrary code execution.*

**Maps to Goal:** The Gateway's data filtering and secure interconnection functionality shall maintain integrity and prevent unauthorized data flow between vehicle networks.
* **Control:** The Gateway shall implement stateful packet inspection and cryptographic authentication for critical data packets exchanged between different network domains.
  * **Rationale:** *This directly mitigates Tampering and Spoofing threats by ensuring that only valid and authenticated messages pass through the gateway, preventing malicious data injection and unauthorized access to different network segments.*

**Maps to Goal:** The OTA firmware update mechanism shall ensure the authenticity and integrity of all firmware delivered to the Gateway and connected ECUs.
* **Control:** The OTA update system shall use strong cryptographic signatures (e.g., ECC, RSA with sufficient key length) for all firmware images, with signature verification performed both on the Gateway and the target ECUs. A secure communication channel (e.g., TLS) shall be used for update delivery.
  * **Rationale:** *This directly mitigates Tampering, Spoofing, and Elevation of Privilege by ensuring that only firmware from trusted sources can be installed, preventing attackers from injecting malicious updates or bricking devices. The secure channel protects against interception and modification during transit.*

**Maps to Goal:** The confidentiality, integrity, and authenticity of data communicated across vehicle networks (CAN, LIN, FlexRay, Ethernet) shall be protected.
* **Control:** All critical safety-related and privacy-sensitive data communications on CAN, LIN, FlexRay, and Ethernet networks shall be protected with Message Authentication Codes (MACs) or encryption where confidentiality is required, and unique session keys.
  * **Rationale:** *This directly mitigates Information Disclosure, Tampering, and Spoofing threats by ensuring that sensitive data cannot be easily read, altered, or impersonated by an attacker who gains access to the network.*

