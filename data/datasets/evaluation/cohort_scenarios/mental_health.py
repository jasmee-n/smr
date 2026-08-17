MENTAL_HEALTH_SCENARIOS = [
    
    {
        "scenario_id": "MH_EVAL001",
        "case_type": "positive",
        "target": "serotonergic_polypharmacy",
        "conditions": [
            "Depression",
            "Chronic pain"
        ],
        "description": (
            "Patient receiving multiple serotonergic medications creating a clinically relevant risk of serotonergic adverse effects."
        )
    },

    {
        "scenario_id": "MH_EVAL002",
        "case_type": "positive",
        "target": "excessive_cns_sedation",
        "conditions": [
            "Anxiety",
            "Insomnia"
        ],
        "description": (
            "Patient receiving multiple centrally acting medications creating excessive sedative burden."
        )
    },

    {
        "scenario_id": "MH_EVAL003",
        "case_type": "positive",
        "target": "qt_risk_psychotropic_polypharmacy",
        "conditions": [
            "Depression",
            "Anxiety"
        ],
        "description": (
            "Patient receiving multiple psychotropic medications contributing to a clinically relevant risk of QT prolongation."
        )
    },

    {
        "scenario_id": "MH_EVAL004",
        "case_type": "positive",
        "target": "long_term_sedative_deprescribing",
        "conditions": [
            "Anxiety",
            "Insomnia"
        ],
        "description": (
            "Patient remaining on long-term sedative treatment that represents a clear medication-review and deprescribing opportunity."
        )
    },

    {
        "scenario_id": "MH_EVAL005",
        "case_type": "negative",
        "target": "appropriate_single_antidepressant",
        "conditions": [
            "Depression"
        ],
        "description": (
            "Stable patient receiving appropriate antidepressant treatment without a predefined medication-related problem."
        )
    },

    {
        "scenario_id": "MH_EVAL006",
        "case_type": "negative",
        "target": "appropriate_mental_health_regimen",
        "conditions": [
            "Depression",
            "Anxiety"
        ],
        "description": (
            "Patient receiving an appropriate mental-health medication regimen without a predefined interaction, duplication or excessive CNS burden."
        )
    },

    {
        "scenario_id": "MH_EVAL007",
        "case_type": "negative",
        "target": "stable_psychotropic_monitoring",
        "conditions": [
            "Depression"
        ],
        "description": (
            "Patient receiving long-term psychotropic treatment with appropriate monitoring and no predefined medication-safety problem."
        )
    },

    {
        "scenario_id": "MH_EVAL008",
        "case_type": "boundary",
        "target": "multiple_psychotropics_with_documented_indications",
        "conditions": [
            "Depression",
            "Anxiety"
        ],
        "description": (
            "Patient receiving multiple psychotropic medications where each medication has a documented clinical indication."
        )
    },

    {
        "scenario_id": "MH_EVAL009",
        "case_type": "boundary",
        "target": "sedative_use_with_uncertain_duration",
        "conditions": [
            "Anxiety",
            "Insomnia"
        ],
        "description": (
            "Patient receiving sedative treatment that may warrant deprescribing but where the duration of treatment is insufficiently documented."
        )
    },

    {
        "scenario_id": "MH_EVAL010",
        "case_type": "complex",
        "target": "multiple_psychotropic_medication_problems",
        "conditions": [
            "Depression",
            "Anxiety",
            "Chronic pain",
            "Insomnia"
        ],
        "description": (
            "Complex mental-health polypharmacy case containing multiple simultaneous interaction, sedation and deprescribing-related medication problems."
        )
    }
]