# ISO/SAE 21434 TARA & Requirements Report

## 1. Target of Evaluation (BoM)
* MCU/MPU
* PMIC
* System Basis Chip (SBC)
* CAN Transceiver
* LIN Transceiver
* FlexRay Transceiver
* Ethernet PHY
* Ethernet Switch
* CAN Interface
* LIN Interface
* FlexRay Interface
* Automotive Ethernet Interface
* CAN Networks
* LIN Networks
* FlexRay Networks
* Automotive Ethernet Networks
* Gateway Routing Logic
* Data Filtering / Firewall
* OTA Update Manager

## 2. Threat Analysis & Risk Matrix with STRIDE
| Asset | CIA | Damage Scenario | Impact | Impact Rationale | Threat Scenario | Feasibility | Feasibility Rationale | Risk |
|---|---|---|---|---|---|---|---|---|
| MCU/MPU | Confidentiality, Integrity, Availability | An attacker gains control of the MCU/MPU, executing malicious code that leads to unintended vehicle behavior (e.g., sudden braking, acceleration, or steering issues) or exfiltrating sensitive internal data and cryptographic keys. | Severe | *Safety impact dominates: Compromise of the core processing unit can lead to loss of vehicle control, resulting in severe injury or fatality. Operational impact is also severe, as the vehicle becomes unsafe or inoperable. (Category: S, O)* | An attacker exploits a firmware vulnerability (e.g., buffer overflow, insecure diagnostic interface) on the MCU/MPU via a diagnostic port or a remotely exploitable connected interface (e.g., infotainment, telematics unit). This allows them to inject and execute arbitrary code with elevated privileges. | Medium | *Requires significant expertise in embedded systems, reverse engineering, and exploit development for the specific MCU architecture. Access can range from local (diagnostic port) to remote (via network). The primary STRIDE threats are Tampering and Denial of Service, with potential Information Disclosure. (STRIDE: Tampering, Denial of Service, Information Disclosure)* | **4** 🚨 |
| PMIC | Integrity, Availability | An attacker manipulates the PMIC's settings, causing unstable voltage supply to critical ECUs or a sudden power shutdown, leading to system crashes, data corruption, or complete vehicle power loss during operation. | Severe | *Safety impact dominates: Unstable or absent power to safety-critical systems can cause sudden failures, leading to loss of vehicle control and severe accidents. Operational impact is severe as the vehicle becomes inoperable. (Category: S, O)* | An attacker, having gained control of the main MCU, sends malicious commands via an internal interface (e.g., I2C, SPI) to the PMIC to alter power regulation settings, trigger resets, or force a complete power down of the system. | Medium | *Requires an initial compromise of the controlling MCU, followed by expertise in the PMIC's register map and communication protocol. This is a targeted attack with adjacent access. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| System Basis Chip (SBC) | Integrity, Availability | An attacker causes the SBC to malfunction, disrupting critical communication transceivers (e.g., CAN, LIN) or power supply lines, leading to a sudden loss of network communication or system resets for attached ECUs, potentially during driving. | Severe | *Safety impact dominates: Failure of communication transceivers or power supply can disable safety-critical systems connected via those networks, potentially causing accidents. Operational impact is severe. (Category: S, O)* | Anattacker, having compromised the host MCU, sends malformed commands or exploits a vulnerability in the SBC's driver software via an internal bus (e.g., SPI) to disable integrated transceivers, force a system reset, or manipulate power management functions. | Medium | *Requires prior compromise of the controlling MCU and specific knowledge of the SBC's interface and functionality. This is a targeted attack with adjacent access. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| CAN Transceiver | Integrity, Availability | An attacker causes the CAN transceiver to malfunction, leading to corruption of legitimate CAN messages or preventing them from being transmitted, thus disrupting critical vehicle control signals and causing unsafe vehicle behavior. | Severe | *Safety impact dominates: Corruption or loss of safety-critical CAN messages can directly lead to dangerous vehicle behavior (e.g., loss of braking, unintended acceleration), posing a severe risk of injury or fatality. (Category: S)* | An attacker, having gained control of the host MCU, sends malicious commands to the CAN transceiver to force it into an error-passive state, disable it, or transmit erroneous bit patterns, effectively jamming or corrupting communication on the CAN bus. | Medium | *Requires prior compromise of the controlling MCU and understanding of the transceiver's control interface. While direct physical bus tampering can be easier for DoS, software control via MCU requires more expertise. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| LIN Transceiver | Integrity, Availability | An attacker causes the LIN transceiver to malfunction, preventing LIN messages from being sent or received. This results in the loss of basic comfort features (e.g., window control, interior lighting) or erratic behavior of LIN-connected devices. | Moderate | *Operational impact dominates: Disruption typically affects non-safety-critical comfort or basic body functions, leading to inconvenience and degraded user experience rather than direct safety risks. (Category: O)* | An attacker, having gained control of the host MCU, sends specific commands to the LIN transceiver to disable it, force it into a sleep mode, or flood the LIN bus with invalid frames, disrupting communication with LIN slave devices. | Medium | *Requires prior compromise of the controlling MCU and specific knowledge of the LIN transceiver's control registers. Similar to CAN transceiver, but LIN is simpler. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | 2 |
| FlexRay Transceiver | Integrity, Availability | An attacker causes the FlexRay transceiver to malfunction, disrupting the time-triggered communication or corrupting safety-critical FlexRay messages. This leads to immediate and catastrophic loss of highly critical functions like steering-by-wire or active suspension. | Severe | *Safety impact dominates: FlexRay typically carries safety-critical, time-synchronous data. Its disruption can lead to a complete loss of vehicle control, resulting in severe injury or fatality. (Category: S)* | An attacker, with deep access to the host MCU and specialized knowledge of FlexRay communication, sends malicious commands to the FlexRay transceiver to disrupt its precise timing, corrupt transmitted frames, or put it into an error state, causing a denial of service on the FlexRay network. | Medium | *Requires prior compromise of the controlling MCU and a very high level of expertise in FlexRay's complex time-triggered protocol and transceiver control. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| Ethernet PHY | Integrity, Availability | An attacker causes the Ethernet PHY to malfunction, corrupting or blocking Ethernet frames. This results in the loss of high-bandwidth communication for ADAS, infotainment, or diagnostic systems, potentially affecting critical driving functions or connectivity. | Major | *Operational impact dominates: Disrupts high-bandwidth communication essential for advanced features and potentially safety-related systems (e.g., ADAS data streams). While not always immediate safety, persistent disruption could be severe. (Category: O, S)* | An attacker, having gained control of the host MCU, sends malicious commands via the Management Data Input/Output (MDIO) interface to the Ethernet PHY to disable the link, force a lower speed, or manipulate its operational mode, causing communication failure or degradation. | Medium | *Requires prior compromise of the controlling MCU and expertise in Ethernet PHY management via MDIO. This is a targeted attack with adjacent access. The primary STRIDE threats are Tampering and Denial of Service. (STRIDE: Tampering, Denial of Service)* | 3 |
| Ethernet Switch | Confidentiality, Integrity, Availability | An attacker reconfigures the Ethernet switch, allowing unauthorized traffic between isolated network segments (e.g., exposing ADAS data to infotainment), performing a denial of service by blocking critical traffic, or corrupting routing tables, leading to system failure or data leakage. | Severe | *Safety impact dominates: Disruption of critical ADAS or vehicle control data paths can directly lead to accidents. Privacy impact is also severe due to unauthorized data disclosure. Operational impact is high due to network segmentation breach. (Category: S, P, O)* | An attacker exploits a vulnerability in the switch's management interface (e.g., SNMP, Web GUI, or via a compromised connected ECU) to reprogram its forwarding rules, VLAN configurations, or Quality of Service (QoS) settings. This can lead to traffic redirection, data exfiltration, or a denial of service for connected ECUs. | Medium | *Requires gaining access to the switch's management plane, either via a compromised adjacent ECU or a direct remote vector if exposed. Expertise in network configuration and switch vulnerabilities is needed. The primary STRIDE threats are Tampering, Information Disclosure, and Denial of Service. (STRIDE: Tampering, Information Disclosure, Denial of Service)* | **4** 🚨 |
| CAN Interface | Confidentiality, Integrity, Availability | An attacker injects false CAN messages (e.g., spoofing sensor readings, sending malicious control commands) or blocks legitimate messages, causing the vehicle to behave erratically, lose critical functions (e.g., braking, steering), or reveal sensitive operational data. | Severe | *Safety impact dominates: Direct manipulation of CAN messages can compromise fundamental vehicle control systems, leading to severe injury or fatality. Operational impact is also severe. (Category: S, O)* | An attacker gains access to the CAN bus (e.g., via the OBD-II port, a compromised infotainment system, or physical wiretapping) and then exploits the lack of inherent authentication in CAN to inject spoofed messages (Tampering/Spoofing) or flood the bus (Denial of Service). | High | *CAN protocol inherently lacks message authentication, encryption, and source validation. Once network access is achieved (which can be relatively low effort for physical/local access), injection and eavesdropping are straightforward. (STRIDE: Spoofing, Tampering, Denial of Service)* | **5** 🚨 |
| LIN Interface | Confidentiality, Integrity, Availability | An attacker injects false LIN messages (e.g., activating windows, lights) or blocks legitimate LIN messages, causing inconvenience, unexpected behavior of comfort features, or potential distractions to the driver. | Moderate | *Operational impact dominates: Attacks primarily affect comfort features, leading to nuisance or degraded user experience. While minor safety distractions are possible, the direct safety impact is generally low. (Category: O)* | An attacker gains access to the LIN bus (e.g., via physical tap or by compromising an adjacent ECU) and exploits the lack of security in the LIN protocol to send unauthorized messages (Spoofing/Tampering) or disrupt the LIN master's communication (Denial of Service). | High | *Similar to CAN, the LIN protocol lacks inherent security mechanisms (authentication, encryption). Once physical or adjacent network access is gained, injecting or blocking messages is relatively easy. (STRIDE: Spoofing, Tampering, Denial of Service)* | 3 |
| FlexRay Interface | Confidentiality, Integrity, Availability | An attacker injects false FlexRay messages (e.g., erroneous steering commands, braking commands) or disrupts the time-triggered communication, leading to immediate and catastrophic loss of safety-critical vehicle functions. | Severe | *Safety impact dominates: FlexRay is used for highly safety-critical applications. Any compromise of its integrity or availability can lead to a complete loss of vehicle control and severe injury or fatality. (Category: S)* | An attacker, with significant expertise and deep system access (e.g., through a compromised safety-critical ECU), attempts to inject malformed or unauthorized FlexRay frames onto the bus, or causes precise timing violations that disrupt the network's synchronized operation, leading to a denial of service or incorrect control. (Spoofing, Tampering, Denial of Service). | Medium | *While FlexRay offers more intrinsic security (time-triggered, robust error handling) than CAN/LIN, a highly skilled attacker with advanced tools and deep system understanding could still attempt to disrupt it. It requires significant expertise and time. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| Automotive Ethernet Interface | Confidentiality, Integrity, Availability | An attacker intercepts, modifies, or injects Ethernet frames containing sensitive ADAS sensor data, vehicle control commands, or infotainment data, leading to incorrect vehicle decisions, data leakage, or system instability. A DoS attack could shut down critical high-bandwidth links. | Severe | *Safety impact dominates: Direct impact on ADAS/autonomous driving decisions can cause severe accidents. Privacy impact is also severe due to potential disclosure of sensitive data streams. Operational impact is high. (Category: S, P, O)* | An attacker exploits vulnerabilities in network protocols (e.g., ARP spoofing, DHCP manipulation), switch configuration, or a connected ECU to launch man-in-the-middle attacks, inject malicious frames, or perform a denial of service on the Ethernet network. This can be initiated from physical access or a compromised adjacent ECU. (Spoofing, Tampering, Information Disclosure, Denial of Service) | Medium | *Automotive Ethernet inherits standard Ethernet attack vectors, which are well-understood. While automotive implementations include security measures (e.g., MACsec, secure boot), these need to be robustly implemented to resist a skilled attacker. Requires moderate expertise. (STRIDE: Spoofing, Tampering, Information Disclosure, Denial of Service)* | **4** 🚨 |
| CAN Networks | Confidentiality, Integrity, Availability | An attacker floods the CAN network with high-priority messages (Denial of Service) or injects spoofed messages (e.g., false speed, brake pedal state) causing critical ECUs to malfunction or the vehicle to exhibit dangerous behavior. | Severe | *Safety impact dominates: Direct manipulation of CAN network traffic can lead to immediate and severe compromises of vehicle control, potentially resulting in severe injury or fatality. (Category: S)* | An attacker gains access to a CAN network segment (e.g., via OBD-II port, compromised infotainment unit, or physically tapping the bus) and then transmits unauthenticated, malicious CAN messages to control or disrupt vehicle functions. (Spoofing, Tampering, Denial of Service) | High | *The CAN protocol design lacks inherent security features such as message authentication or encryption. Once an attacker has network access, injecting or manipulating messages is relatively straightforward, requiring only basic tools and protocol understanding. (STRIDE: Spoofing, Tampering, Denial of Service)* | **5** 🚨 |
| LIN Networks | Confidentiality, Integrity, Availability | An attacker injects or blocks LIN messages, leading to the erratic operation or failure of comfort features (e.g., windows, mirrors, climate control, interior lights), causing user annoyance or distraction. | Moderate | *Operational impact dominates: Attacks on LIN networks primarily cause inconvenience and degraded user experience due to the loss of non-safety-critical comfort features. Direct safety risks are generally low. (Category: O)* | An attacker gains access to a LIN network (e.g., via physical tap or by compromising a connected ECU) and sends unauthorized LIN messages or disrupts the master/slave communication, causing connected devices to malfunction. (Spoofing, Tampering, Denial of Service) | High | *Similar to CAN, the LIN protocol is designed without built-in security features like authentication or encryption. Once physical or logical access to the network is established, manipulating traffic is relatively simple. (STRIDE: Spoofing, Tampering, Denial of Service)* | 3 |
| FlexRay Networks | Confidentiality, Integrity, Availability | An attacker introduces timing deviations, injects corrupted messages, or performs a denial of service on the FlexRay network, leading to catastrophic failure of safety-critical vehicle functions (e.g., x-by-wire systems). | Severe | *Safety impact dominates: FlexRay networks handle safety-critical, time-deterministic communications. Their compromise leads to an immediate loss of vehicle control, posing an extreme risk of severe injury or fatality. (Category: S)* | An attacker with significant expertise and potentially physical access or deep system compromise attempts to disrupt the synchronized communication or inject carefully crafted malicious frames onto the FlexRay network, exploiting subtle timing vulnerabilities or implementation flaws. (Spoofing, Tampering, Denial of Service) | Medium | *FlexRay's time-triggered design and built-in error handling make it significantly harder to attack than CAN/LIN. However, a highly sophisticated attacker with specialized tools and deep protocol knowledge could still attempt to bypass or disrupt it, requiring substantial resources and expertise. (STRIDE: Tampering, Denial of Service)* | **4** 🚨 |
| Automotive Ethernet Networks | Confidentiality, Integrity, Availability | An attacker performs a denial of service, injects spoofed data (e.g., false sensor readings for ADAS), or intercepts sensitive data (e.g., ADAS camera feeds, infotainment personal data) on the Ethernet network, leading to incorrect autonomous driving decisions, data breaches, or complete system failure. | Severe | *Safety impact dominates: Direct compromise of ADAS/autonomous driving functions can cause severe accidents. Privacy impact is also severe due to the high volume of sensitive data transmitted. Operational impact is critical for advanced features. (Category: S, P, O)* | An attacker exploits vulnerabilities in network protocols (e.g., ARP spoofing, DHCP manipulation), network devices (e.g., switches, ECUs), or software to launch man-in-the-middle attacks, inject malicious frames, flood the network, or eavesdrop on sensitive communications. This could be initiated from a compromised infotainment unit, diagnostic port, or remotely. (Spoofing, Tampering, Information Disclosure, Denial of Service) | Medium | *Automotive Ethernet, while having more built-in security features than CAN/LIN, is susceptible to various standard network attacks. Exploiting these in an automotive context requires moderate expertise and potentially prior access to a connected ECU or network segment. (STRIDE: Spoofing, Tampering, Information Disclosure, Denial of Service)* | **4** 🚨 |
| Gateway Routing Logic | Confidentiality, Integrity, Availability | An attacker modifies the gateway's routing rules, allowing unauthorized messages to pass between otherwise isolated networks (e.g., infotainment to safety-critical CAN), injecting malicious messages into critical domains, or blocking legitimate traffic, leading to vehicle control compromise, data leakage, or system failure. | Severe | *Safety impact dominates: A breach of network segmentation can expose safety-critical systems to malicious input, directly leading to accidents. Operational and privacy impacts are also severe due to systemic compromise and data leakage. (Category: S, O, P)* | An attacker, having compromised the gateway's MCU, exploits a vulnerability in the routing logic's software to alter routing tables or firewall rules. This could lead to a breach of network segmentation, enabling attacks on previously isolated ECUs, or causing a denial of service by misrouting messages. (Tampering, Spoofing, Denial of Service) | Medium | *Requires an initial, successful compromise of the gateway's MCU or management interface. This involves high expertise in firmware analysis and exploit development, but the impact of success is extremely high, making it a valuable target for sophisticated attackers. (STRIDE: Tampering, Spoofing, Denial of Service)* | **4** 🚨 |
| Data Filtering / Firewall | Confidentiality, Integrity, Availability | An attacker disables, bypasses, or reconfigures the data filtering/firewall, allowing malicious messages to reach critical ECUs, enabling unauthorized data exfiltration, or blocking legitimate traffic, leading to system compromise or denial of service. | Severe | *Safety impact dominates: Bypassing the firewall allows malicious messages to directly affect safety-critical systems, leading to severe accidents. Operational and privacy impacts are also severe due to systemic compromise and data leakage. (Category: S, O, P)* | An attacker, having gained control of the gateway's MCU or a privileged process, exploits a vulnerability in the firewall's implementation (e.g., configuration parsing error, buffer overflow, logical flaw) to disable its rules, bypass its checks, or inject new rules that permit malicious traffic. (Tampering, Information Disclosure, Denial of Service) | Medium | *Requires a prior, successful compromise of the gateway's controlling entity and high expertise in security software vulnerabilities. This is a critical security control, so attacking it demands significant skill and resources. (STRIDE: Tampering, Information Disclosure, Denial of Service)* | **4** 🚨 |
| OTA Update Manager | Confidentiality, Integrity, Availability | An attacker introduces malicious firmware updates, corrupts legitimate updates, or causes the update process to fail, leading to permanent system damage (bricking), introduction of malware, prolonged vehicle downtime, or disclosure of sensitive intellectual property. | Severe | *Safety impact dominates: Injection of malicious firmware can lead to unsafe vehicle operation or complete loss of control. Operational impact is severe (bricking, extended downtime). Financial impact is immense due to widespread recalls, and privacy impact is high from IP disclosure. (Category: S, O, F, P)* | An attacker intercepts an OTA update package, modifies it to contain malicious code (Tampering), or substitutes it with an entirely different malicious package (Spoofing). This could involve exploiting vulnerabilities in the update server, communication channels (e.g., insecure TLS), or the vehicle-side OTA Update Manager (e.g., insufficient signature verification, buffer overflows). A DoS attack could prevent critical security updates. (Tampering, Spoofing, Denial of Service, Information Disclosure) | Medium | *OTA update mechanisms are complex and involve multiple components (server, network, client). Exploiting vulnerabilities requires high expertise in cryptography, network protocols, and client-side software. Attacks have high scalability, making them a prime target for skilled adversaries. (STRIDE: Tampering, Spoofing, Denial of Service, Information Disclosure)* | **4** 🚨 |

