# imports
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager


# style
available_fonts = {font.name for font in font_manager.fontManager.ttflist}

if 'Times New Roman' in available_fonts:
    FONT = 'Times New Roman'
elif 'Liberation Serif' in available_fonts:
    FONT = 'Liberation Serif'
else:
    FONT = 'DejaVu Serif'

plt.rcParams.update({
    'font.family': FONT,
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.edgecolor': 'black',
    'axes.linewidth': 0.8,
    'xtick.color': 'black',
    'ytick.color': 'black',
    'text.color': 'black',
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white'
})


# paths
PROJECT_ROOT = Path('/data/home/bt25094/dissertation/smr pipeline')

METRICS_PATH = PROJECT_ROOT / 'results' / 'evaluation_metrics.json'
SUMMARY_PATH = PROJECT_ROOT / 'results' / 'summary_evaluation.json'
STATISTICS_PATH = PROJECT_ROOT / 'results' / 'evaluation_statistics.json'
FIGURES_PATH = PROJECT_ROOT / 'results' / 'figures'

FIGURES_PATH.mkdir(parents = True, exist_ok = True)


# load metrics
with METRICS_PATH.open('r', encoding = 'utf-8') as file:
    results = json.load(file)

with SUMMARY_PATH.open('r', encoding = 'utf-8') as file:
    summary = json.load(file)

execution = results['execution_reliability']
clinical = results['clinical_evaluation_attempt_2']

metrics = clinical['metrics']
target_detection = clinical['target_detection']


# confidence intervals
def wilson_interval(successes, total, z = 1.96):
    if total == 0:
        return 0, 0

    p = successes / total
    denominator = 1 + z ** 2 / total
    centre = (p + z ** 2 / (2 * total)) / denominator

    margin = z * math.sqrt(
        p * (1 - p) / total
        + z ** 2 / (4 * total ** 2)
    ) / denominator

    return round(centre - margin, 3), round(centre + margin, 3)


# statistics
clinical_statistics = {
    agent: {
        'precision': values['precision'],
        'precision_95_ci': list(
            wilson_interval(values['tp'], values['tp'] + values['fp'])
        ),
        'recall': values['recall'],
        'recall_95_ci': list(
            wilson_interval(values['tp'], values['tp'] + values['fn'])
        ),
        'f1': values['f1']
    }
    for agent, values in metrics.items()
}

target_statistics = {
    agent: {
        'detected': values['detected'],
        'expected': values['expected'],
        'detection_rate': values['recall'],
        'detection_95_ci': list(
            wilson_interval(values['detected'], values['expected'])
        )
    }
    for agent, values in target_detection.items()
}

execution_statistics = {
    attempt: {
        'completed': values['completed'],
        'failed': values['failed'],
        'total': values['total'],
        'success_rate': values['success_rate'],
        'success_95_ci': list(
            wilson_interval(values['completed'], values['total'])
        )
    }
    for attempt, values in execution.items()
}

statistics = {
    'execution_reliability': execution_statistics,
    'clinical_performance': clinical_statistics,
    'target_detection': target_statistics,
    'micro_metrics': clinical['micro_metrics'],
    'macro_metrics': clinical['macro_metrics'],
    'final_report_quality': {
        'completeness': summary['overall_completeness'],
        'completeness_95_ci': summary['completeness_95_ci'],
        'validator_pass_rate': summary['validator_pass_rate']
    }
}

with STATISTICS_PATH.open('w', encoding = 'utf-8') as file:
    json.dump(statistics, file, indent = 2, ensure_ascii = False)


# 1. indication and interaction agent evaluation
agents = ['indications', 'interactions']
agent_labels = ['Indication\nAgent', 'Interaction\nAgent']

x = np.arange(len(agent_labels))
width = 0.23

tp = [metrics[agent]['tp'] for agent in agents]
fp = [metrics[agent]['fp'] for agent in agents]
fn = [metrics[agent]['fn'] for agent in agents]

precision = [metrics[agent]['precision'] for agent in agents]
recall = [metrics[agent]['recall'] for agent in agents]
f1 = [metrics[agent]['f1'] for agent in agents]

