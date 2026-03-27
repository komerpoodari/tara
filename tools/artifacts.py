import json

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
                md.write(f"  * **Rationale:** *{req_rationale}*\n\n")

        return "SUCCESS: tara_output.json and tara_report.md have been successfully written to the local disk."
    except Exception as e:
        return f"FAILED to save artifacts: {str(e)}"