## 3. Security Goals (Risk Treatment)
**Asset:** MCU/MPU
> The MCU/MPU SHALL prevent unauthorized code execution and maintain the integrity of its firmware and sensitive data.

**Asset:** PMIC
> The PMIC's power regulation settings SHALL be protected from unauthorized manipulation and ensure stable power delivery.

**Asset:** System Basis Chip (SBC)
> The SBC's critical communication transceivers and power supply lines SHALL operate reliably and be protected from unauthorized interference.

**Asset:** CAN Transceiver
> The CAN transceiver SHALL ensure the integrity and authenticity of transmitted and received CAN messages.

**Asset:** FlexRay Transceiver
> The FlexRay transceiver SHALL maintain the integrity and availability of time-triggered communication.

**Asset:** Ethernet PHY
> The Ethernet PHY SHALL ensure reliable and secure data transmission and reception, preventing unauthorized disruption or manipulation.

**Asset:** Ethernet Switch
> The Ethernet switch SHALL enforce network segmentation and ensure the integrity and confidentiality of routing tables and data.

**Asset:** CAN Interface
> The CAN interface SHALL prevent the injection of false messages and ensure the authenticity and integrity of legitimate messages.

**Asset:** LIN Interface
> The LIN interface SHALL prevent unauthorized message injection and ensure the integrity of comfort-related communications.

