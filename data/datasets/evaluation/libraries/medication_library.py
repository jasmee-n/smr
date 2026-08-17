CONDITION_MEDICATIONS = {
    # cardiovascular
    'Atrial fibrillation': ['Apixaban 5 mg twice daily', 'Bisoprolol 2.5 mg once daily', 'Dabigatran 150 mg twice daily', 'Digoxin 125 micrograms once daily', 'Diltiazem MR 120 mg once daily'],
    'Cardiac arrhythmia': ['Amiodarone 200 mg once daily', 'Bisoprolol 2.5 mg once daily', 'Flecainide 100 mg twice daily', 'Propafenone 150 mg three times daily', 'Sotalol 80 mg twice daily'],
    'Heart failure': ['Bisoprolol 1.25 mg once daily', 'Dapagliflozin 10 mg once daily', 'Furosemide 40 mg once daily', 'Ramipril 2.5 mg once daily', 'Spironolactone 25 mg once daily'],
    'Hypertension': ['Amlodipine 5 mg once daily', 'Doxazosin 1 mg once daily', 'Indapamide 2.5 mg once daily', 'Losartan 50 mg once daily', 'Ramipril 5 mg once daily'],
    'Ischaemic heart disease': ['Aspirin 75 mg once daily', 'Atorvastatin 80 mg once daily', 'Bisoprolol 5 mg once daily', 'Glyceryl trinitrate 400 micrograms when required', 'Isosorbide mononitrate MR 60 mg once daily'],
    'Peripheral oedema': ['Bendroflumethiazide 2.5 mg once daily', 'Bumetanide 1 mg once daily', 'Furosemide 40 mg once daily', 'Spironolactone 25 mg once daily', 'Torasemide 10 mg once daily'],
    'Recent acute coronary syndrome': ['Aspirin 75 mg once daily', 'Atorvastatin 80 mg once daily', 'Bisoprolol 2.5 mg once daily', 'Clopidogrel 75 mg once daily', 'Ticagrelor 90 mg twice daily'],

    # diabetes and chronic kidney disease
    'Chronic kidney disease': ['Dapagliflozin 10 mg once daily', 'Empagliflozin 10 mg once daily', 'Lisinopril 5 mg once daily', 'Losartan 50 mg once daily', 'Ramipril 2.5 mg once daily'],
    'Type 2 diabetes': ['Dapagliflozin 10 mg once daily', 'Empagliflozin 10 mg once daily', 'Gliclazide 80 mg once daily', 'Metformin 500 mg twice daily', 'Sitagliptin 100 mg once daily'],

    # respiratory
    'Allergic rhinitis': ['Beclometasone nasal spray 50 micrograms twice daily', 'Cetirizine 10 mg once daily', 'Fexofenadine 120 mg once daily', 'Loratadine 10 mg once daily', 'Mometasone nasal spray 100 micrograms once daily'],
    'Asthma': ['Beclometasone inhaler 100 micrograms twice daily', 'Budesonide/formoterol 200/6 micrograms twice daily', 'Montelukast 10 mg at night', 'Salbutamol inhaler 100 micrograms when required', 'Tiotropium inhaler 5 micrograms once daily'],
    'Chronic obstructive pulmonary disease': ['Aclidinium inhaler 322 micrograms twice daily', 'Salbutamol inhaler 100 micrograms when required', 'Tiotropium inhaler 18 micrograms once daily', 'Umeclidinium inhaler 55 micrograms once daily', 'Umeclidinium/vilanterol 55/22 micrograms once daily'],

    # mental health
    'Anxiety': ['Duloxetine 60 mg once daily', 'Escitalopram 10 mg once daily', 'Pregabalin 75 mg twice daily', 'Sertraline 50 mg once daily', 'Venlafaxine MR 75 mg once daily'],
    'Bipolar disorder': ['Aripiprazole 15 mg once daily', 'Lamotrigine 200 mg once daily', 'Lithium carbonate MR 400 mg at night', 'Olanzapine 10 mg once daily', 'Quetiapine 300 mg once daily'],
    'Depression': ['Citalopram 20 mg once daily', 'Fluoxetine 20 mg once daily', 'Mirtazapine 15 mg at night', 'Sertraline 50 mg once daily', 'Venlafaxine MR 75 mg once daily'],
    'Insomnia': ['Melatonin MR 2 mg at night', 'Promethazine 25 mg at night', 'Temazepam 10 mg at night', 'Zolpidem 5 mg at night', 'Zopiclone 3.75 mg at night'],
    'Schizophrenia': ['Amisulpride 200 mg twice daily', 'Aripiprazole 10 mg once daily', 'Olanzapine 10 mg once daily', 'Quetiapine 300 mg once daily', 'Risperidone 2 mg once daily'],

    # neurological
    'Epilepsy': ['Carbamazepine 200 mg twice daily', 'Lacosamide 100 mg twice daily', 'Lamotrigine 100 mg twice daily', 'Levetiracetam 500 mg twice daily', 'Topiramate 50 mg twice daily'],
    'Parkinson’s disease': ['Co-beneldopa 100/25 mg three times daily', 'Co-careldopa 100/25 mg three times daily', 'Pramipexole 88 micrograms three times daily', 'Rasagiline 1 mg once daily', 'Ropinirole 1 mg three times daily'],

    # pain and musculoskeletal
    'Chronic pain': ['Amitriptyline 10 mg at night', 'Duloxetine 60 mg once daily', 'Gabapentin 300 mg three times daily', 'Naproxen 250 mg twice daily', 'Paracetamol 1 g when required'],
    'Osteoarthritis': ['Capsaicin cream 0.025% four times daily', 'Diclofenac gel 1.16% when required', 'Ibuprofen gel 5% when required', 'Naproxen 250 mg twice daily', 'Paracetamol 1 g when required'],

    # gastrointestinal
    'Constipation': ['Bisacodyl 5 mg at night', 'Docusate sodium 100 mg twice daily', 'Lactulose 15 mL twice daily', 'Macrogol one sachet once daily', 'Senna 15 mg at night'],
    'Gastro-oesophageal reflux disease': ['Esomeprazole 20 mg once daily', 'Famotidine 20 mg twice daily', 'Lansoprazole 30 mg once daily', 'Omeprazole 20 mg once daily', 'Pantoprazole 40 mg once daily'],

    # frailty
    'Frailty': [],
    'History of falls': [],

    # other
    'Benign prostatic hyperplasia': ['Alfuzosin XL 10 mg once daily', 'Doxazosin 1 mg once daily', 'Dutasteride 500 micrograms once daily', 'Finasteride 5 mg once daily', 'Tamsulosin 400 micrograms once daily'],
    'Hypothyroidism': ['Levothyroxine 25 micrograms once daily', 'Levothyroxine 50 micrograms once daily', 'Levothyroxine 75 micrograms once daily', 'Levothyroxine 100 micrograms once daily', 'Levothyroxine 125 micrograms once daily'],
    'Overactive bladder': ['Mirabegron 50 mg once daily', 'Oxybutynin 5 mg twice daily', 'Solifenacin 5 mg once daily', 'Tolterodine 2 mg twice daily', 'Trospium 20 mg twice daily']
}