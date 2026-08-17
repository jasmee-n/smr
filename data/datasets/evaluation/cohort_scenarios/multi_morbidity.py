MULTI_MORBIDITY_SCENARIOS = [
    
    {
        "scenario_id": "MULTI_EVAL001",
        "case_type": "positive",
        "target": "medication_without_clear_indication",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with multiple long-term conditions receiving a medication for which no clear current indication is documented."
        )
    },

    {
        "scenario_id": "MULTI_EVAL002",
        "case_type": "positive",
        "target": "therapeutic_duplication",
        "conditions": [
            "Hypertension",
            "Osteoarthritis",
            "Gastro-oesophageal reflux disease"
        ],
        "description": (
            "Patient with multiple long-term conditions receiving unintended duplicate therapy within the medication regimen."
        )
    },

    {
        "scenario_id": "MULTI_EVAL003",
        "case_type": "positive",
        "target": "prescribing_cascade",
        "conditions": [
            "Hypertension",
            "Osteoarthritis",
            "Peripheral oedema"
        ],
        "description": (
            "Patient with a potential prescribing cascade where an adverse effect of one medication is being treated with an additional medication."
        )
    },

    {
        "scenario_id": "MULTI_EVAL004",
        "case_type": "positive",
        "target": "cumulative_adverse_effect_burden",
        "conditions": [
            "Hypertension",
            "Depression",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving multiple medications that contribute to a clinically relevant cumulative adverse-effect burden."
        )
    },

    {
        "scenario_id": "MULTI_EVAL005",
        "case_type": "positive",
        "target": "long_term_medication_no_longer_required",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Gastro-oesophageal reflux disease"
        ],
        "description": (
            "Patient remaining on long-term treatment despite no clear ongoing requirement for the medication."
        )
    },

    {
        "scenario_id": "MULTI_EVAL006",
        "case_type": "positive",
        "target": "monitoring_gap_in_polypharmacy",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving multiple long-term medications where clinically relevant medication monitoring is absent or overdue."
        )
    },

    {
        "scenario_id": "MULTI_EVAL007",
        "case_type": "positive",
        "target": "medication_disease_interaction",
        "conditions": [
            "Hypertension",
            "Heart failure",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving a medication for one condition that may adversely affect another established long-term condition."
        )
    },

    {
        "scenario_id": "MULTI_EVAL008",
        "case_type": "negative",
        "target": "appropriate_multimorbidity_regimen",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with multiple long-term conditions receiving an appropriate medication regimen without a predefined medication-related problem."
        )
    },

    {
        "scenario_id": "MULTI_EVAL009",
        "case_type": "negative",
        "target": "appropriate_high_medication_count",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension",
            "Type 2 diabetes",
            "Gastro-oesophageal reflux disease"
        ],
        "description": (
            "Patient with a high medication count where each medication has an appropriate indication and no deliberately embedded medication-related problem."
        )
    },

    {
        "scenario_id": "MULTI_EVAL010",
        "case_type": "negative",
        "target": "appropriate_multiple_indications",
        "conditions": [
            "Hypertension",
            "Depression",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving multiple medications appropriately prescribed for distinct documented indications."
        )
    },

    {
        "scenario_id": "MULTI_EVAL011",
        "case_type": "negative",
        "target": "stable_multimorbidity_with_monitoring",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Ischaemic heart disease"
        ],
        "description": (
            "Patient with stable multimorbidity receiving appropriate treatment with relevant monitoring information available."
        )
    },

    {
        "scenario_id": "MULTI_EVAL012",
        "case_type": "boundary",
        "target": "uncertain_medication_indication",
        "conditions": [
            "Hypertension",
            "Osteoarthritis",
            "Gastro-oesophageal reflux disease"
        ],
        "description": (
            "Patient receiving a medication with a plausible indication where insufficient clinical information is available to confirm its ongoing appropriateness."
        )
    },

    {
        "scenario_id": "MULTI_EVAL013",
        "case_type": "boundary",
        "target": "potential_deprescribing_with_valid_benefit",
        "conditions": [
            "Hypertension",
            "Ischaemic heart disease",
            "Osteoarthritis"
        ],
        "description": (
            "Patient receiving a medication that may be considered for deprescribing but continues to provide a plausible clinical benefit."
        )
    },

    {
        "scenario_id": "MULTI_EVAL014",
        "case_type": "boundary",
        "target": "treatment_burden_without_clear_inappropriateness",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis",
            "Depression"
        ],
        "description": (
            "Patient with substantial medication burden where no individual medication is clearly inappropriate."
        )
    },

    {
        "scenario_id": "MULTI_EVAL015",
        "case_type": "boundary",
        "target": "incomplete_clinical_information",
        "conditions": [
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Patient with incomplete clinical information where medication appropriateness cannot be confidently determined."
        )
    },

    {
        "scenario_id": "MULTI_EVAL016",
        "case_type": "complex",
        "target": "multiple_medication_review_problems",
        "conditions": [
            "Atrial fibrillation",
            "Hypertension",
            "Type 2 diabetes",
            "Osteoarthritis"
        ],
        "description": (
            "Complex multimorbidity case containing multiple simultaneous medication-related problems involving interactions, monitoring and medication appropriateness."
        )
    },

    {
        "scenario_id": "MULTI_EVAL017",
        "case_type": "complex",
        "target": "multimorbidity_with_renal_impairment",
        "conditions": [
            "Type 2 diabetes",
            "Chronic kidney disease",
            "Hypertension",
            "Osteoarthritis"
        ],
        "description": (
            "Complex multimorbidity case where renal impairment affects several medication safety and prescribing decisions."
        )
    },

    {
        "scenario_id": "MULTI_EVAL018",
        "case_type": "complex",
        "target": "cardiometabolic_polypharmacy",
        "conditions": [
            "Atrial fibrillation",
            "Heart failure",
            "Type 2 diabetes",
            "Hypertension"
        ],
        "description": (
            "Complex cardiometabolic polypharmacy case containing multiple simultaneous medication-related considerations."
        )
    },

    {
        "scenario_id": "MULTI_EVAL019",
        "case_type": "complex",
        "target": "multimorbidity_with_frailty",
        "conditions": [
            "Hypertension",
            "Osteoarthritis",
            "Depression",
            "Atrial fibrillation",
            "Frailty"
        ],
        "description": (
            "Complex multimorbidity case where frailty creates competing medication benefits, risks and deprescribing considerations."
        )
    },

    {
        "scenario_id": "MULTI_EVAL020",
        "case_type": "complex",
        "target": "high_burden_polypharmacy",
        "conditions": [
            "Heart failure",
            "Atrial fibrillation",
            "Type 2 diabetes",
            "Osteoarthritis",
            "Gastro-oesophageal reflux disease"
        ],
        "description": (
            "Patient with high-burden polypharmacy containing multiple simultaneous medication-related problems."
        )
    }
]