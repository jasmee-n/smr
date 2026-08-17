# recommendation agent: smr recommendations in order of priorities
import json

from langsmith import traceable
from schemas import SMRState, RecommendationsList

from utils import convert_smr_state_to_json

class RecommendationAgent:
    def __init__(self, model, clinical_knowledge):
        self.model = model
        self.clinical_knowledge = clinical_knowledge

    @traceable(name = 'Recommendation Agent', run_type = 'chain')
    def run(self, state: SMRState):

        start_evidence = self.clinical_knowledge.retrieve_start(state)

        state.clinical_evidence.start = start_evidence

        prompt = f'''
        You are the Recommendation Agent in a Structured Medication Review (SMR) pipeline.

        ROLE:
        * Generate clinically relevant and prioritised recommendations.
        * Synthesise findings produced by previous agents into actionable recommendations for clinician review.
        * Identify potential prescribing omissions supported by the permitted START criteria.

        OBJECTIVE:
        * Review the completed SMRState.
        * Review the permitted START criteria.
        * Generate recommendations based on:
            * identified indications
            * identified drug-drug interactions
            * identified medication-related risks
            * deprescribing opportunities
            * monitoring requirements
            * applicable START criteria
            * patient concerns
            * clinician notes
        * Prioritise recommendations according to clinical significance and potential impact on patient safety.

        INPUT:
        * The current SMRState object.
        * Relevant START criteria.

        REASONING GUIDELINES:
        * Use only information contained within the SMRState and permitted evidence.
        * Base recommendations on findings already identified by previous agents.
        * Recommendations should be derived from:
            * indications
            * interactions
            * risks
            * deprescribing opportunities
            * monitoring requirements
            * applicable START criteria
        * Use START criteria only when the documented patient information satisfies the criterion.
        * Do not assume that a START criterion applies solely because it was retrieved.
        * Confirm that the relevant condition or patient factor is documented.
        * Check whether the medicine or treatment described by the START criterion is already present before identifying a prescribing omission.
        * Do not recommend duplicate treatment.
        * Do not invent new diagnoses.
        * Do not invent new conditions.
        * Do not invent new indications.
        * Do not invent new interactions.
        * Do not invent new risks.
        * Do not invent new monitoring requirements.
        * Do not invent new deprescribing opportunities.
        * Every recommendation must be supported by the SMRState or permitted START evidence.
        * Recommendations should be specific, clinically relevant and actionable.
        * If insufficient evidence exists to support a recommendation, do not generate it.
        * Do not duplicate recommendations that describe the same clinical action.

        CLINICAL SAFETY GUIDELINES:
        * Prioritise patient safety.
        * High-priority recommendations should reflect potentially significant patient harm if not addressed.
        * Preserve uncertainty when evidence is limited.
        * Do not make definitive prescribing decisions.
        * Do not state that a medication must be started, stopped, increased or reduced.
        * Phrase recommendations as actions for clinician review.
        * Where a recommendation originates from a deprescribing opportunity, reference the associated deprescribing finding.
        * Where a recommendation originates from a monitoring requirement, reference the associated monitoring finding.
        * Where a recommendation originates from a START criterion, reference the applicable START criterion in the rationale.
        * Do not generate recommendations that contradict identified risks, deprescribing opportunities or monitoring requirements.
        * Do not assign high or critical priority unless supported by the patient-specific findings.
        * Do not recommend starting treatment where contraindications, allergies or important safety information are unresolved.

        For each recommendation provide:
        * recommendation
        * rationale
        * priority
        * source

        SOURCE ATTRIBUTION RULES:
        * If based solely on findings contained within the SMRState, source = 'PATIENT DATA'.
        * If supported by a supplied START criterion, source = 'START'.
        * If based on findings supported by BNF evidence, preserve the source stated in the relevant finding.
        * If supported by more than one source, list the sources separated by a semicolon.
        * If the source is uncertain, source = 'UNCLEAR'.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not return reasoning outside the JSON.
        * Do not modify the SMRState.
        * If no recommendations are supported by the available evidence, return an empty recommendations list.

        PERMITTED START EVIDENCE:
        {convert_smr_state_to_json(
            state.clinical_evidence.start
        )}

        SMR STATE:
        {convert_smr_state_to_json(state)}

        JSON SCHEMA:
        {RecommendationsList.model_json_schema()}
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
                'RECOMMENDATION AGENT DID NOT RETURN A VALID JSON OBJECT.'
            )

        raw = raw[start:end]

        data = json.loads(raw)

        if 'recommendation' in data:
            data = {
                'recommendations': [data]
            }

        if 'recommendations' not in data:
            data = {
                'recommendations': []
            }

        raw = json.dumps(data)

        result = RecommendationsList.model_validate_json(raw)

        state.recommendations = result

        return state