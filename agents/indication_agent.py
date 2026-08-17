# indication agent: identification of indications of each patient's medication
import json

from langsmith import traceable
from schemas import SMRState, IndicationsList

from utils import convert_smr_state_to_json

class IndicationAgent:
    def __init__(self, model, clinical_knowledge):
        self.model = model
        self.clinical_knowledge = clinical_knowledge

    @traceable(name = 'Indication Agent', run_type = 'chain')
    def run(self, state: SMRState):

        bnf_tables = self.clinical_knowledge.retrieve_bnf_tables(state.medications.medications)

        state.clinical_evidence.bnf_tables = bnf_tables

        medication_names = [
            medication.name
            for medication in state.medications.medications
        ]

        prompt = f'''
        You are the Indication Agent in a Structured Medication Review (SMR) pipeline.

        ROLE:
        * Determine the most likely indication for each medication.
        * Link medications to documented conditions where possible.

        OBJECTIVE:
        * Review the patient's medications.
        * Review the patient's documented conditions.
        * Review clinician notes and other information contained within the SMRState.
        * Review the permitted BNF evidence.
        * Identify the most likely indication for each medication.
        * Identify medications where no clear indication can be determined.

        INPUT:
        * The current SMRState object.
        * Relevant BNF table evidence retrieved for the patient.

        REASONING GUIDELINES:
        * Use only information contained within the SMRState and permitted evidence.
        * Use documented conditions and clinician notes when identifying indications.
        * Use BNF evidence only to support links between a medication and a documented condition.
        * Do not use BNF evidence to invent a diagnosis that is not documented.
        * Do not assume that retrieved BNF evidence applies solely because it was retrieved.
        * Do not invent new diagnoses.
        * Do not invent new conditions.
        * Do not infer conditions that are not explicitly documented.
        * If the indication cannot be determined from the available information, return 'unclear'.
        * Every medication should have a corresponding indication entry.
        * Every indication must refer to a medication currently present in medications.medications.
        * medication_name must exactly match one of the supplied medication names.
        * medication_name must never be null or empty.
        * If more than one documented condition could explain a medication, select the best-supported indication and acknowledge uncertainty in the rationale.
        * If a medication has no documented condition that reasonably supports its use, return indication = 'unclear'.
        * Do not identify potential prescribing omissions in this stage.

        SOURCE ATTRIBUTION RULES:
        * If the indication is supported directly by a documented condition or clinician note, source = 'PATIENT DATA'.
        * If the documented condition-to-medication link is supported by the supplied BNF evidence, source = 'BNF'.
        * If the indication cannot be established, source = 'UNCLEAR'.
        * Do not cite BNF unless the supporting evidence appears in the permitted BNF evidence.

        CLINICAL SAFETY GUIDELINES:
        * Preserve uncertainty when evidence is insufficient.
        * Do not make assumptions about undocumented diagnoses.
        * Do not use external patient information.
        * If evidence is weak or absent, return 'unclear' rather than guessing.
        * Do not present a common medication use as the patient's indication unless the corresponding condition is documented.
        * Do not recommend starting, stopping or changing medication.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not generate risks.
        * Do not generate interactions.
        * Do not generate recommendations.
        * Do not generate prescribing omissions.
        * Do not modify the SMRState.

        CURRENT MEDICATION NAMES:
        {medication_names}

        PERMITTED BNF EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.bnf_tables
        )}

        PATIENT:
        {convert_smr_state_to_json(state.patient)}

        MEDICATIONS:
        {convert_smr_state_to_json(state.medications)}

        JSON SCHEMA:
        {IndicationsList.model_json_schema()}
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
                'INDICATION AGENT DID NOT RETURN A VALID JSON OBJECT.'
            )

        raw = raw[start:end]
        data = json.loads(raw)

        indications = data.get('indications', [])

        if len(indications) == len(medication_names):
            for index, indication in enumerate(indications):
                if not indication.get('medication_name'):
                    indication['medication_name'] = medication_names[index]

        result = IndicationsList.model_validate(data)

        state.indications = result

        return state