**Asset:** FlexRay Interface
> The FlexRay interface SHALL ensure the integrity and availability of safety-critical FlexRay messages.

**Asset:** Automotive Ethernet Interface
> The Automotive Ethernet interface SHALL ensure the confidentiality, integrity, and availability of transmitted and received Ethernet frames.

**Asset:** CAN Networks
> The CAN networks SHALL ensure the integrity and authenticity of all messages and prevent denial of service attacks.

**Asset:** LIN Networks
> The LIN networks SHALL prevent unauthorized message injection and ensure the integrity of comfort feature communications.

**Asset:** FlexRay Networks
> The FlexRay networks SHALL maintain the integrity, availability, and time-synchronization of critical communications.

**Asset:** Automotive Ethernet Networks
> The Automotive Ethernet networks SHALL ensure the confidentiality, integrity, and availability of all network traffic and enforce network segmentation.

**Asset:** Gateway Routing Logic
> The Gateway Routing Logic SHALL prevent unauthorized modification of routing rules and enforce secure network segmentation.

**Asset:** Data Filtering / Firewall
> The Data Filtering / Firewall SHALL ensure the integrity and effectiveness of its filtering rules to prevent malicious traffic and unauthorized data exfiltration.

**Asset:** OTA Update Manager
> The OTA Update Manager SHALL ensure the authenticity and integrity of all firmware updates and prevent their unauthorized modification or injection.

