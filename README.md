# Multi-Agent Pipeline for Structured Medication Reviews Using a Large Language Model

A multi-agent pipeline that uses a **Large Language Model (LLM)** and structured clinical knowledge to perform components of a **Structured Medication Review (SMR)**.

This project was developed as part of an **MSc Bioinformatics dissertation**. It investigates whether decomposing an SMR into specialised LLM-based agents can support structured medication review while integrating external clinical evidence and stage-specific validation.

The pipeline assesses medication indications, drug–drug interactions, patient-specific risks, deprescribing considerations, monitoring requirements and recommendations before integrating the findings into a final SMR report.

The system was evaluated using a purpose-built cohort of **100 synthetic patients** with a predefined reference standard.

> **Important:** This repository is an academic research prototype. It is not a validated clinical decision-support system or medical device and must not be used to make decisions about real patients.

---

## Contents

* [Project Overview](#project-overview)
* [Objectives](#objectives)
* [Pipeline Architecture](#pipeline-architecture)
* [Pipeline Agents](#pipeline-agents)
* [Safety Validation](#safety-validation)
* [Clinical Knowledge Base](#clinical-knowledge-base)
* [Repository Structure](#repository-structure)
* [Technology Stack](#technology-stack)
* [Installation](#installation)
* [Configuration](#configuration)
* [Model Configuration](#model-configuration)
* [Running the Pipeline](#running-the-pipeline)
* [Synthetic Patient Dataset](#synthetic-patient-dataset)
* [Evaluation Design](#evaluation-design)
* [Evaluation Metrics](#evaluation-metrics)
* [Results](#results)
* [Figures](#figures)
* [Reproducibility](#reproducibility)
* [Limitations](#limitations)
* [Future Work](#future-work)
* [Clinical Disclaimer](#clinical-disclaimer)

---

## Project Overview

Structured Medication Reviews require multiple aspects of a patient's medication regimen to be considered together.

These include:

* whether medications have appropriate indications
* whether clinically significant drug–drug interactions are present
* whether patient characteristics increase medication-related risk
* whether medications may warrant deprescribing consideration
* whether additional clinical or laboratory monitoring is required
* what recommendations should follow from the identified findings

These tasks are interdependent and can require information from several clinical knowledge sources.

Instead of asking a single LLM to perform the entire medication review within one prompt, this project uses a **multi-agent architecture**.

The SMR is decomposed into specialised stages, with each agent responsible for a defined component of the review.

Structured clinical evidence from the **British National Formulary (BNF)** and **STOPP/START Version 3 criteria** is incorporated into relevant stages to supplement the LLM's internal knowledge.

A shared **Safety Validator Agent** is additionally used between stages to assess generated findings before they propagate through the remainder of the pipeline.

The overall approach can therefore be summarised as:

```text
Patient Data
      │
      ▼
Specialised LLM Agents
      │
      ├──────── Structured Clinical Evidence
      │             BNF
      │         STOPP / START
      │
      ▼
Stage-Specific Validation
      │
      ▼
Integrated SMR Report
```

---

## Objectives

The project aimed to:

1. Develop a modular multi-agent pipeline for Structured Medication Reviews.
2. Decompose the SMR into specialised clinical reasoning tasks.
3. Incorporate structured external clinical evidence into relevant stages.
4. Use structured schemas to improve consistency between LLM agents.
5. Introduce stage-specific validation of generated clinical findings.
6. Develop a reproducible synthetic patient cohort for pipeline evaluation.
7. Evaluate individual pipeline components rather than relying solely on an overall performance measure.
8. Examine the strengths and limitations of LLM-based multi-agent systems for medication review.

---

## Pipeline Architecture

The final pipeline follows a sequential multi-agent architecture.

```text
                         ┌─────────────────────┐
                         │    Patient Record   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Input Agent     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Indication Agent   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │ DDI Interaction Agent       │
                    │ + BNF Interaction Evidence  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │ Risk Agent                  │
                    │ + BNF / STOPP / START       │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                       ┌────────────────────────┐
                       │  Deprescribing Agent   │
                       └────────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   Monitoring Agent    │
                        └───────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                      ┌─────────────────────────┐
                      │  Recommendation Agent   │
                      └─────────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Safety Validator   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Summary Agent    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Final SMR Report   │
                         └─────────────────────┘
```

Each stage contributes to a shared structured patient state.

The state contains information relating to:

```text
patient
medications
indications
interactions
risks
deprescribing
monitoring
recommendations
overview
conclusion
```

This allows downstream agents to operate using findings generated earlier in the medication review.

---

## Pipeline Agents

### 1. Input Agent

The Input Agent processes the original patient record and prepares a structured representation for downstream analysis.

Patient information can include:

* demographics
* medical conditions
* medications
* clinical observations
* laboratory results
* frailty
* falls history
* smoking status
* alcohol status

The purpose of this stage is to establish a consistent patient representation before medication assessment begins.

### 2. Indication Agent

The Indication Agent assesses the relationship between medications and documented clinical conditions.

For each medication, the agent attempts to identify its likely clinical indication and determine whether this is supported by the patient's medical history.

For evaluation, predicted indications are compared against predefined expected and acceptable indications.

### 3. DDI Interaction Agent

The Drug–Drug Interaction Agent identifies potential clinically relevant interactions between medications in the patient's medication list.

The final agent is supported by structured interaction evidence extracted from the **British National Formulary** rather than relying solely on the LLM's internal knowledge.

Retrieved interaction information can include:

* interacting medications
* interaction description
* severity
* evidence classification
* recommended action
* BNF table reference

Interaction severity was normalised into:

```text
SEVERE
MODERATE
MILD
```

Evidence classifications include:

```text
STUDY
THEORETICAL
ANECDOTAL
```

Potential actions include:

```text
AVOID
MONITOR
ADJUST
```

The extracted BNF interaction database contains approximately **13,385 interaction records**.

### 4. Risk Agent

The Risk Agent evaluates broader medication-related risks that cannot necessarily be represented as simple medication pairs.

The assessment can incorporate:

* medication combinations
* diagnoses
* age
* renal function
* laboratory results
* frailty
* falls history
* other patient-specific characteristics

Relevant BNF and STOPP/START evidence is retrieved through the clinical knowledge base.

The Risk Agent focuses on identifying and prioritising risks. Recommendation generation is intentionally handled separately.

### 5. Deprescribing Agent

The Deprescribing Agent identifies medications that may warrant review for possible deprescribing.

The agent considers the accumulated patient state and identifies treatment that may require reconsideration.

Its output represents **deprescribing considerations** rather than instructions to automatically discontinue medication.

### 6. Monitoring Agent

The Monitoring Agent identifies potential monitoring requirements associated with the patient's medication regimen and clinical findings.

Monitoring may relate to:

* renal function
* electrolytes
* blood pressure
* cardiovascular parameters
* medication adverse effects
* relevant laboratory investigations

### 7. Recommendation Agent

The Recommendation Agent generates potential actions based on findings accumulated throughout the previous stages.

Separating recommendation generation from initial risk identification allows this stage to use information from:

* indication assessment
* drug–drug interactions
* risk assessment
* deprescribing assessment
* monitoring requirements

### 8. Summary Agent

The Summary Agent integrates the structured outputs produced throughout the pipeline into a final medication review.

The final output includes an overview and conclusion alongside the findings produced by the specialist agents.

---

## Safety Validation

A shared **Safety Validator Agent** is applied after relevant stages of the pipeline.

The validator receives:

* the current pipeline state
* the stage being validated
* the generated stage output
* stage-specific validation rules
* supporting evidence where applicable

Validation is **stage-aware**.

This means that the validation process changes depending on whether the output relates to indications, interactions, risks, deprescribing, monitoring or recommendations.

The validator provides an additional control layer intended to reduce propagation of structurally invalid, inconsistent or unsupported findings.

It does **not** guarantee clinical correctness and is not a replacement for professional clinical review.

---

## Clinical Knowledge Base

Structured clinical evidence is managed separately from the LLM agent implementations.

The clinical knowledge layer supports evidence retrieval for relevant stages of the medication review.

### British National Formulary

Drug interaction information was extracted from **BNF 85 Appendix 1**.

The source information was processed into machine-readable JSON files including:

```text
tables.json
interactions.json
```

The final extracted interaction database contains approximately:

```text
13,385 interaction records
```

This allows relevant BNF evidence to be retrieved programmatically without supplying the complete source document to the LLM for every patient.

The structured evidence can include:

```json
{
    "drug_1": "...",
    "drug_2": "...",
    "severity": "...",
    "evidence": "...",
    "action": "...",
    "table_reference": "..."
}
```

Original BNF source PDFs are not distributed through the repository where redistribution is restricted by copyright or licensing.

### STOPP/START Version 3

The pipeline also incorporates structured **STOPP/START Version 3** criteria.

Processed criteria are stored as:

```text
stopp.json
start.json
```

STOPP criteria support identification of potentially inappropriate prescribing.

START criteria support identification of potentially omitted clinically indicated treatment.

---

## Repository Structure

The project is organised into separate components for agents, prompts, clinical logic, data, validation and evaluation.

```text
smr/
│
├── agents/
│   ├── input_agent.py
│   ├── indication_agent.py
│   ├── ddi_interaction_agent.py
│   ├── risk_agent.py
│   ├── deprescribing_agent.py
│   ├── monitoring_agent.py
│   ├── recommendation_agent.py
│   ├── summary_agent.py
│   └── safety_validator_agent.py
│
├── prompts/
│   ├── input_agent.txt
│   ├── indication_agent.txt
│   ├── ddi_interaction_agent.txt
│   ├── risk_agent.txt
│   ├── deprescribing_agent.txt
│   ├── monitoring_agent.txt
│   ├── recommendation_agent.txt
│   ├── summary_agent.txt
│   └── safety_validator_agent.txt
│
├── clinical_logic/
│   ├── knowledge_base.py
│   └── priority.py
│
├── data/
│   ├── clinical_database/
│   │   ├── bnf_evidence/
│   │   │   ├── tables.json
│   │   │   └── interactions.json
│   │   └── stopp_start/
│   │       ├── stopp.json
│   │       └── start.json
│   └── datasets/
│       ├── development/
│       └── evaluation/
│
├── evaluation/
│   └── evaluation and analysis scripts
│
├── reports/
│   └── generated SMR reports
│
├── results/
│   ├── figures/
│   │   ├── indication_interaction_evaluation.png
│   │   └── clinical_detection_and_final_report.png
│   └── evaluation outputs
│
├── schemas/
│   └── Pydantic models and shared schemas
│
├── utils/
│   └── shared utility functions
│
├── validation/
│   └── validation logic
│
├── config.py
├── development_run.py
├── evaluation_run.py
├── imports.py
├── .gitignore
└── README.md
```

> The exact contents of generated-data directories may vary depending on which pipeline and evaluation scripts have been executed.

Generated patient reports are excluded from Git tracking to avoid unnecessary repository size.

Final evaluation results and figures are retained in `results/` to support transparency and reproducibility.

---

## Prompts

Copies of the final prompts used by the pipeline are provided separately in:

```text
prompts/
```

This makes the LLM instructions used during the study directly inspectable without requiring readers to search through each agent implementation.

The executable agent implementations remain within:

```text
agents/
```

The prompt files therefore provide a transparent record of the instructions used during the final evaluation.

---

## Technology Stack

The project was developed using **Python 3.12**.

| Technology              | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| Python                  | Core pipeline implementation             |
| LangChain               | LLM integration                          |
| `langchain-huggingface` | Hugging Face integration                 |
| Hugging Face            | LLM inference endpoint                   |
| Qwen2.5-7B-Instruct     | Language model used by the agents        |
| Pydantic v2             | Structured outputs and schema validation |
| pandas                  | Dataset processing and evaluation        |
| NumPy                   | Numerical operations                     |
| SciPy                   | Pearson correlation analysis             |
| scikit-learn            | Evaluation utilities                     |
| Matplotlib              | Results visualisation                    |
| Seaborn                 | Statistical visualisation                |
| PyMuPDF                 | PDF processing and evidence extraction   |
| LangSmith               | Development tracing and debugging        |
| JupyterLab              | Development and exploratory analysis     |
| Git                     | Version control                          |
| GitHub                  | Repository hosting                       |

Development and final evaluation were performed within an HPC environment.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jasmee-n/smr.git
cd smr
```

### 2. Create a Virtual Environment

Python **3.12** is recommended.

```bash
python -m venv .venv
```

Activate the environment on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install Dependencies

The principal dependencies include:

```bash
pip install \
    langchain \
    langchain-huggingface \
    huggingface-hub \
    pydantic \
    pandas \
    numpy \
    scipy \
    scikit-learn \
    matplotlib \
    seaborn \
    pymupdf
```

If a `requirements.txt` file is provided, the environment can instead be installed using:

```bash
pip install -r requirements.txt
```

Using the package versions associated with the final project environment is recommended for reproducibility.

---

## Configuration

External service configuration is defined in:

```text
config.py
```

The public repository contains placeholder values rather than private credentials.

For example:

```python
# Hugging Face
HUGGINGFACEHUB_API_TOKEN = 'YOUR_TOKEN'

# LangSmith
LANGSMITH_API_KEY = 'YOUR_API_KEY'
LANGSMITH_ENDPOINT = 'YOUR_ENDPOINT'
```

Replace these placeholders locally with the appropriate credentials before running the pipeline.

**Never commit real API keys, access tokens or other credentials to GitHub.**

---

## Model Configuration

The final pipeline used:

```text
Qwen2.5-7B-Instruct
```

through a Hugging Face inference endpoint.

The principal generation settings were:

```text
temperature = 0
max_new_tokens = 4000
```

A temperature of `0` was used to reduce unnecessary sampling variability during evaluation.

This does not guarantee completely identical outputs across repeated runs when inference depends on externally hosted infrastructure.

---

## LangSmith

LangSmith was used during development for:

* tracing agent execution
* debugging
* inspecting model calls
* examining latency

LangSmith was used as a development and observability tool rather than as an automated evaluator of clinical correctness.

---

## Running the Pipeline

Two primary execution scripts are provided.

### Development Pipeline

The development pipeline can be run using:

```bash
python development_run.py
```

The development dataset contains a smaller collection of synthetic patients used during implementation and debugging.

This allowed individual agents and pipeline behaviour to be inspected before the final evaluation.

### Final Evaluation Pipeline

The final evaluation is executed using:

```bash
python evaluation_run.py
```

This processes the synthetic evaluation cohort through the complete multi-agent pipeline.

The final evaluation cohort contains:

```text
100 synthetic patients
```

Outputs can subsequently be processed by the analysis scripts contained within:

```text
evaluation/
```

Evaluation outputs and figures are stored within:

```text
results/
```

---

## Generated Reports

The pipeline can produce a human-readable SMR report for each processed patient.

Generated reports are stored within:

```text
reports/
```

These reports integrate findings from the different pipeline stages, including:

* indications
* interactions
* risks
* deprescribing considerations
* monitoring requirements
* recommendations
* overview
* conclusion

The `reports/` directory is excluded from Git tracking because the reports are generated outputs and can be reproduced by running the pipeline.

---

## Synthetic Patient Dataset

The final evaluation uses a purpose-built synthetic cohort rather than identifiable patient data.

The evaluation dataset contains:

```text
N = 100
```

patients.

Synthetic patient characteristics include:

* age
* sex
* ethnicity
* height
* weight
* systolic and diastolic blood pressure
* heart rate
* HbA1c
* eGFR
* creatinine
* potassium
* haemoglobin
* smoking status
* alcohol status
* frailty
* medical conditions
* medications

Dataset generation uses:

```python
RANDOM_SEED = 42
```

to improve reproducibility.

Generated patients contain a minimum of:

```text
5 medications
2 clinical conditions
```

with variation in medication burden, multimorbidity and clinical complexity.

---

## Clinical Scenario Groups

The evaluation cohort contains seven broad clinical scenario groups:

```text
CARDIOVASCULAR_SCENARIOS
DIABETES_AND_CKD_SCENARIOS
HIGH_RISK_DRUG_INTERACTION_SCENARIOS
FRAILTY_SCENARIOS
MENTAL_HEALTH_SCENARIOS
MULTIMORBIDITY_SCENARIOS
RESPIRATORY_SCENARIOS
```

These groups introduce variation in both clinical characteristics and medication-related problems.

---

## Evaluation Case Types

Patients are additionally categorised according to four evaluation case types:

| Case Type | N |
| --------- | --: |
| Positive  | 44 |
| Negative  | 25 |
| Boundary  | 21 |
| Complex   | 10 |
| **Total** | **100** |

### Positive Cases

Contain predefined medication-related findings that the pipeline should detect.

### Negative Cases

Assess inappropriate detection and false-positive behaviour.

### Boundary Cases

Represent less straightforward or borderline clinical scenarios.

### Complex Cases

Contain greater clinical complexity, such as multimorbidity, polypharmacy or multiple simultaneous medication-related findings.

The use of different case types allows performance to be assessed beyond straightforward positive examples.

---

## Reference Standard

Reference standard is generated separately from the patient records supplied to the pipeline.

This prevents expected findings from being directly exposed to the LLM during inference.

Reference standard-truth targets include clinically relevant scenarios such as:

* anticoagulant/antiplatelet bleeding risk
* anticoagulant/NSAID bleeding risk
* dual antiplatelet therapy
* ACE inhibitor and potassium-sparing diuretic combinations
* NSAID use in chronic kidney disease
* ACE inhibitor + diuretic + NSAID combinations
* beta-blocker and rate-limiting calcium-channel blocker combinations
* CNS medication combinations
* serotonin syndrome risk
* QT-prolongation risk
* anticholinergic burden
* hyponatraemia risk
* falls risk
* respiratory risk

Expected medication indications are also stored separately for evaluation of the Indication Agent.

---

## Evaluation Design

Different evaluation approaches are used according to the output generated by each pipeline component.

This is necessary because indication and interaction outputs can be evaluated as discrete matches, while later clinical reasoning stages produce broader clinical findings.

### Indication Evaluation

Predicted medication indications are compared with predefined expected and acceptable indications.

The analysis calculates:

```text
True Positives
False Positives
False Negatives

Precision
Recall
F1-score
```

### Drug–Drug Interaction Evaluation

Predicted interaction pairs are compared against expected interaction pairs.

Performance is evaluated using:

```text
True Positives
False Positives
False Negatives

Precision
Recall
F1-score
```

### Clinical Target Detection

Later stages are evaluated according to whether predefined clinical targets are detected.

This includes:

```text
Risk
Deprescribing
Monitoring
Recommendation
```

Target-detection recall is calculated as:

```text
Number of expected targets detected
───────────────────────────────────
Total number of expected targets
```

---

## Evaluation Metrics

### Precision

Precision measures the proportion of generated findings that correspond to expected findings.

```text
Precision = TP / (TP + FP)
```

### Recall

Recall measures the proportion of expected findings that were successfully detected.

```text
Recall = TP / (TP + FN)
```

### F1-score

The F1-score represents the harmonic mean of precision and recall.

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### 95% Confidence Intervals

Where applicable, **95% confidence intervals** were calculated for proportion-based performance estimates using the **Wilson score method**.

The Wilson intervals were implemented directly in Python using a two-sided critical value of:

```text
z = 1.96
```

This method was applied to precision, recall, target-detection recall and execution success rates to provide an estimate of uncertainty around observed proportions.

For the medication-burden analysis, Pearson correlation coefficients were calculated using `scipy.stats.pearsonr`. Corresponding 95% confidence intervals for Pearson's *r* were estimated using Fisher's *z*-transformation.

### Micro-Averaged Performance

Micro averaging aggregates individual predictions before calculating overall performance.

This gives greater influence to components containing more individual evaluation observations.

### Macro-Averaged Performance

Macro averaging calculates metrics across components before averaging them.

This gives components more equal influence regardless of differences in the number of evaluation observations.

---

## Results

The final evaluation demonstrated substantial variation between individual pipeline components.

### Indication Agent

| Metric    | Result    | 95% CI      |
| --------- | --------: | -----------: |
| Precision | **0.854** | 0.828–0.876 |
| Recall    | **0.903** | 0.880–0.922 |
| F1-score  | **0.878** | — |

Classification counts:

```text
True Positives  = 706
False Positives = 121
False Negatives = 76
```

The Indication Agent was the strongest-performing evaluated component of the pipeline.

### Drug–Drug Interaction Agent

| Metric    | Result    | 95% CI      |
| --------- | --------: | -----------: |
| Precision | **0.289** | 0.254–0.328 |
| Recall    | **0.229** | 0.200–0.261 |
| F1-score  | **0.255** | — |

Classification counts:

```text
True Positives  = 166
False Positives = 408
False Negatives = 560
```

Interaction identification remained substantially more challenging than medication-indication mapping despite the integration of structured BNF evidence.

### Clinical Target Detection

| Agent          | Detected | Expected | Recall    | 95% CI      |
| -------------- | -------: | -------: | --------: | -----------: |
| Risk           | 130      | 302      | **0.430** | 0.376–0.487 |
| Deprescribing  | 4        | 22       | **0.182** | 0.073–0.385 |
| Monitoring     | 21       | 114      | **0.184** | 0.124–0.265 |
| Recommendation | 1        | 136      | **0.007** | 0.001–0.040 |

Among the later reasoning stages, the Risk Agent demonstrated the highest target-detection recall.

Recommendation target detection was particularly limited.

### Overall Performance

#### Micro-Averaged

| Metric    | Result    | 95% CI      |
| --------- | --------: | -----------: |
| Precision | **0.622** | 0.597–0.647 |
| Recall    | **0.578** | 0.553–0.603 |
| F1-score  | **0.600** | — |

#### Macro-Averaged

| Metric    | Result    |
| --------- | --------: |
| Precision | **0.572** |
| Recall    | **0.566** |
| F1-score  | **0.567** |

These results demonstrate why individual clinical functions should be evaluated separately rather than describing an LLM medication-review system using a single overall accuracy value.

### Execution Reliability

Technical execution reliability was evaluated separately from clinical performance.

Two complete evaluation attempts were performed:

| Attempt   | Successfully Completed |
| --------- | ---------------------: |
| Attempt 1 | 87 / 100 |
| Attempt 2 | 91 / 100 |

A pipeline execution may fail because of factors including:

* model endpoint availability
* inference timeouts
* malformed model responses
* structured-output validation failures
* other runtime errors

A successfully completed pipeline execution therefore does **not** imply that the generated medication review is clinically correct.

---

## Figures

Final evaluation figures are stored within:

```text
results/figures/
```

The repository retains the final composite figures rather than duplicate individual panels.

### Indication and Interaction Evaluation

```text
results/figures/indication_interaction_evaluation.png
```

This composite figure summarises performance for the two pipeline components evaluated using conventional classification metrics.

It presents:

* indication true positives, false positives and false negatives
* indication precision, recall and F1-score
* interaction true positives, false positives and false negatives
* interaction precision, recall and F1-score

The figure visually demonstrates the large difference between the relatively strong indication performance and substantially weaker interaction performance.

### Clinical Detection and Final Report

```text
results/figures/clinical_detection_and_final_report.png
```

This figure summarises downstream clinical target detection and final report performance.

It allows performance across later pipeline stages to be compared and highlights the decline in target detection for more integrative tasks, particularly recommendation generation.

Together, the final figures provide a visual summary of both discrete medication-level evaluation and broader clinical reasoning performance.

---

## Interpretation

Performance varied substantially according to the clinical task being performed.

Medication-indication mapping demonstrated comparatively strong precision and recall.

In contrast, drug–drug interaction detection showed both substantial false-positive and false-negative behaviour.

Later clinical reasoning stages also demonstrated limited target detection, with the Risk Agent outperforming the Deprescribing, Monitoring and Recommendation Agents.

These findings suggest that the difficulty of LLM-based medication review increases as tasks require greater integration of multiple pieces of patient information and previously generated findings.

The results also demonstrate that providing structured external clinical evidence does not automatically guarantee accurate use of that evidence by an LLM.

Retrieval, interpretation, structured generation, validation and downstream integration remain separate potential sources of error.

---

## Reproducibility

Several design choices were used to improve reproducibility.

### Fixed Dataset Seed

```python
RANDOM_SEED = 42
```

is used during synthetic patient generation.

### Model Temperature

The final model configuration uses:

```text
temperature = 0
```

to reduce sampling variability.

### Structured Schemas

Pydantic models constrain communication between pipeline components and provide structured output validation.

### Independent Reference Standard

Evaluation targets are stored independently from the patient information supplied to the agents.

### Version-Controlled Prompts

Copies of the final agent prompts are provided in:

```text
prompts/
```

allowing the instructions used during evaluation to be inspected directly.

### Structured Clinical Evidence

BNF and STOPP/START information is processed into machine-readable data before pipeline execution.

The final evaluation therefore does not depend on uncontrolled live web retrieval of clinical evidence.

### Version-Controlled Evaluation

Dataset generation, evaluation logic, pipeline code, schemas and final result figures are retained within the repository.

---

## Limitations

### Synthetic Patients

The final evaluation uses synthetic rather than real patient records.

Synthetic cases allow controlled reference standard evaluation but cannot reproduce the full uncertainty, missing information, documentation variability and longitudinal context present in real clinical records.

### Reference Standard Construction

Reference standard represents predefined expected findings.

It cannot represent every clinically reasonable interpretation of a patient, particularly for boundary and complex cases where clinical judgement may differ.

### Single Language Model

The final pipeline was evaluated using **Qwen2.5-7B-Instruct**.

Results should therefore not automatically be generalised to other LLMs.

### Clinical Knowledge Coverage

The BNF and STOPP/START criteria represent important clinical knowledge sources but do not contain all information required for a comprehensive medication review.

The system does not integrate every relevant clinical guideline or patient-specific information source.

### Drug–Drug Interaction Detection

Interaction evaluation is affected by:

* medication naming
* pair matching
* evidence retrieval
* representation of interaction mechanisms
* differences between generated findings and predefined reference standard truth

Interaction identification remained one of the weakest components in the final evaluation.

### Sequential Error Propagation

The pipeline is sequential.

Errors generated by an earlier agent may therefore influence later stages.

The Safety Validator aims to reduce this problem but cannot guarantee that all incorrect findings are identified or removed.

### External Inference Infrastructure

The system relies on an externally hosted model endpoint.

Endpoint availability, latency and infrastructure behaviour can therefore affect technical execution independently of the clinical reasoning task.

### Clinical Validation

The system has not undergone prospective clinical validation.

Its outputs must not be used for patient care.

---

## Future Work

Potential future development includes:

* evaluation using clinically reviewed or appropriately de-identified patient cases
* independent pharmacist evaluation of generated SMRs
* comparison with other LLMs
* comparison of single-agent and multi-agent architectures
* improved medication-name normalisation
* improved drug-interaction retrieval and matching
* integration of additional clinical knowledge sources
* explicit evidence citation within generated findings
* improved validator architecture
* uncertainty or confidence estimation
* systematic analysis of inference latency and computational cost
* assessment of run-to-run consistency
* evaluation of human–AI collaboration during medication review

The modular architecture allows individual agents to be modified, evaluated or replaced without redesigning the complete system.

---

## Clinical Disclaimer

This repository contains an **academic research prototype only**.

The system:

* is not a medical device
* has not been clinically validated
* is not intended to replace pharmacists, doctors or other healthcare professionals
* must not be used to make medication decisions for real patients

LLM-generated outputs can contain incorrect, incomplete or misleading clinical information.

Medication-related decisions must be made by appropriately qualified healthcare professionals using validated clinical systems, complete patient information and current clinical guidance.

---

## Author

**Jasmee Navaratnarajah**

MSc Bioinformatics Dissertation Project  
2026

---

## Licence and Clinical Sources

Any licence applied to this repository covers only the original project code and materials for which the author holds the appropriate rights.

Third-party clinical resources, including the **British National Formulary** and **STOPP/START criteria**, remain subject to their respective copyright and licensing conditions.

Original copyrighted source documents should not be redistributed through this repository unless redistribution is permitted.
