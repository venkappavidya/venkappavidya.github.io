---
title: Predicting Security Incidents with Machine Learning
date: December 2024
order: 4
kind: Project write-up
tags: Machine Learning, CatBoost, Security, MITRE ATT&CK
repo: https://github.com/vidyavenkappa/Microsoft-Security-Incident-Detection
excerpt: Building an 80%-accurate CatBoost classifier over Microsoft's GUIDE dataset (13 million data points, 1.6 million alerts), and what the feature analysis revealed about how attacks actually arrive.
---

Being able to predict and prevent a security incident before it happens is worth a great deal more
than responding well after the fact. This project built a machine learning model to predict security
incidents in Microsoft systems using the GUIDE dataset.

## Project overview

The goal was a classification model capable of analysing patterns in Microsoft's GUIDE dataset to
predict potential security incidents. The dataset is substantial: **13 million data points across 33
entity types, covering 1.6 million alerts and 1 million annotated incidents from over 6,100
organisations**.

Using CatBoost and detailed feature engineering, the final model reached **80% accuracy**.

## Data analysis and preparation

Working through the dataset surfaced several things worth knowing before modelling anything:

- Only **35%** of detected incidents are classified as true positives requiring immediate attention
- **Initial Access** attacks represent **70%** of all security incidents, followed by Suspicious
  Activity (10.8%) and Impact (7.2%)
- **Windows** systems account for 90.88% of affected systems, then Linux (7.55%) and macOS (1.51%)
- Incidents peak at **5:00 PM** and are generally more frequent during nighttime hours

Preparation involved converting categorical values into meaningful numeric representations, web
scraping with Beautiful Soup to decode certain numeric codes, cleaning and imputing missing data, and
creating temporal features to capture the attack-time patterns above.

## Feature engineering and selection

Feature engineering mattered more to the final result than model choice did. Correlation analysis
across the dataset identified the most predictive variables:

- OS family identification (Windows, Linux, macOS)
- MITRE ATT&CK technique categorisation, with TA0001 (Initial Access) predominant
- Temporal patterns of attack occurrence
- Host and network-based indicators

I used correlation matrices to select features with strong relationships to incident grades,
following a consistent process: understand the feature characteristics and relationships, clean and
impute, then select the columns with real correlation to incident classification.

## Model development

After trying several classification algorithms, **CatBoost** came out ahead. The architecture ran in
three stages: feature understanding and selection, training and fine-tuning, then rigorous
evaluation.

CatBoost suited this dataset specifically because:

- It handles categorical variables natively, without extensive preprocessing
- It is robust to outliers and missing data
- It performs well on imbalanced classification problems, which security incident detection very much
  is

## Results and MITRE ATT&CK analysis

The final model achieved **80% accuracy**, identifying potential security incidents while keeping
false positives in check.

The analysis also surfaced the most common MITRE ATT&CK techniques in the dataset:

- **T1078: Valid Accounts.** By far the most prevalent attack vector.
- **T1566: Phishing.** The second most common initial access technique.
- **T1110: Brute Force.** Still significant, despite years of security advancement.
- **T1133: External Remote Services.** Exploiting vulnerabilities in remote access.
- **T1087: Account Discovery.** Attackers mapping internal network accounts.

That ranking is directly actionable: it tells you which mitigations to fund first.

## Mitigations the data supports

### Techniques

- **Employee training and testing.** Yearly security awareness training, with more frequent random
  phishing tests.
- **Least privilege access.** Monthly audits of server access permissions.
- **Zero trust.** Audit every admin rights access request.

### Tools

- **Multi-factor authentication with physical keys.** Hardware tokens for all company computer
  logins; hardware tokens or biometrics for mobile.
- **Supplier software and hardware maintenance.** Monthly audits of supplier-implemented services and
  hardware for vulnerabilities.
- **Automated incident detection.** Deploy the prediction model and keep investing in it.

These align with Microsoft's Return on Mitigation (ROM) scoring methodology, which evaluates security
measures on security value, potential user impact, and ease of implementation.

## Future directions

- Enhancing the model with more sophisticated machine learning techniques
- Better systems for collaboration and information sharing about emerging threats
- Moving toward a comprehensive zero trust architecture
- More effective proactive security awareness programmes
- Prioritising security investment using ROM scoring

## Conclusion

This project demonstrates what machine learning can add to cybersecurity defence. Working with
CatBoost over the GUIDE dataset makes it possible to move from reactive to proactive security,
potentially preventing incidents before they reach systems and users.

The four findings that matter most: Initial Access dominates at 70% of incidents; attacks concentrate
in the evening, peaking at 5:00 PM; Windows systems are the overwhelming target at 90.88%; and valid
accounts, not exotic exploits, are the most common way in.

Address those specifically, deploy the prediction model, and an organisation's security posture
improves measurably.
