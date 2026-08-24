# safety validator agent: checks that outputs are not hallucinations
import json

from langsmith import traceable
from schemas import SMRState, ValidationResult
from typing import Any, Optional

from utils import convert_smr_state_to_json

class SafetyValidatorAgent:
    def __init__(self, model):
        self.model = model

        self.validation_mapping = {
            'medications': 'medications_validation',
            'indications': 'indications_validation',
            'interactions': 'interactions_validation',
            'risks': 'risks_validation',
            'deprescribing': 'deprescribing_validation',
            'monitoring': 'monitoring_validation',
            'recommendations': 'recommendation_validation',
            'summary': 'final_validation'
        }


    @traceable(name = 'Safety Validator Agent', run_type = 'chain')
    def run(self, state, stage, stage_output, validation_rules = '', evidence: Optional[Any] = None):
        stage = stage.strip().lower()

        if stage not in self.validation_mapping:
            raise ValueError(
                f'UNKNOWN VALIDATION STAGE: {stage}. '
                f'EXPECTED STAGES: {sorted(self.validation_mapping)}'
            )

        prompt = f'''
        You are the Safety Validator Agent in a Structured Medication Review
        (SMR) pipeline.

        ROLE:
        * Validate the output produced by the previous pipeline agent.
        * Check whether the output contains hallucinated, unsupported,
          contradictory, patient-inconsistent or clinically unsafe claims.
        * Do not generate new clinical findings.
        * Do not generate new recommendations.
        * Do not rewrite the stage output.

        VALIDATION OBJECTIVE:
        * Determine whether the stage output is grounded in the permitted
          evidence.
        * Determine whether the stage output is consistent with the patient
          record.
        * Determine whether the stage output is clinically safe.
        * Determine whether important missing information or uncertainty has
          been acknowledged.
        * Determine whether severity and priority labels are supported.

        REASONING GUIDELINES:
        * Use only the current SMRState, the stage output and the permitted
          evidence.
        * Do not use unstated general clinical knowledge.
        * Do not invent diagnoses.
        * Do not invent conditions.
        * Do not invent medications.
        * Do not invent laboratory values.
        * Do not invent indications.
        * Do not invent interactions.
        * Do not invent risks.
        * Do not invent monitoring requirements.
        * Do not invent deprescribing opportunities.
        * Do not assume that retrieved evidence applies to the patient merely
          because it was retrieved.
        * A claim is supported only when both the patient data and the supplied
          evidence support it.
        * Do not mark a claim as grounded merely because it appears clinically
          plausible.
        * Preserve uncertainty where evidence is incomplete.
        * Flag claims that are expressed with unjustified certainty.
        * Flag source references that do not correspond to the permitted
          evidence.
        * Flag contradictions with the patient record or earlier findings.
        * Flag severity labels that do not match the source evidence.
        * Flag recommendations that state a medication must be started,
          stopped, increased or reduced without clinician review.
        * Flag unsafe recommendations.
        * Flag missing information when a conclusion depends on unavailable
          patient data.

        STATUS DEFINITIONS:
        * passed:
            * no material validation issues are identified
        * passed_with_warnings:
            * the output is broadly usable but contains minor uncertainty,
              missing information or unsupported wording
        * failed:
            * the output contains serious unsupported, contradictory or unsafe
              claims

        ISSUE TYPE DEFINITIONS:
        * unsupported_claim:
            * the claim is not supported by the patient data or permitted
              evidence
        * patient_mismatch:
            * the claim conflicts with the patient record
        * missing_information:
            * important patient information is unavailable
        * unsafe_recommendation:
            * the proposed action may be unsafe or excessively definitive
        * severity_mismatch:
            * the stated severity is not supported by the evidence
        * contradiction:
            * the claim conflicts with another finding or part of the state
        * uncertainty_not_acknowledged:
            * uncertainty exists but the output presents the claim as certain
        * other:
            * another validation concern not covered above

        STAGE:
        {stage}

        STAGE OUTPUT:
        {convert_smr_state_to_json(stage_output)}

        PERMITTED EVIDENCE:
        {convert_smr_state_to_json(evidence)}

        STAGE-SPECIFIC VALIDATION RULES:
        {validation_rules or 'NO ADDITIONAL STAGE-SPECIFIC RULES SUPPLIED.'}

        CURRENT SMR STATE:
        {convert_smr_state_to_json(state)}

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied ValidationResult schema exactly.
        * The stage field must equal "{stage}".
        * summary is required and must contain a short validation summary.
        * Do not return markdown.
        * Do not return explanations outside the JSON.
        * Do not modify the SMRState.
        * Do not generate replacement findings.
        * If no issues are identified, return an empty issues list.

        JSON SCHEMA:
        {ValidationResult.model_json_schema()}
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
            raise ValueError('SAFETY VALIDATOR DID NOT RETURN A VALID JSON OBJECT.')

        raw = raw[start:end]
        data = json.loads(raw)

        # formatting fallback only
        if not data.get('stage'):
            data['stage'] = stage

        if not data.get('summary'):
            data['summary'] = 'VALIDATION COMPLETE.'

        result = ValidationResult.model_validate(data)

        if result.stage.strip().lower() != stage:
            result.stage = stage

        self.store_validation_result(state, stage, result)

        return state


    def store_validation_result(self, state, stage, result):
        validation_field = self.validation_mapping[stage]
        setattr(state, validation_field, result)