fig, axes = plt.subplots(
    1,
    2,
    figsize = (11, 4.8)
)


# A. number of findings
bars_a = [
    axes[0].bar(
        x - width,
        tp,
        width,
        label = 'True Positives',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = '//'
    ),
    axes[0].bar(
        x,
        fp,
        width,
        label = 'False Positives',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = '..'
    ),
    axes[0].bar(
        x + width,
        fn,
        width,
        label = 'False Negatives',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = 'xx'
    )
]

axes[0].set_ylabel('Number of Findings')
axes[0].set_xticks(x)
axes[0].set_xticklabels(agent_labels)

max_count = max(tp + fp + fn)
axes[0].set_ylim(0, max_count * 1.18)

axes[0].legend(
    frameon = False,
    loc = 'upper right',
    fontsize = 9
)

for group in bars_a:
    axes[0].bar_label(
        group,
        padding = 4,
        fontsize = 9
    )

axes[0].text(
    -0.10,
    1.04,
    'A',
    transform = axes[0].transAxes,
    fontsize = 12,
    fontweight = 'bold',
    va = 'top'
)


# B. precision, recall and F1-score
bars_b = [
    axes[1].bar(
        x - width,
        precision,
        width,
        label = 'Precision',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = '//'
    ),
    axes[1].bar(
        x,
        recall,
        width,
        label = 'Recall',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = '..'
    ),
    axes[1].bar(
        x + width,
        f1,
        width,
        label = 'F1-Score',
        facecolor = 'white',
        edgecolor = 'black',
        linewidth = 1,
        hatch = 'xx'
    )
]

axes[1].set_ylabel('Performance Score')
axes[1].set_ylim(0, 1.12)
axes[1].set_xticks(x)
axes[1].set_xticklabels(agent_labels)

axes[1].legend(
    frameon = False,
    loc = 'upper right',
    fontsize = 9
)

for group in bars_b:
    axes[1].bar_label(
        group,
        fmt = '%.3f',
        padding = 4,
        fontsize = 9
    )

axes[1].text(
    -0.10,
    1.04,
    'B',
    transform = axes[1].transAxes,
    fontsize = 12,
    fontweight = 'bold',
    va = 'top'
)


# formatting
for ax in axes:
    ax.tick_params(axis = 'both', labelsize = 9)

fig.subplots_adjust(
    left = 0.08,
    right = 0.98,
    bottom = 0.16,
    top = 0.92,
    wspace = 0.30
)

for extension in ['png', 'pdf']:
    fig.savefig(
        FIGURES_PATH / f'indication_interaction_evaluation.{extension}',
        dpi = 300,
        bbox_inches = 'tight'
    )

plt.show()
plt.close(fig)


# 2. reference finding detection and final report completeness
labels = [
    'Indication\nAgent',
    'Interaction\nAgent',
    'Risk\nAgent',
    'Deprescribing\nAgent',
    'Monitoring\nAgent',
    'Recommendation\nAgent'
]

detected = [
    metrics['indications']['tp'],
    metrics['interactions']['tp'],
    target_detection['risks']['detected'],
    target_detection['deprescribing']['detected'],
    target_detection['monitoring']['detected'],
    target_detection['recommendations']['detected']
]

expected = [
    metrics['indications']['tp'] + metrics['indications']['fn'],
    metrics['interactions']['tp'] + metrics['interactions']['fn'],
    target_detection['risks']['expected'],
    target_detection['deprescribing']['expected'],
    target_detection['monitoring']['expected'],
    target_detection['recommendations']['expected']
]

rates = np.array([
    detected_value / expected_value * 100
    for detected_value, expected_value in zip(detected, expected)
])

intervals = [
    wilson_interval(detected_value, expected_value)
    for detected_value, expected_value in zip(detected, expected)
]

lower = np.array([
    rate - ci[0] * 100
    for rate, ci in zip(rates, intervals)
])

upper = np.array([
    ci[1] * 100 - rate
    for rate, ci in zip(rates, intervals)
])

completeness = summary['overall_completeness']
ci_lower = summary['completeness_95_ci'][0]
ci_upper = summary['completeness_95_ci'][1]

