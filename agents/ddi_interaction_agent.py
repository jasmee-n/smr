# ddi interaction agent: identification of drug-drug interactions
import json

from langsmith import traceable
from schemas import SMRState, InteractionsList
from utils import convert_smr_state_to_json

class DDIInteractionAgent:
    def __init__(self, model, clinical_knowledge):
        self.model = model
        self.clinical_knowledge = clinical_knowledge

    @traceable(name = 'DDI Interaction Agent', run_type = 'chain')
    def run(self, state):
        medications = state.medications.medications

        bnf_interactions = self.clinical_knowledge.retrieve_bnf_interactions(medications)

        bnf_tables = self.clinical_knowledge.retrieve_bnf_tables(medications)

        state.clinical_evidence.bnf_interactions = bnf_interactions
        state.clinical_evidence.bnf_tables = bnf_tables

        prompt = f'''
        You are the Drug-Drug Interaction Agent in a Structured Medication Review (SMR) pipeline.

        ROLE:
        * Identify drug-drug interactions using the supplied BNF evidence.
        * Provide a concise clinical explanation for each identified interaction.

        REASONING GUIDELINES:
        * Use only the supplied BNF interaction and table evidence.
        * Only report interactions involving medications currently present in the patient's medication list.
        * Explicit BNF interaction records may be used when both medications are supported by the record.
        * BNF table evidence may be used when two or more current medications are explicitly listed in the same table.
        * For table evidence, the interaction must reflect the shared effect described by that table.
        * Do not associate a medication with a table unless it is explicitly listed in that table.
        * Do not use external pharmacological knowledge.
        * Do not duplicate interactions.
        * Preserve the severity stated in explicit BNF interaction evidence.
        * For BNF table evidence where no severity is provided, use severity = 'moderate'.
        * Return an empty interactions list if no supplied evidence supports an interaction.

        CLINICAL SAFETY GUIDELINES:
        * Do not exaggerate interaction severity.
        * Do not generate treatment recommendations.
        * Do not generate monitoring plans.
        * Do not generate deprescribing recommendations.
        * Only report findings supported by supplied BNF evidence.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the InteractionsList schema exactly.
        * Each interaction must contain drug_a, drug_b, severity, rationale and source.
        * Use source = 'BNF'.
        * Do not return markdown or explanations outside the JSON.

        PERMITTED BNF INTERACTION EVIDENCE:
        {convert_smr_state_to_json(state.clinical_evidence.bnf_interactions)}

        PERMITTED BNF TABLE EVIDENCE:
        {convert_smr_state_to_json(state.clinical_evidence.bnf_tables)}

        MEDICATIONS:
        {state.medications.model_dump_json(indent = 2)}

        JSON SCHEMA:
        {InteractionsList.model_json_schema()}
        '''
        def get_response(prompt_text):
            response = self.model.invoke(prompt_text)

            raw = (
                response.content
                .replace('```json', '')
                .replace('```', '')
                .strip()
            )

            start = raw.find('{')
            end = raw.rfind('}') + 1

            if start == -1 or end == 0:
                raise ValueError('DDI INTERACTION AGENT DID NOT RETURN A VALID JSON OBJECT.')

            return raw[start:end]

        raw = get_response(prompt)

        try:
            data = json.loads(raw)

        except json.JSONDecodeError:
            retry_prompt = prompt + '''

            IMPORTANT:
            * Your previous response contained invalid JSON.
            * Return the answer again as one valid JSON object only.
            * Check all commas, brackets, quotation marks and list separators.
            * Do not include any text outside the JSON object.
            '''
            raw = get_response(retry_prompt)
            data = json.loads(raw)

        if 'interactions' not in data:
            data = {'interactions': []}

        for interaction in data.get('interactions', []):
            if not interaction.get('severity'):
                interaction['severity'] = 'moderate'

        result = InteractionsList.model_validate(data)
        state.interactions = result

        return state
