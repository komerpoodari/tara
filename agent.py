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
            
        with open(md_file_path, 'w') as md:
            md.write("# ISO/SAE 21434 TARA & Requirements Report\n\n")
            
            md.write("## 1. Target of Evaluation (BoM)\n")
            for item in data.get('bom', []):
                md.write(f"* {item}\n")
            md.write("\n")
            
            md.write("## 2. Threat Analysis & Risk Matrix\n")
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
                risk = str(row.get('risk_value', ''))
                
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
Your task is to analyze automotive E/E architecture inputs (whether provided as textual descriptions, uploaded images, or PDFs) and generate a TARA strictly adhering to ISO/SAE 21434.
CRITICAL: You must provide a Chain of Thought (CoT) rationale for every impact, feasibility, and requirement decision. Do not output a score without explaining *why*.

### 🔍 TASK FLOW

1. **Visual/Textual Asset Identification (BoM & TOE)**
   - Extract all physical components and logical data buses to establish the Target of Evaluation (TOE).
2. **Damage Scenarios & Impact Rationale**
   - Evaluate CIA impact across SFOP (Severe, Major, Moderate, Negligible).
   - Provide a specific engineering or safety rationale for why this impact level was chosen.
3. **Threat Scenarios & Feasibility Rationale**
   - Map threats and determine Attack Feasibility (High, Medium, Low, Very Low).
   - Provide a specific rationale for the feasibility (e.g., requires physical access, uses known vulnerabilities, requires specialized SDR equipment).
4. **Risk Determination**
   - Assign Risk Value (1 to 5).
5. **Security Goals**
   - Formulate goals for High Risk (4 or 5) scenarios.
6. **Security Requirements & Rationale**
   - Define specific, testable engineering controls.
   - Explain exactly *how* this control mitigates the identified threat.
7. **Save Artifacts (CRITICAL STEP)**
   - Call the `save_tara_artifacts` tool with your structured JSON response.

### 🧾 OUTPUT FORMAT
Construct your data in this exact JSON structure:
{
  "bom": ["..."],
  "tara_matrix": [
    {
      "asset": "...", "cybersecurity_property": "...", "damage_scenario": "...", 
      "impact_sfop": "...", "impact_rationale": "...", "threat_scenario": "...", 
      "attack_feasibility": "...", "feasibility_rationale": "...", "risk_value": 1
    }
  ],
  "security_goals": [
    { "related_asset": "...", "goal": "..." }
  ],
  "security_requirements": [
    { "related_goal": "...", "requirement": "...", "requirement_rationale": "..." }
  ]
}

After calling the tool, reply to the user summarizing the top risks and confirming the files were saved.
    """,
    tools=[save_tara_artifacts],
)