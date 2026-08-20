from schemas import PrioritisedFinding

def rank_findings(state):
    findings = []

    priority_scores = {
        'critical': 4,
        'high': 3,
        'moderate': 2,
        'medium': 2,
        'low': 1
    }

    for item in state.interactions.interactions:
        level = item.severity.lower()

        findings.append(
            PrioritisedFinding(
                finding_type = 'Interaction',
                description = f'{item.drug_a} + {item.drug_b}: {item.rationale}',
                priority_level = level.upper(),
                priority_score = priority_scores.get(level, 1),
                source = item.source
            )
        )

    for item in state.risks.risks:
        level = item.severity.lower()

        findings.append(
            PrioritisedFinding(
                finding_type = 'Risk',
                description = f'{item.risk_type}: {item.rationale}',
                priority_level = level.upper(),
                priority_score = priority_scores.get(level, 1),
                source = item.source
            )
        )

    for item in state.deprescribing.deprescribing:
        level = item.priority.lower()

        findings.append(
            PrioritisedFinding(
                finding_type = 'Deprescribing',
                description = f'{item.medication}: {item.issue}',
                priority_level = 'MODERATE' if level == 'medium' else level.upper(),
                priority_score = priority_scores.get(level, 1),
                source = item.source
            )
        )

    for item in state.monitoring.monitoring:
        level = item.priority.lower()

        findings.append(
            PrioritisedFinding(
                finding_type = 'Monitoring',
                description = f'{item.medication_or_condition}: {item.monitoring_required}',
                priority_level = 'MODERATE' if level == 'medium' else level.upper(),
                priority_score = priority_scores.get(level, 1),
                source = item.source
            )
        )

    for item in state.recommendations.recommendations:
        level = item.priority.lower()

        findings.append(
            PrioritisedFinding(
                finding_type = 'Recommendation',
                description = item.recommendation,
                priority_level = 'MODERATE' if level == 'medium' else level.upper(),
                priority_score = priority_scores.get(level, 1),
                source = item.source
            )
        )

    findings.sort(
        key = lambda finding: finding.priority_score,
        reverse = True
    )

    return findings