## 4. Security Requirements (Engineering Controls)
**Maps to Goal:** The MCU/MPU SHALL prevent unauthorized code execution and maintain the integrity of its firmware and sensitive data.
* **Control:** The MCU/MPU SHALL implement a secure boot process to verify the authenticity and integrity of firmware before execution.
  * **Rationale:** *Secure boot ensures that only trusted and unaltered firmware is loaded and executed, preventing the introduction of malicious code.*

**Maps to Goal:** The MCU/MPU SHALL prevent unauthorized code execution and maintain the integrity of its firmware and sensitive data.
* **Control:** The MCU/MPU SHALL enforce memory protection mechanisms (e.g., MPU/MMU) to prevent unauthorized access and modification of critical memory regions.
  * **Rationale:** *Protects sensitive data and code from unauthorized access by other processes.*

**Maps to Goal:** The MCU/MPU SHALL prevent unauthorized code execution and maintain the integrity of its firmware and sensitive data.
* **Control:** The MCU/MPU SHALL provide hardware-backed root of trust for secure storage of cryptographic keys and sensitive configuration data.
  * **Rationale:** *Ensures the integrity and confidentiality of critical security parameters.*

**Maps to Goal:** The PMIC's power regulation settings SHALL be protected from unauthorized manipulation and ensure stable power delivery.
* **Control:** Access to PMIC configuration registers SHALL be restricted to authenticated and authorized processes only.
  * **Rationale:** *Prevents malicious modification of power settings.*

