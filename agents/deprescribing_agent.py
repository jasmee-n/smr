# deprescribing agent: identification of medications that could be discontinued
import json

from langsmith import traceable
from schemas import SMRState, DeprescribingList

from utils import convert_smr_state_to_json

class DeprescribingAgent:
    def __init__(self, model, clinical_knowledge):
        self.model = model
        self.clinical_knowledge = clinical_knowledge

    @traceable(name = 'Deprescribing Agent', run_type = 'chain')
    def run(self, state):

        stopp_evidence = self.clinical_knowledge.retrieve_stopp(state)

        bnf_tables = self.clinical_knowledge.retrieve_bnf_tables(state.medications.medications)

        state.clinical_evidence.stopp = stopp_evidence
        state.clinical_evidence.bnf_tables = bnf_tables

        prompt = f'''
        You are the Deprescribing Agent in a Structured Medication Review pipeline.

        ROLE:
        * Identify potential deprescribing opportunities.
        * Identify medicines that may require review, dose reduction, switching or discontinuation.

        OBJECTIVE:
        * Review the completed SMRState.
        * Review the permitted STOPP criteria and BNF table evidence.
        * Assess the appropriateness of the current medication regimen.

        Consider:
        * duplicate therapy
        * medicines without clear indication
        * inappropriate long-term use
        * high-risk medicines
        * frailty
        * renal impairment
        * falls risk
        * anticholinergic burden
        * documented medication-related risks
        * documented drug-drug interactions

        REASONING GUIDELINES:
        * Use only information contained within the SMRState and permitted evidence.
        * Base deprescribing opportunities on documented medications, indications, interactions and risks.
        * Use STOPP criteria only when the patient and medication information satisfy the criterion.
        * Use BNF table evidence only when it applies to the patient's medication or clinical characteristics.
        * Do not assume that retrieved evidence applies solely because it was retrieved.
        * Do not invent diagnoses.
        * Do not invent indications.
        * Do not invent interactions.
        * Do not invent risks.
        * Do not invent monitoring requirements.
        * Do not assume that a medicine should be stopped solely because it has risks.
        * Every deprescribing opportunity must refer to a medication currently present in medications.medications.
        * Every deprescribing opportunity must be supported by the SMRState, STOPP evidence or BNF evidence.
        * A medication with an unclear indication may be flagged for indication review, but this alone does not prove that it should be discontinued.
        * If insufficient evidence exists, do not generate a deprescribing opportunity.
        * Do not duplicate the same deprescribing opportunity using different wording.

        CLINICAL SAFETY GUIDELINES:
        * Prioritise patient safety.
        * Preserve uncertainty where evidence is limited.
        * Do not make definitive prescribing decisions.
        * Do not state that a medication must be stopped.
        * Phrase outputs as recommendations for clinician review.
        * Consider the balance between medication benefit and potential harm.
        * Do not recommend abrupt discontinuation unless explicitly supported by the permitted evidence.
        * Where withdrawal or dose reduction may require tapering, state that clinician-led tapering review may be required.
        * Do not generate monitoring plans.
        * Do not generate new risks or interactions.

        For each deprescribing opportunity provide:
        * medication
        * issue
        * rationale
        * suggested_action
        * priority
        * source

        SOURCE ATTRIBUTION RULES:
        * If based solely on the SMRState, source = 'PATIENT DATA'.
        * If supported by a supplied STOPP criterion, source = 'STOPP'.
        * If supported by supplied BNF evidence, source = 'BNF'.
        * If supported by more than one supplied source, list the sources separated by a semicolon.
        * If the source is uncertain, source = 'UNCLEAR'.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not modify the SMRState.
        * If no deprescribing opportunities are identified, return an empty deprescribing list.

        PERMITTED STOPP EVIDENCE:
        {convert_smr_state_to_json(state.clinical_evidence.stopp)}

        PERMITTED BNF TABLE EVIDENCE:
        {convert_smr_state_to_json(state.clinical_evidence.bnf_tables)}

        SMR STATE:
        {convert_smr_state_to_json(state)}

        JSON SCHEMA:
        {DeprescribingList.model_json_schema()}
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
            raise ValueError('DEPRESCRIBING AGENT DID NOT RETURN A VALID JSON OBJECT.')

        raw = raw[start:end]

        data = json.loads(raw)

        if 'medication' in data:
            data = {'deprescribing': [data]}

        if 'deprescribing' not in data:
            data = {'deprescribing': []}
        raw = json.dumps(data)

        result = DeprescribingList.model_validate_json(raw)
        state.deprescribing = result

        return state
