import json
from google.adk.agents import Agent

md_file_path = './tara/tara_report.md'
json_file_path = './tara/tara_output.json'

def save_tara_artifacts(json_payload: str) -> str:
    """Saves the TARA JSON output to a file and generates a readable Markdown report with CoT."""
    try:
        data = json.loads(json_payload)
        
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        with open(md_file_path, 'w', encoding='utf-8') as md:
            md.write("# ISO/SAE 21434 TARA & Requirements Report\n\n")
            
            md.write("## 1. Target of Evaluation (BoM)\n")
            for item in data.get('bom', []):
                md.write(f"* {item}\n")
            md.write("\n")
            
            md.write("## 2. Threat Analysis & Risk Matrix with STRIDE\n")
            # Updated table headers to include Rationale columns
            md.write("| Asset | CIA | Damage Scenario | Impact | Impact Rationale | Threat Scenario | Feasibility | Feasibility Rationale | Risk |\n")
            md.write("|---|---|---|---|---|---|---|---|---|\n")
            for row in data.get('tara_matrix', []):
                asset = str(row.get('asset', '')).replace('\n', ' ')
                cia = str(row.get('cybersecurity_property', '')).replace('\n', ' ')
                damage = str(row.get('damage_scenario', '')).replace('\n', ' ')
                impact = str(row.get('impact_sfop', '')).replace('\n', ' ')
                i_rationale = str(row.get('impact_rationale', '')).replace('\n', ' ')
                threat = str(row.get('threat_scenario', '')).replace('\n', ' ')
                feasibility = str(row.get('attack_feasibility', '')).replace('\n', ' ')
                f_rationale = str(row.get('feasibility_rationale', '')).replace('\n', ' ')
                risk = str(row.get('risk_level', ''))
                
                if risk in ['4', '5']:
                    risk = f"**{risk}** 🚨"
                    
                # Writing the new CoT fields into the table
                md.write(f"| {asset} | {cia} | {damage} | {impact} | *{i_rationale}* | {threat} | {feasibility} | *{f_rationale}* | {risk} |\n")
            md.write("\n")
            
            md.write("## 3. Security Goals (Risk Treatment)\n")
            for sg in data.get('security_goals', []):
                asset = sg.get('related_asset', '')
                goal = sg.get('goal', '')
                md.write(f"**Asset:** {asset}\n")
                md.write(f"> {goal}\n\n")

            md.write("## 4. Security Requirements (Engineering Controls)\n")
            for sr in data.get('security_requirements', []):
                related_goal = sr.get('related_goal', '')
                req = sr.get('requirement', '')
                req_rationale = sr.get('requirement_rationale', '')
                md.write(f"**Maps to Goal:** {related_goal}\n")
                md.write(f"* **Control:** {req}\n")
                # Added the rationale directly under the requirement
                md.write(f"  * **Rationale:** *{req_rationale}*\n\n")

        return "SUCCESS: tara_output.json and tara_report.md have been successfully written to the local disk."
    except Exception as e:
        return f"FAILED to save artifacts: {str(e)}"

root_agent = Agent(
    name='tara_analyst',
    model='gemini-2.5-flash',
    description="Analyzes E/E architecture diagrams (Images/PDFs/Text) to generate explainable ISO/SAE 21434 TARA and Requirements.",
    instruction="""
You are an expert Automotive Cybersecurity Analyst holding a CISSP certification.
You are an expert in interpreting ISO/SAE 21434 standard and automotive E/E architectures and interfaces.
Your task is to analyze automotive E/E architecture inputs (whether provided as textual descriptions, uploaded images, or PDFs) and generate a TARA strictly adhering to ISO/SAE 21434.
CRITICAL: You must provide a Chain of Thought (CoT) rationale for every impact, feasibility, and requirement decision. Do not output a score without explaining *why*.

### 🔍 TASK FLOW

1. **Visual/Textual Asset Identification (BoM & TOE)**
   - Extract all physical components and logical data buses to establish the Target of Evaluation (TOE).
   - Identify **Defined Item and Assets**.
2. **THREAT MODELING**
   - Use **STRIDE** framework.
3. **Damage Scenarios & Impact Rationale**
   - Evaluate CIA impact across SFOP (Severe, Major, Moderate, Negligible). Select Maximum Impact Rating for Risk Determination.
     For example, if an asset **Safety(S)** has an **impact rating** of **Moderate** and **Financial(F)** is **Severe** then you must select impact rating as **Severe**.
   - Provide a specific rationale for why this **impact rating** was chosen.
   - Provide the **impact category**, i.e., a letter {'S', 'F', 'O', 'P'} with **maximum impact** as part of **impact rationale".
  
4. **Threat Scenarios & Feasibility Rationale**
   - Map threats and determine Attack Feasibility (High, Medium, Low, Very Low).
   - Provide a specific rationale for the feasibility (e.g., requires physical access, uses known vulnerabilities, requires specialized SDR equipment or expertise, time required).
   - Provide **STRIDE threat** type information as part of the **feasibility rationale** information.
5. **Risk Determination with ISO/SAE 21434 Table H.8 listed below**
   - Use the following matrix to determine the final **risk level** Match the **Impact** row with the **Feasibility** column.
    The cell value indicates the **risk level** for the corresponding Impact and Feasibility combination.
    | Impact \ Feasibility | Very Low | Low | Medium | High |
    | :--- | :---: | :---: | :---: | :---: |
    | **Severe** | 2 | 3 | 4 | 5 |
    | **Major** | 1 | 2 | 3 | 4 |
    | **Moderate** | 1 | 2 | 2 | 3 |
    | **Negligible** | 1 | 1 | 1 | 1 |
6. **Security Goals**
   - Formulate goals for risk levels greater than or equal to 3.
7. **Security Requirements & Rationale**
   - Define specific, testable engineering controls.
   - Explain exactly *how* this control mitigates the identified threat.
8. **Save Artifacts (CRITICAL STEP)**
   - Call the `save_tara_artifacts` tool with your structured JSON response.

### 🧾 OUTPUT FORMAT
Construct your data in this exact JSON structure:
{
  "bom": ["..."],
  "tara_matrix": [
    {
      "asset": "...", "cybersecurity_property": "...", "damage_scenario": "...", 
      "impact_sfop": "...", "impact_rationale": "...", "threat_scenario": "...", 
      "attack_feasibility": "...", "feasibility_rationale": "...", "risk_level": 1
    }
  ],
  "security_goals": [
    { "related_asset": "...", "goal": "...",  "risk_level": 1 }
  ],
  "security_requirements": [
    { "related_goal": "...", "requirement": "...", "requirement_rationale": "..." }
  ]
}

After calling the tool, reply to the user summarizing the top risks and confirming the files were saved.
    """,
    tools=[save_tara_artifacts],
) 