**Maps to Goal:** The PMIC's power regulation settings SHALL be protected from unauthorized manipulation and ensure stable power delivery.
* **Control:** The PMIC control interface SHALL implement command authentication and integrity checks.
  * **Rationale:** *Ensures that only legitimate commands are executed by the PMIC.*

**Maps to Goal:** The SBC's critical communication transceivers and power supply lines SHALL operate reliably and be protected from unauthorized interference.
* **Control:** The SBC's configuration and control interfaces SHALL be protected with access control mechanisms, limiting modifications to authorized entities.
  * **Rationale:** *Prevents attackers from disabling or reconfiguring critical transceivers or power supply functions.*

**Maps to Goal:** The SBC's critical communication transceivers and power supply lines SHALL operate reliably and be protected from unauthorized interference.
* **Control:** The SBC SHALL implement integrity checks on commands received from the host MCU to prevent malicious manipulation.
  * **Rationale:** *Ensures that commands to the SBC are legitimate and untampered.*

**Maps to Goal:** The CAN transceiver SHALL ensure the integrity and authenticity of transmitted and received CAN messages.
* **Control:** The CAN transceiver SHALL support filtering of invalid or malformed CAN messages.
  * **Rationale:** *Reduces the attack surface by rejecting potentially malicious frames.*

