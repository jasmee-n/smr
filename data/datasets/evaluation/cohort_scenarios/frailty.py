FRAILTY_SCENARIOS = [
    
    {
        "scenario_id": "FRAIL_EVAL001",
        "case_type": "positive",
        "target": "sedative_falls_risk",
        "conditions": [
            "Frailty",
            "Insomnia"
        ],
        "description": (
            "Frail patient receiving sedating medication associated with an increased risk of falls."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL002",
        "case_type": "positive",
        "target": "anticholinergic_burden",
        "conditions": [
            "Frailty",
            "Overactive bladder",
            "Depression"
        ],
        "description": (
            "Frail patient receiving multiple medications contributing to clinically relevant anticholinergic burden."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL003",
        "case_type": "positive",
        "target": "recurrent_falls_medication_risk",
        "conditions": [
            "Frailty",
            "Hypertension",
            "History of falls"
        ],
        "description": (
            "Frail patient with recurrent falls receiving medication that may contribute to further falls risk."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL004",
        "case_type": "positive",
        "target": "benzodiazepine_long_term_use",
        "conditions": [
            "Frailty",
            "Anxiety"
        ],
        "description": (
            "Frail patient receiving long-term benzodiazepine treatment requiring medication review."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL005",
        "case_type": "positive",
        "target": "orthostatic_hypotension_medication_risk",
        "conditions": [
            "Frailty",
            "Hypertension"
        ],
        "description": (
            "Frail patient receiving blood-pressure-lowering treatment contributing to clinically relevant postural hypotension risk."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL006",
        "case_type": "positive",
        "target": "potentially_inappropriate_medication_in_frailty",
        "conditions": [
            "Frailty",
            "Osteoarthritis"
        ],
        "description": (
            "Frail patient receiving a medication with an unfavourable risk-benefit profile requiring medication review."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL007",
        "case_type": "positive",
        "target": "high_cns_medication_burden",
        "conditions": [
            "Frailty",
            "Depression",
            "Chronic pain"
        ],
        "description": (
            "Frail patient receiving multiple centrally acting medications creating excessive CNS and falls-related burden."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL008",
        "case_type": "negative",
        "target": "appropriate_frail_patient_regimen",
        "conditions": [
            "Frailty",
            "Hypertension"
        ],
        "description": (
            "Frail patient receiving an appropriate medication regimen without a predefined high-risk medication-related problem."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL009",
        "case_type": "negative",
        "target": "appropriate_pain_management_in_frailty",
        "conditions": [
            "Frailty",
            "Osteoarthritis"
        ],
        "description": (
            "Frail patient receiving appropriate pain management without a deliberately embedded medication-related problem."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL010",
        "case_type": "negative",
        "target": "stable_frailty_polypharmacy",
        "conditions": [
            "Frailty",
            "Hypertension",
            "Osteoarthritis"
        ],
        "description": (
            "Frail patient receiving several medications without a predefined inappropriate prescribing or medication-safety problem."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL011",
        "case_type": "boundary",
        "target": "low_dose_sedative_without_falls",
        "conditions": [
            "Frailty",
            "Insomnia"
        ],
        "description": (
            "Frail patient receiving low-dose sedating treatment without documented falls or clear medication-related adverse effects."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL012",
        "case_type": "boundary",
        "target": "moderate_anticholinergic_burden",
        "conditions": [
            "Frailty",
            "Overactive bladder"
        ],
        "description": (
            "Frail patient with moderate anticholinergic exposure where the overall clinical significance is uncertain."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL013",
        "case_type": "boundary",
        "target": "deprescribing_competing_benefit",
        "conditions": [
            "Frailty",
            "Ischaemic heart disease"
        ],
        "description": (
            "Frail patient receiving preventive medication that may be considered for deprescribing but continues to provide plausible clinical benefit."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL014",
        "case_type": "boundary",
        "target": "frailty_score_near_risk_threshold",
        "conditions": [
            "Frailty",
            "Hypertension"
        ],
        "description": (
            "Patient with frailty severity close to a threshold where medication-risk interpretation may change."
        )
    },

    {
        "scenario_id": "FRAIL_EVAL015",
        "case_type": "complex",
        "target": "frailty_multiple_medication_risks",
        "conditions": [
            "Frailty",
            "Atrial fibrillation",
            "Osteoarthritis",
            "Depression",
            "History of falls"
        ],
        "description": (
            "Complex frail patient containing multiple simultaneous falls, CNS, interaction and deprescribing-related medication problems."
        )
    }
]