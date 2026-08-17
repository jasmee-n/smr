# monitoring agent: identification of clinically relevant monitoring requirements
import json

from langsmith import traceable
from schemas import SMRState, MonitoringList

from utils import convert_smr_state_to_json

class MonitoringAgent:
    def __init__(self, model, clinical_knowledge):
        self.model = model
        self.clinical_knowledge = clinical_knowledge

    @traceable(name = 'Monitoring Agent', run_type = 'chain')
    def run(self, state: SMRState):

        bnf_tables = self.clinical_knowledge.retrieve_bnf_tables(state.medications.medications)
            
        bnf_interactions = self.clinical_knowledge.retrieve_bnf_interactions(state.medications.medications)
            
        state.clinical_evidence.bnf_tables = bnf_tables
        state.clinical_evidence.bnf_interactions = bnf_interactions
    
        prompt = f'''
        You are the Monitoring Agent in a Structured Medication Review pipeline.

        ROLE:
        * Identify clinically relevant monitoring requirements.
        * Identify monitoring needed to support safe and effective medication use.

        OBJECTIVE:
        * Review the completed SMRState.
        * Review the permitted BNF table and BNF interaction evidence.
        * Identify monitoring requirements associated with:
            * medications
            * documented conditions
            * identified risks
            * documented drug-drug interactions
            * deprescribing opportunities

        Consider:
        * medication monitoring
        * blood tests
        * renal function monitoring
        * liver function monitoring
        * blood pressure monitoring
        * disease monitoring
        * symptom monitoring
        * follow-up reviews
        * adverse effect monitoring

        INPUT:
        * The current SMRState object.
        * Relevant BNF table evidence.
        * Relevant BNF interaction evidence.

        REASONING GUIDELINES:
        * Use only information contained within the SMRState and permitted evidence.
        * Base monitoring requirements on documented medications, conditions, interactions, risks, deprescribing opportunities and supplied BNF evidence.
        * Use BNF evidence only where it applies to the patient's medication or clinical characteristics.
        * Do not assume that retrieved evidence applies solely because it was retrieved.
        * Do not invent diagnoses.
        * Do not invent laboratory values.
        * Do not invent medications.
        * Do not invent risks.
        * Do not invent interactions.
        * Do not invent monitoring requirements that are unsupported by the available evidence.
        * Every monitoring requirement must be supported by the SMRState or permitted evidence.
        * If insufficient evidence exists, do not generate the monitoring requirement.
        * If a monitoring need is plausible but cannot be confirmed, omit it rather than guessing.
        * Do not duplicate the same monitoring requirement using different wording.
        * Where a current laboratory result is available, use it only as documented and do not infer a trend.
        * Where monitoring is linked to a documented interaction, make that link clear in the rationale.
        * Where monitoring is linked to a deprescribing opportunity, make that link clear in the rationale.

        CLINICAL SAFETY GUIDELINES:
        * Prioritise patient safety.
        * Preserve uncertainty where evidence is limited.
        * Monitoring recommendations should support clinician review and decision-making.
        * Do not make definitive clinical decisions.
        * Do not generate deprescribing recommendations.
        * Do not generate new risks or interactions.
        * Do not generate treatment recommendations.
        * Do not assign an urgent timeframe unless urgency is supported by the patient data or permitted evidence.
        * Do not state that monitoring is overdue unless the timing information required to establish this is present.

        For each monitoring requirement provide:
        * medication_or_condition
        * monitoring_required
        * rationale
        * timeframe
        * priority
        * source

        SOURCE ATTRIBUTION RULES:
        * If based solely on the SMRState, source = 'PATIENT DATA'.
        * If supported by supplied BNF table evidence, source = 'BNF'.
        * If supported by supplied BNF interaction evidence, source = 'BNF'.
        * If supported by more than one supplied source, list the sources separated by a semicolon.
        * If the source is uncertain, source = 'UNCLEAR'.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not return reasoning outside the JSON.
        * Do not modify the SMRState.
        * If no monitoring requirements are identified, return an empty monitoring list.
        * The output must be a single JSON object matching the schema.

        PERMITTED BNF TABLE EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.bnf_tables
        )}

        PERMITTED BNF INTERACTION EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.bnf_interactions
        )}

        SMR STATE:
        {convert_smr_state_to_json(state)}

        JSON SCHEMA:
        {MonitoringList.model_json_schema()}
        '''         
        response = self.model.invoke(prompt)

        raw = (
            response.content
            .replace('```json', '')
            .replace('```', '')
            .strip()
        )

        start = raw.find('{')
        end = raw.rfind('}') + 1

        if start == -1 or end == 0:
            raise ValueError(
                'MONITORING AGENT DID NOT RETURN A VALID JSON OBJECT.'
            )

        raw = raw[start:end]

        data = json.loads(raw)

        if 'medication_or_condition' in data:
            data = {
                'monitoring': [data]
            }

        if 'monitoring' not in data:
            data = {
                'monitoring': []
            }

        raw = json.dumps(data)

        result = MonitoringList.model_validate_json(raw)
        state.monitoring = result

        return state