**Maps to Goal:** The CAN transceiver SHALL ensure the integrity and authenticity of transmitted and received CAN messages.
* **Control:** Access to the CAN transceiver's control registers SHALL be restricted to prevent unauthorized manipulation (e.g., forcing error-passive states).
  * **Rationale:** *Prevents an attacker from intentionally disrupting CAN communication.*

**Maps to Goal:** The FlexRay Transceiver SHALL maintain the integrity and availability of time-triggered communication.
* **Control:** The FlexRay transceiver's control interface SHALL implement robust access controls and integrity checks for commands.
  * **Rationale:** *Prevents unauthorized modification of its operational parameters, crucial for time-sensitive communication.*

**Maps to Goal:** The FlexRay Transceiver SHALL maintain the integrity and availability of time-triggered communication.
* **Control:** The FlexRay transceiver SHALL provide status feedback to the host MCU to detect and report any unexpected operational states or errors.
  * **Rationale:** *Allows early detection of potential attacks or malfunctions affecting communication.*

**Maps to Goal:** The Ethernet PHY SHALL ensure reliable and secure data transmission and reception, preventing unauthorized disruption or manipulation.
* **Control:** Access to the Ethernet PHY's Management Data Input/Output (MDIO) interface SHALL be restricted to authorized processes.
  * **Rationale:** *Prevents an attacker from manipulating PHY settings to degrade or disable communication.*

**Maps to Goal:** The Ethernet PHY SHALL ensure reliable and secure data transmission and reception, preventing unauthorized disruption or manipulation.
* **Control:** The host MCU SHALL monitor the status of the Ethernet PHY to detect unexpected operational changes or link disruptions.
  * **Rationale:** *Provides early warning of potential attacks or malfunctions.*

**Maps to Goal:** The Ethernet switch SHALL enforce network segmentation and ensure the integrity and confidentiality of routing tables and data.
* **Control:** The Ethernet switch SHALL implement secure configuration management, requiring authentication and authorization for all changes.
  * **Rationale:** *Prevents unauthorized alteration of VLANs, routing rules, or QoS settings.*

**Maps to Goal:** The Ethernet switch SHALL enforce network segmentation and ensure the integrity and confidentiality of routing tables and data.
* **Control:** The Ethernet switch SHALL support MACsec (Media Access Control Security) or similar link-layer encryption for sensitive communication paths.
  * **Rationale:** *Provides confidentiality and integrity protection for data frames, preventing eavesdropping and tampering.*

