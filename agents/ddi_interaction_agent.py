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
    def run(self, state: SMRState):
        medications = state.medications.medications
        
        bnf_interactions = self.clinical_knowledge.retrieve_bnf_interactions(medications)

        bnf_tables = self.clinical_knowledge.retrieve_bnf_tables(medications)

        state.clinical_evidence.bnf_interactions = bnf_interactions
        state.clinical_evidence.bnf_tables = bnf_tables
            
        prompt = f'''
        You are the Drug-Drug Interaction Agent in a Structured Medication Review (SMR) pipeline.
        
        ROLE:
        * Identify and interpret drug-drug interactions using the supplied BNF evidence.
        * Provide a concise clinical explanation for each identified interaction.

        OBJECTIVE:
        * Review the permitted BNF interaction and table evidence for the patient's current medications.
        * Identify interactions supported by the supplied evidence.
        * Preserve severity stated in explicit BNF interaction evidence.
        * Explain the clinical relevance of each interaction using only the supplied evidence.
        * Return the results in the required schema.
    
        REASONING GUIDELINES:
        * Use only the permitted BNF interaction and table evidence.
        * Do not search for or infer interactions using external pharmacological knowledge.
        * Only include interactions involving two medications currently present in the patient's medication list.
        * Confirm that both medications are present before reporting an interaction.
        * Explicit BNF interaction records may be used directly when both current medications are supported by the record.
        * BNF table evidence may be used when both current medications are explicitly listed in the same clinically relevant table.
        * Do not assume that retrieved evidence applies solely because it was retrieved.
        * Do not infer an interaction from a table unless both medications are explicitly present and the table describes a shared clinically relevant effect.
        * Do not duplicate interactions.
        * Preserve severity and uncertainty stated in explicit interaction evidence.
        * If table evidence does not provide an interaction-specific severity, do not invent one.
        * Keep the rationale concise and clinically relevant.
        * Return an empty interactions list if no supplied evidence supports an interaction.
    
        CLINICAL SAFETY GUIDELINES:
        * Do not exaggerate interaction severity.
        * Do not generate treatment recommendations.
        * Do not generate monitoring plans.
        * Do not generate risk assessments.
        * Do not generate deprescribing recommendations.
        * Only report interactions supported by the supplied BNF evidence.
        
        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not modify the SMRState.
        
        For each interaction provide:
        * drug_a
        * drug_b
        * severity
        * rationale
        * source
        
        SOURCE:
        * Use source = 'BNF' for interactions supported by supplied BNF evidence.
        
        PERMITTED BNF INTERACTION EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.bnf_interactions
        )}

        PERMITTED BNF TABLE EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.bnf_tables
        )}
        
        MEDICATIONS:
        {state.medications.model_dump_json(indent = 2)}
        
        JSON SCHEMA:
        {InteractionsList.model_json_schema()}
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
                'DDI INTERACTION AGENT DID NOT RETURN A VALID JSON OBJECT.'
            )
        
        raw = raw[start:end]
        
        result = InteractionsList.model_validate_json(raw)
        state.interactions = result
        
        return state