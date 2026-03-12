# ISO/SAE 21434 TARA & Requirements Report

## 1. Target of Evaluation (BoM)
* MCU/MPU (NXP S32G2, MPC574xB-C-G)
* CAN Interface/Transceivers
* LIN Interface/Transceivers
* FlexRay Transceivers
* Ethernet PHY (TJA1100HN, TJA1102/A)
* Ethernet Switch (SJA1105, SJA1110 series)
* PMIC and CAN/LIN SBC (VR5510)
* CAN Networks (Logical Bus)
* LIN Networks (Logical Bus)
* FlexRay Network (Logical Bus)
* Ethernet Network(s) (Logical Bus)
* Data Filtering Functionality
* OTA Firmware Update Functionality
* Vehicle Data (on Buses)

## 2. Threat Analysis & Risk Matrix with STRIDE
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
* **Control:** The gateway MCU/MPU shall implement a secure boot mechanism that cryptographically verifies the integrity and authenticity of all loaded firmware images before execution.
  * **Rationale:** *Secure boot prevents the execution of tampered or unauthorized firmware by verifying digital signatures and checksums, thereby ensuring that only trusted software runs on the MCU/MPU. This directly mitigates the tampering threat and ensures the integrity and availability of the MCU/MPU's operations.*

**Maps to Goal:** The gateway MCU/MPU shall ensure the integrity and authenticity of its software to prevent unauthorized execution of malicious code.
* **Control:** The gateway MCU/MPU shall implement hardware-enforced memory protection (e.g., MPU/MMU) to isolate critical software components and data from unauthorized access or modification.
  * **Rationale:** *Memory protection mechanisms prevent malicious code (even if partially injected) from accessing or corrupting critical system memory areas, thereby improving the integrity and availability of the MCU/MPU and its functions.*

**Maps to Goal:** The OTA firmware update mechanism shall ensure the integrity and authenticity of all updates delivered to connected ECUs to prevent malicious software deployment.
* **Control:** The OTA firmware update process shall utilize strong cryptographic signatures to authenticate the origin and verify the integrity of all firmware packages before installation on any ECU.
  * **Rationale:** *Cryptographic signatures ensure that firmware updates originate from a trusted source and have not been tampered with in transit. This directly mitigates spoofing and tampering threats, safeguarding the integrity and authenticity of OTA updates.*

**Maps to Goal:** The OTA firmware update mechanism shall ensure the integrity and authenticity of all updates delivered to connected ECUs to prevent malicious software deployment.
* **Control:** The gateway shall implement secure communication channels (e.g., TLS) for all external communication related to OTA updates, including fetching update packages and status reporting.
  * **Rationale:** *Secure communication channels protect against eavesdropping, tampering, and man-in-the-middle attacks during the OTA update process, ensuring the confidentiality and integrity of the update delivery mechanism.*

**Maps to Goal:** The gateway's data filtering functionality shall maintain the integrity and availability of its rules to prevent unauthorized data flow between vehicle networks.
* **Control:** The gateway shall implement robust access control mechanisms to prevent unauthorized modification or bypass of its data filtering rules, allowing only authenticated and authorized entities to manage configurations.
  * **Rationale:** *Access control ensures that only authorized personnel or processes can alter filtering rules, preventing malicious bypasses or modifications, thereby maintaining the integrity and availability of the filtering functionality.*

**Maps to Goal:** The gateway's data filtering functionality shall maintain the integrity and availability of its rules to prevent unauthorized data flow between vehicle networks.
* **Control:** The gateway shall employ deep packet inspection (DPI) capabilities to validate the structure and content of messages against expected protocols and values before forwarding them between different vehicle networks.
  * **Rationale:** *DPI goes beyond basic packet filtering to analyze the content of messages, detecting anomalous or malicious data that might conform to basic protocol headers but contain unsafe payloads, thus enhancing the integrity of data flow.*

**Maps to Goal:** The confidentiality, integrity, and availability of vehicle data communicated via in-vehicle buses (CAN, LIN, FlexRay, Ethernet) shall be protected against unauthorized access or modification.
* **Control:** The gateway shall implement message authentication and integrity checks (e.g., MACs, secure on-board communication - SecOC) for safety-critical messages transmitted across CAN, FlexRay, and Ethernet buses.
  * **Rationale:** *Message authentication and integrity checks ensure that critical data messages originate from legitimate sources and have not been altered in transit, directly mitigating spoofing and tampering threats on the bus, thus preserving data integrity and authenticity.*

**Maps to Goal:** The confidentiality, integrity, and availability of vehicle data communicated via in-vehicle buses (CAN, LIN, FlexRay, Ethernet) shall be protected against unauthorized access or modification.
* **Control:** The gateway shall enforce strict separation and isolation between different vehicle network domains (e.g., using VLANs for Ethernet, and logical partitioning for CAN/LIN) to limit the impact of a compromise in one domain.
  * **Rationale:** *Network segregation limits the blast radius of a successful attack, preventing an attacker who compromises one network from easily gaining access or control over other, more critical, vehicle networks. This enhances overall system availability and integrity.*