**Maps to Goal:** The Ethernet switch SHALL enforce network segmentation and ensure the integrity and confidentiality of routing tables and data.
* **Control:** The Ethernet switch SHALL implement port security mechanisms (e.g., MAC address filtering) to prevent unauthorized devices from connecting.
  * **Rationale:** *Limits the ability of an attacker to introduce rogue devices into the network.*

**Maps to Goal:** The CAN interface SHALL prevent the injection of false messages and ensure the authenticity and integrity of legitimate messages.
* **Control:** The CAN interface SHALL implement a secure on-board communication (SecOC) mechanism to provide cryptographic authentication and integrity protection for safety-critical CAN messages.
  * **Rationale:** *Prevents spoofing and tampering of messages on the CAN bus.*

**Maps to Goal:** The CAN interface SHALL prevent the injection of false messages and ensure the authenticity and integrity of legitimate messages.
* **Control:** The CAN interface SHALL apply message filtering based on sender IDs and message content rules.
  * **Rationale:** *Reduces the attack surface by discarding messages from unauthorized sources or with invalid content.*

**Maps to Goal:** The CAN interface SHALL prevent the injection of false messages and ensure the authenticity and integrity of legitimate messages.
* **Control:** The CAN interface SHALL detect and report bus-off states and other anomalies to the host MCU.
  * **Rationale:** *Enables detection of denial-of-service attacks.*

**Maps to Goal:** The LIN interface SHALL prevent unauthorized message injection and ensure the integrity of comfort-related communications.
* **Control:** The LIN master controller SHALL validate incoming LIN frames for correct checksums and message IDs.
  * **Rationale:** *Detects malformed or unauthorized messages.*

**Maps to Goal:** The LIN interface SHALL prevent unauthorized message injection and ensure the integrity of comfort-related communications.
* **Control:** The LIN master SHALL enforce timing constraints for LIN messages to detect and mitigate bus flooding attempts.
  * **Rationale:** *Prevents denial-of-service attacks by detecting excessive or out-of-sequence messages.*

**Maps to Goal:** The FlexRay interface SHALL ensure the integrity and availability of safety-critical FlexRay messages.
* **Control:** The FlexRay interface SHALL implement cryptographic integrity protection for critical FlexRay frames.
  * **Rationale:** *Protects against message tampering and spoofing.*

**Maps to Goal:** The FlexRay interface SHALL ensure the integrity and availability of safety-critical FlexRay messages.
* **Control:** The FlexRay interface SHALL strictly adhere to the time-triggered protocol to reject any frames that violate timing constraints.
  * **Rationale:** *Prevents disruption of synchronized communication crucial for safety-critical functions.*

**Maps to Goal:** The Automotive Ethernet interface SHALL ensure the confidentiality, integrity, and availability of transmitted and received Ethernet frames.
* **Control:** The Automotive Ethernet interface SHALL support MACsec for link-layer encryption and authentication.
  * **Rationale:** *Provides confidentiality and integrity protection for sensitive data streams.*

**Maps to Goal:** The Automotive Ethernet interface SHALL ensure the confidentiality, integrity, and availability of transmitted and received Ethernet frames.
* **Control:** The interface SHALL implement robust ingress and egress filtering to block unauthorized or malformed frames.
  * **Rationale:** *Prevents injection of malicious traffic and ensures only legitimate data is processed.*

**Maps to Goal:** The CAN networks SHALL ensure the integrity and authenticity of all messages and prevent denial of service attacks.
* **Control:** All ECUs connected to safety-critical CAN networks SHALL implement secure on-board communication (SecOC) for message authentication and integrity.
  * **Rationale:** *Cryptographically protects messages from spoofing and tampering across the network.*

**Maps to Goal:** The CAN networks SHALL ensure the integrity and authenticity of all messages and prevent denial of service attacks.
* **Control:** Network monitoring tools and intrusion detection systems SHALL be deployed to detect unusual traffic patterns or unauthorized messages on the CAN bus.
  * **Rationale:** *Provides early warning and detection of ongoing attacks.*

**Maps to Goal:** The LIN networks SHALL prevent unauthorized message injection and ensure the integrity of comfort feature communications.
* **Control:** LIN master ECUs SHALL validate the consistency and timing of messages received from LIN slave devices.
  * **Rationale:** *Detects attempts to inject false messages or disrupt communication.*

**Maps to Goal:** The LIN networks SHALL prevent unauthorized message injection and ensure the integrity of comfort feature communications.
* **Control:** Measures shall be implemented to prevent unauthorized physical access to LIN bus wiring.
  * **Rationale:** *Reduces the risk of physical wiretapping and direct message injection.*

