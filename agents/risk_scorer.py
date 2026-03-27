from google.adk.agents import Agent

# ISO/SAE 21434 Table H.8 risk matrix — deterministic lookup
_RISK_MATRIX = {
    ("Severe",     "Very Low"): 2,
    ("Severe",     "Low"):      3,
    ("Severe",     "Medium"):   4,
    ("Severe",     "High"):     5,
    ("Major",      "Very Low"): 1,
    ("Major",      "Low"):      2,
    ("Major",      "Medium"):   3,
    ("Major",      "High"):     4,
    ("Moderate",   "Very Low"): 1,
    ("Moderate",   "Low"):      2,
    ("Moderate",   "Medium"):   2,
    ("Moderate",   "High"):     3,
    ("Negligible", "Very Low"): 1,
    ("Negligible", "Low"):      1,
    ("Negligible", "Medium"):   1,
    ("Negligible", "High"):     1,
}


def calculate_risk(impact: str, feasibility: str) -> int:
    """Deterministically maps impact + feasibility to a risk level per ISO/SAE 21434 Table H.8."""
    impact = impact.strip().capitalize()
    feasibility = feasibility.strip().title()
    return _RISK_MATRIX.get((impact, feasibility), 1)


risk_scorer = Agent(
    name='risk_scorer',
    model='gemini-2.5-flash',
    description=(
        "Applies the ISO/SAE 21434 Table H.8 risk matrix to a TARA matrix, "
        "then formulates Security Goals (for risk >= 3) and actionable Security Requirements."
    ),
    instruction="""
You are an expert Automotive Cybersecurity Risk Engineer specializing in ISO/SAE 21434.
You will receive a JSON object with a `tara_matrix` array.

### YOUR TASK

1. **Risk Determination (Table H.8)**
   - For each row, use the `calculate_risk` tool with the `impact_sfop` and `attack_feasibility` values.
   - Store the integer result as `risk_level`.

2. **Security Goals**
   - For every asset with `risk_level >= 3`, formulate ONE concise security goal.
   - The goal must be measurable and asset-specific (e.g., "The OTA mechanism SHALL verify...").

3. **Security Requirements**
   - For each security goal, define ONE or more specific, testable engineering controls.
   - Each requirement must include a `requirement_rationale` explaining HOW it mitigates the threat.

### OUTPUT FORMAT
Return ONLY a valid JSON object:
```json
{
  "tara_matrix": [
    {
      "asset": "...", "cybersecurity_property": "...", "damage_scenario": "...",
      "impact_sfop": "...", "impact_rationale": "...", "threat_scenario": "...",
      "attack_feasibility": "...", "feasibility_rationale": "...", "risk_level": 4
    }
  ],
  "security_goals": [
    { "related_asset": "...", "goal": "...", "risk_level": 4 }
  ],
  "security_requirements": [
    { "related_goal": "...", "requirement": "...", "requirement_rationale": "..." }
  ]
}
```

Include the full `tara_matrix` (with `risk_level` added) plus `security_goals` and `security_requirements`.
Do NOT output anything outside the JSON block.
""",
    tools=[calculate_risk],
)
