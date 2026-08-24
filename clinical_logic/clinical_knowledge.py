import json
from pathlib import Path

# paths
BASE_PATH = Path('/data/home/bt25094/dissertation/smr pipeline/data/clinical_database')

BNF_PATH = BASE_PATH/ 'bnf_evidence'/ 'bnf_evidence.json'

STOPP_START_PATH = BASE_PATH/ 'stopp_start_evidence'/ 'stopp_start_evidence.json'

# clinical knowledge
class ClinicalKnowledge:
    def __init__(self):
        with BNF_PATH.open('r', encoding='utf-8') as file:
            bnf = json.load(file)

        with STOPP_START_PATH.open('r', encoding='utf-8') as file:
            stopp_start = json.load(file)

        self.bnf_tables = bnf['tables']
        self.bnf_interactions = bnf['interactions']

        self.stopp = [
            criterion
            for criterion in stopp_start
            if criterion['framework'] == 'STOPP'
        ]

        self.start = [
            criterion
            for criterion in stopp_start
            if criterion['framework'] == 'START'
        ]

    # BNF interaction retrieval
    def retrieve_bnf_interactions(self, medications):
        medication_names = [
            medication.name.lower().strip()
            for medication in medications
        ]

        retrieved = []

        for interaction in self.bnf_interactions:
            drug_a = (
                interaction.get('drug_or_class_a')
                or ''
            ).lower()

            drug_b = (
                interaction.get('drug_or_class_b')
                or ''
            ).lower()

            interaction_text = (
                interaction.get('interaction')
                or ''
            ).lower()

            full_text = f'{drug_a} {drug_b} {interaction_text}'

            matched_medications = [
                medication
                for medication in medication_names
                if medication in full_text
            ]

            if len(set(matched_medications)) >= 2:
                retrieved.append({
                    **interaction,
                    'matched_medications': list(
                        set(matched_medications)
                    )
                })

        return retrieved

    # BNF table retrieval
    def retrieve_bnf_tables(self, medications):
        medication_names = [
            medication.name.lower().strip()
            for medication in medications
        ]

        retrieved = []

        for table in self.bnf_tables:
            drugs = [
                drug.lower().strip()
                for drug in table.get('drugs', [])
            ]

            matched_medications = [
                medication
                for medication in medication_names
                if any(
                    medication == drug
                    or medication in drug
                    or drug in medication
                    for drug in drugs
                )
            ]

            if matched_medications:
                retrieved.append({
                    **table,
                    'matched_medications': list(
                        set(matched_medications)
                    )
                })

        return retrieved

    # STOPP guideline retrieval
    def retrieve_stopp(self, state):
        retrieved = []

        for criterion in self.stopp:
            criterion_text = (
                criterion.get('criterion')
                or ''
            ).lower()

            if any(
                medication.name.lower() in criterion_text
                for medication
                in state.medications.medications
            ):
                retrieved.append(criterion)

        return retrieved

    # START guideline retrieval
    def retrieve_start(self, state):
        retrieved = []

        for criterion in self.start:
            criterion_text = (
                criterion.get('criterion')
                or ''
            ).lower()

            if any(
                condition.lower() in criterion_text
                for condition in state.patient.conditions
            ):
                retrieved.append(criterion)

        return retrieved
