from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .agents.asset_analyst import asset_analyst
from .agents.stride_analyst import stride_analyst
from .agents.risk_scorer import risk_scorer
from .tools.artifacts import save_tara_artifacts

asset_analyst_tool = AgentTool(agent=asset_analyst)
stride_analyst_tool = AgentTool(agent=stride_analyst)
risk_scorer_tool = AgentTool(agent=risk_scorer)

root_agent = Agent(
    name='tara_orchestrator',
    model='gemini-2.5-flash',
    description=(
        "Orchestrates the full ISO/SAE 21434 TARA pipeline. Calls specialist "
        "agent-tools in sequence, then saves artifacts and summarizes results."
    ),
    instruction="""
You are the TARA Orchestrator for ISO/SAE 21434 compliance analysis.
You have four tools. Call them in this exact order. Do not stop early.

---

**STEP 1 — Call `asset_analyst_tool`**
Request: "Analyze the provided E/E architecture and return the BoM and assets with CIA properties as JSON."
Store the `bom` list and `assets` list from the response.

---

**STEP 2 — Call `stride_analyst_tool`**
Pass the full `assets` JSON from Step 1 in your request:
"Perform STRIDE threat modeling on these assets and return a tara_matrix JSON: [assets JSON]"
Store the `tara_matrix` from the response.

---

**STEP 3 — Call `risk_scorer_tool`**
Pass the full `tara_matrix` JSON from Step 2 in your request:
"Score this tara_matrix using ISO/SAE 21434 Table H.8 and return scored tara_matrix, security_goals, and security_requirements as JSON: [tara_matrix JSON]"
Store the scored `tara_matrix`, `security_goals`, and `security_requirements`.

---

**STEP 4 — Call `save_tara_artifacts`** ⚠️ MANDATORY
Build this JSON string from your stored data and call `save_tara_artifacts` with it:
{
  "bom": [<bom from Step 1>],
  "tara_matrix": [<scored tara_matrix from Step 3>],
  "security_goals": [<security_goals from Step 3>],
  "security_requirements": [<security_requirements from Step 3>]
}

---

**STEP 5 — Reply to the user**
- Total assets analyzed
- Count of High risk (4-5) findings
- Count of Medium risk (3) findings
- Top 3 highest-risk assets with their security goals
- Confirmation that tara_output.json and tara_report.md were saved

### EXTENSIBILITY NOTE (future tools)
- `cve_lookup_tool` — wraps cve_lookup_agent to enrich feasibility (Project 3)
- `guardrail_tool` — wraps guardrail_agent for input validation (Project 5)
""",
    tools=[asset_analyst_tool, stride_analyst_tool, risk_scorer_tool, save_tara_artifacts],
)

