# ISO/SAE 21434 TARA Report

## 1. Target of Evaluation (BoM)
* Key Fob Microcontroller: NXP PCF7953
* Key Fob LF Antenna: 125 kHz 3D
* Key Fob UHF Transmitter: 433 MHz
* Key Fob Cryptography: AES-128
* Key Fob Power: CR2032 Battery
* SKM Microcontroller: NXP S32K144
* SKM LF Driver: 125 kHz transmission antenna
* SKM UHF Receiver: 433 MHz
* SKM Network Interface: Texas Instruments TCAN4550
* Vehicle CAN Bus
* Body Control Module (BCM)
* Engine Control Unit (ECU)

## 2. Threat Analysis & Risk Matrix
| Asset | CIA | Damage Scenario | Impact | Threat Scenario | Feasibility | Risk Value |
|---|---|---|---|---|---|---|
| Key Fob AES-128 Key (Hardcoded) | Confidentiality | Unauthorized extraction of the AES-128 key, allowing cloning of the key fob or calculation of valid responses. | Severe | Side-channel attack (e.g., power analysis, electromagnetic analysis) on the Key Fob's NXP PCF7953 MCU to extract the hardcoded AES-128 key. | Medium | **4** 🚨 |
| Key Fob AES-128 Key (Hardcoded) | Integrity | Tampering with the AES-128 key or cryptographic calculations within the Key Fob firmware. | Severe | Physical tampering/reverse engineering of Key Fob to modify firmware or key storage. | Medium | **4** 🚨 |
| SKM LF Driver / Key Fob LF Antenna (LF Communication) | Confidentiality, Integrity | Eavesdropping on LF challenge to gain information about cryptographic process or vehicle status. | Moderate | Attacker uses an LF receiver to capture the 125 kHz challenge signal. | Medium | 3 |
| Key Fob UHF Transmitter / SKM UHF Receiver (UHF Communication) | Integrity, Authenticity | Relay attack where LF challenge and UHF response are relayed over long distances. | Severe | Attacker uses two devices to relay the LF challenge to the key fob and the UHF response back to the vehicle, extending the operational range. | High | **5** 🚨 |
| Key Fob UHF Transmitter / SKM UHF Receiver (UHF Communication) | Availability | Jamming of 433 MHz UHF frequency, preventing Key Fob communication and legitimate access/start. | Moderate | RF jamming using a cheap jammer. | High | 3 |
| SKM Microcontroller (NXP S32K144) | Integrity, Availability | Tampering with SKM firmware, allowing unauthorized validation bypass or control of vehicle functions. | Severe | Physical access and flashing malicious firmware onto the SKM MCU. | Medium | **4** 🚨 |
| Vehicle CAN Bus / BCM / ECU (CAN Frames for Unlock/Start) | Integrity, Authenticity | Spoofing of the unencrypted CAN frame to the BCM to unlock doors or enable engine start. | Severe | Attacker gains physical access to the Vehicle CAN Bus (e.g., via OBD-II port) and injects crafted CAN messages to unlock doors or enable engine start. | Medium | **4** 🚨 |
| Key Fob (CR2032 Battery) | Availability | Battery depletion, rendering the key fob inoperable. | Negligible | Normal wear and tear, or user negligence in replacement. | Very Low | 1 |

## 3. Security Goals (Risk Treatment)
**Asset:** Key Fob AES-128 Key
> The AES-128 key stored in the Key Fob microcontroller shall be protected against unauthorized extraction via side-channel attacks to a very low level of feasibility.

**Asset:** Key Fob AES-128 Key
> The Key Fob firmware and cryptographic calculations shall be protected against unauthorized modification and physical tampering to ensure integrity.

**Asset:** Key Fob UHF Transmitter / SKM UHF Receiver (UHF Communication)
> The PEPS system shall detect and prevent relay attacks to an acceptable level, preventing unauthorized vehicle access and start.

**Asset:** SKM Microcontroller
> The SKM microcontroller's firmware shall be protected against unauthorized modification or flashing to maintain system integrity and prevent bypass of security functions.

**Asset:** Vehicle CAN Bus / BCM / ECU (CAN Frames)
> The CAN frames used for critical functions like unlocking doors and enabling engine start shall be protected against spoofing and unauthorized injection to ensure authenticity and integrity.