summary_rate = completeness * 100
summary_lower = (completeness - ci_lower) * 100
summary_upper = (ci_upper - completeness) * 100

fig, axes = plt.subplots(
    1,
    2,
    figsize = (11, 4.8),
    gridspec_kw = {'width_ratios': [4, 1.3]}
)


# A. reference finding detection
bars = axes[0].bar(
    labels,
    rates,
    yerr = [lower, upper],
    capsize = 4,
    facecolor = 'white',
    edgecolor = 'black',
    linewidth = 1,
    error_kw = {
        'ecolor': 'black',
        'elinewidth': 1,
        'capthick': 1
    }
)

axes[0].set_ylabel('Reference Findings Detected (%)')
axes[0].set_ylim(0, 110)

for bar, rate, error in zip(bars, rates, upper):
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        rate + error + 2,
        f'{rate:.1f}%',
        ha = 'center',
        va = 'bottom',
        fontsize = 9
    )

axes[0].text(
    -0.08,
    1.03,
    'A',
    transform = axes[0].transAxes,
    fontsize = 12,
    fontweight = 'bold'
)


# B. final report completeness
bars = axes[1].bar(
    ['Final\nReport'],
    [summary_rate],
    yerr = [[summary_lower], [summary_upper]],
    capsize = 4,
    facecolor = 'white',
    edgecolor = 'black',
    linewidth = 1,
    error_kw = {
        'ecolor': 'black',
        'elinewidth': 1,
        'capthick': 1
    }
)

axes[1].set_ylabel('High-Priority Findings Retained (%)')
axes[1].set_ylim(0, 110)

axes[1].text(
    bars[0].get_x() + bars[0].get_width() / 2,
    summary_rate + summary_upper + 2,
    f'{summary_rate:.1f}%',
    ha = 'center',
    va = 'bottom',
    fontsize = 9
)

axes[1].text(
    -0.18,
    1.03,
    'B',
    transform = axes[1].transAxes,
    fontsize = 12,
    fontweight = 'bold'
)

fig.subplots_adjust(
    left = 0.08,
    right = 0.98,
    bottom = 0.17,
    top = 0.92,
    wspace = 0.35
)

for extension in ['png', 'pdf']:
    fig.savefig(
        FIGURES_PATH / f'clinical_detection_and_final_report.{extension}',
        dpi = 300,
        bbox_inches = 'tight'
    )

plt.show()
plt.close(fig)


# output
print(f'\nFONT USED: {FONT}')

print('\n95% CONFIDENCE INTERVALS:')
print('-' * 50)

for agent, values in clinical_statistics.items():
    print(
        f'{agent.upper():20} '
        f'P={values["precision"]:.3f} {values["precision_95_ci"]}  '
        f'R={values["recall"]:.3f} {values["recall_95_ci"]}'
    )

print('\nREFERENCE FINDING DETECTION:')
print('-' * 50)

for label, detected_value, expected_value, rate, ci in zip(
    labels,
    detected,
    expected,
    rates,
    intervals
):
    print(
        f'{label.replace(chr(10), " "):20} '
        f'{detected_value}/{expected_value} '
        f'({rate:.1f}%) '
        f'{ci}'
    )

print('\nEXECUTION RELIABILITY:')
print('-' * 50)

for attempt, values in execution_statistics.items():
    print(
        f'{attempt.upper():20} '
        f'{values["completed"]}/{values["total"]} '
        f'({values["success_rate"]:.1%}) '
        f'{values["success_95_ci"]}'
    )

print('\nFINAL REPORT QUALITY:')
print('-' * 50)

print(
    f'COMPLETENESS: '
    f'{summary["high_priority_findings_represented"]}/'
    f'{summary["high_priority_findings"]} '
    f'({summary["overall_completeness"]:.1%}) '
    f'{summary["completeness_95_ci"]}'
)

print(
    f'VALIDATOR PASS RATE: '
    f'{summary["validator_pass_rate"]:.1%}'
)

print(f'\nSTATISTICS SAVED TO: {STATISTICS_PATH}')
print(f'FIGURES SAVED TO: {FIGURES_PATH}')