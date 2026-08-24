# input agent: extraction and standardisation of patient data
import json

from langsmith import traceable
from schemas import SMRState


class InputAgent:
    def __init__(self, model):
        self.model = model

    @traceable(name = 'Input Agent', run_type = 'chain')
    def run(self, row):

        raw_medications = (
            row.get('raw_medications')
            or row.get('current_medications')
            or []
        )

        raw_input = f'''
        PATIENT ID: {row['patient_id']}
        AGE: {row['age']}
        SEX: {row['sex']}
        ETHNICITY: {row.get('ethnicity')}

        WEIGHT: {row.get('weight')}
        BMI: {row.get('bmi')}

        SYSTOLIC BP: {row.get('systolic_bp')}
        DIASTOLIC BP: {row.get('diastolic_bp')}

        HBA1C LEVEL: {row.get('hba1c')}
        EGFR LEVEL: {row.get('egfr')}
        CREATININE LEVEL: {row.get('creatinine')}
        TOTAL CHOLESTEROL LEVEL: {row.get('total_cholesterol')}
        LDL CHOLESTEROL LEVEL: {row.get('ldl_cholesterol')}
        POTASSIUM LEVEL: {row.get('potassium')}
        HAEMOGLOBIN LEVEL: {row.get('haemoglobin')}

        SMOKING STATUS: {row.get('smoking_status')}
        ALCOHOL STATUS: {row.get('alcohol_status')}
        
        CONDITIONS: {row.get('conditions', [])}
        
        CURRENT MEDICATIONS: {raw_medications}
        ALLERGIES: {row.get('allergies', [])}
        FRAILTY SCORE: {row.get('frailty_score')}

        FALLS HISTORY: {row.get('falls_history')}
        CLINICAL NOTES: {row.get('clinical_notes')}
        PATIENT CONCERNS: {row.get('patient_concerns', [])}
        '''

        prompt = f'''
        You are the Input Agent in a Structured Medication Review (SMR) pipeline.

        ROLE:
        * Convert raw patient information into a valid SMRState object.
        * Standardise and structure patient information for downstream agents.

        OBJECTIVE:
        * Extract patient information into the PatientRecord.
        * Store the original medication text in patient.raw_medications.
        * Extract each medication into a Medication object.
        * Populate medications.medications.
        * Convert medication frequency abbreviations into clear patient-friendly text.
        * Create a complete SMRState object ready for further processing.

        INPUTS:
        * Raw patient information.
        * SMRState schema.

        REASONING GUIDELINES:
        * Use only information explicitly present in the raw input.
        * Do not infer diagnoses.
        * Do not infer indications.
        * Do not infer medication interactions.
        * Do not infer risks.
        * Do not infer recommendations.
        * Do not infer monitoring requirements.
        * Do not infer deprescribing opportunities.
        * If information is missing, return null.
        * If a list is missing, return an empty list.
        * Conditions must always be represented as a list of strings.
        * Allergies must always be represented as a list of strings.
        * Patient concerns must always be represented as a list of strings.
        * Initialise clinical_evidence using the empty structure required by the schema.
        * Initialise indications using the empty structure required by the schema.
        * Initialise interactions using the empty structure required by the schema.
        * Initialise risks using the empty structure required by the schema.
        * Initialise deprescribing using the empty structure required by the schema.
        * Initialise monitoring using the empty structure required by the schema.
        * Initialise recommendations using the empty structure required by the schema.
        * Do not populate these fields with clinical findings.
        * Do not return null for fields that the schema requires to be objects.
        * All validation fields must remain null.

        MEDICATION EXTRACTION RULES:
        * Extract each documented medication separately.
        * Preserve the documented medication name.
        * Extract dose, frequency, route and start date only when explicitly available.
        * If dose, frequency, route or start date are unavailable, return null.
        * Do not infer a route from the medication name.
        * Do not infer a dose.
        * Do not infer a frequency.
        * Do not infer a start date.
        * Convert abbreviations such as OD, BD, TDS, QDS and PRN into clear text only when present.
        * Do not change the clinical meaning of the documented frequency.

        CLINICAL SAFETY GUIDELINES:
        * Do not create clinical information that is not documented.
        * Do not assume medication doses.
        * Do not assume medication frequencies.
        * Do not assume diagnoses.
        * If information is unavailable, preserve uncertainty rather than making assumptions.

        OUTPUT REQUIREMENTS:
        * Return valid JSON only.
        * Follow the supplied schema exactly.
        * Do not return markdown.
        * Do not return explanations.
        * Do not return reasoning.
        * Do not return the schema itself.
        
        JSON SCHEMA:
        {SMRState.model_json_schema()}

        RAW INPUT:
        {raw_input}
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
            raise ValueError('INPUT AGENT DID NOT RETURN A VALID JSON OBJECT.')

        raw = raw[start:end]
        data = json.loads(raw)

        for field in [
            'clinical_evidence',
            'indications',
            'interactions',
            'risks',
            'deprescribing',
            'monitoring',
            'recommendations',
            'medications_validation',
            'indications_validation',
            'interactions_validation',
            'risks_validation',
            'deprescribing_validation',
            'monitoring_validation',
            'recommendation_validation',
            'final_validation'
        ]:
            if data.get(field) in [None, {}]:
                data.pop(field, None)

        # medication fallback
        if not data.get('medications', {}).get('medications'):

            parsed_medications = []

            for medication in raw_medications:
                parts = medication.split()

                parsed_medications.append({
                    'name': parts[0],
                    'dose': ' '.join(parts[1:3]) if len(parts) >= 3 else None,
                    'frequency': ' '.join(parts[3:]) if len(parts) >= 4 else None,
                    'route': None,
                    'start_date': None
                })

            data['medications'] = {'medications': parsed_medications}

        state = SMRState.model_validate(data)

        return state