**Maps to Goal:** The FlexRay networks SHALL maintain the integrity, availability, and time-synchronization of critical communications.
* **Control:** All ECUs participating in FlexRay networks SHALL implement cryptographic integrity protection for safety-critical data.
  * **Rationale:** *Ensures the authenticity and integrity of messages even if the network is compromised.*

**Maps to Goal:** The FlexRay networks SHALL maintain the integrity, availability, and time-synchronization of critical communications.
* **Control:** The FlexRay controller SHALL enforce strict adherence to the time-triggered protocol and reject any frames that do not conform to the predefined schedule.
  * **Rationale:** *Prevents timing attacks and ensures deterministic communication.*

**Maps to Goal:** The Automotive Ethernet networks SHALL ensure the confidentiality, integrity, and availability of all network traffic and enforce network segmentation.
* **Control:** All critical nodes on the Automotive Ethernet network SHALL utilize MACsec (Media Access Control Security) for link-layer encryption and authentication.
  * **Rationale:** *Protects data in transit from eavesdropping and tampering.*

**Maps to Goal:** The Automotive Ethernet networks SHALL ensure the confidentiality, integrity, and availability of all network traffic and enforce network segmentation.
* **Control:** The network architecture SHALL enforce strict VLAN segmentation to isolate different security domains.
  * **Rationale:** *Prevents lateral movement of attackers and restricts access to sensitive network segments.*

**Maps to Goal:** The Automotive Ethernet networks SHALL ensure the confidentiality, integrity, and availability of all network traffic and enforce network segmentation.
* **Control:** An in-vehicle intrusion detection system (IDS) SHALL monitor Ethernet traffic for anomalies, unauthorized protocols, or malicious patterns.
  * **Rationale:** *Detects network-based attacks in real-time.*

**Maps to Goal:** The Gateway Routing Logic SHALL prevent unauthorized modification of routing rules and enforce secure network segmentation.
* **Control:** The gateway's routing configuration SHALL be stored in protected memory and authenticated during boot.
  * **Rationale:** *Ensures that only trusted routing rules are loaded and active.*

**Maps to Goal:** The Gateway Routing Logic SHALL prevent unauthorized modification of routing rules and enforce secure network segmentation.
* **Control:** Access to modify gateway routing rules SHALL be restricted to cryptographically signed and authenticated configuration updates.
  * **Rationale:** *Prevents unauthorized modification of routing behavior by attackers.*

**Maps to Goal:** The Gateway Routing Logic SHALL prevent unauthorized modification of routing rules and enforce secure network segmentation.
* **Control:** The gateway SHALL implement robust firewall rules to enforce segmentation policies and filter traffic between domains.
  * **Rationale:** *Prevents unauthorized communication between isolated networks.*

**Maps to Goal:** The Data Filtering / Firewall SHALL ensure the integrity and effectiveness of its filtering rules to prevent malicious traffic and unauthorized data exfiltration.
* **Control:** The firewall's rule set SHALL be cryptographically signed and verified before activation.
  * **Rationale:** *Ensures the integrity and authenticity of the filtering rules.*

**Maps to Goal:** The Data Filtering / Firewall SHALL ensure the integrity and effectiveness of its filtering rules to prevent malicious traffic and unauthorized data exfiltration.
* **Control:** The firewall software SHALL be designed with a minimal attack surface and regularly audited for vulnerabilities.
  * **Rationale:** *Reduces the likelihood of exploitation to bypass or disable the firewall.*

**Maps to Goal:** The Data Filtering / Firewall SHALL ensure the integrity and effectiveness of its filtering rules to prevent malicious traffic and unauthorized data exfiltration.
* **Control:** The firewall SHALL log and alert on suspicious traffic patterns or attempts to bypass filtering rules.
  * **Rationale:** *Provides detection capabilities for attacks.*

**Maps to Goal:** The OTA Update Manager SHALL ensure the authenticity and integrity of all firmware updates and prevent their unauthorized modification or injection.
* **Control:** All OTA update packages SHALL be cryptographically signed by a trusted authority and verified by the vehicle's OTA Update Manager before installation.
  * **Rationale:** *Ensures that only legitimate and untampered updates are applied.*

**Maps to Goal:** The OTA Update Manager SHALL ensure the authenticity and integrity of all firmware updates and prevent their unauthorized modification or injection.
* **Control:** The OTA update process SHALL include robust rollback mechanisms in case of update failure or corruption.
  * **Rationale:** *Prevents bricking the vehicle and allows recovery from faulty updates.*

**Maps to Goal:** The OTA Update Manager SHALL ensure the authenticity and integrity of all firmware updates and prevent their unauthorized modification or injection.
* **Control:** The communication channel for OTA updates SHALL be secured using TLS 1.3 or equivalent cryptographic protocols.
  * **Rationale:** *Protects updates in transit from eavesdropping and tampering.*

