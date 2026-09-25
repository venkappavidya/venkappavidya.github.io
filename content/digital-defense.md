---
title: Uncovering Cyber Threats with RAG and Phi-3.5
date: February 2025
order: 2
kind: Project write-up
tags: RAG, LLM, Security, ChromaDB, LangChain
repo: https://github.com/vidyavenkappa/Microsoft-Defense-Report-Analysis
excerpt: Building a retrieval-augmented pipeline over five years of Microsoft Digital Defense Reports with ChromaDB, LangChain and Phi-3.5, and what it revealed about how attacks evolved between 2020 and 2024.
---

Staying ahead of emerging threats requires more than access to good intelligence. It requires the
ability to extract something actionable from a great deal of data. Microsoft's Digital Defense
Reports are a genuine trove of information on the state of cybersecurity, but at 80 to 120 pages
each, pulling the relevant parts out by hand is slow and easy to get wrong.

For this project I built a retrieval-augmented generation pipeline over the Microsoft Digital Defense
Reports from 2020 through 2024, giving security practitioners fast access to threat intelligence and
the mitigation strategies that go with it.

## Why these reports are hard to analyse

The reports are comprehensive, which is exactly what makes them difficult:

- **Volume.** Each report spans 80 to 120 pages of dense material.
- **Complex structure.** Multi-column layouts, tables and graphics defeat naive text extraction.
- **Temporal change.** Tracking how a threat evolved across five yearly reports is a substantial
  manual effort.
- **Context.** Relating a specific threat to the broader security picture takes domain expertise.

The pipeline had to do more than extract text. It had to contextualise it well enough to answer
specific security questions.

## Building the pipeline

### 1. Ingestion and processing

The first job was turning PDFs into usable text:

- Used the `unstructured` Python library to extract text while preserving the semantic structure of
  the content
- Processed roughly 3,000 tokens per page across five years of reports
- Maintained the connections between related sections despite the complex document layout

### 2. A searchable knowledge base

To make any of that queryable:

- Segmented text into manageable chunks with LangChain's text splitters
- Generated embeddings for each chunk to capture semantic meaning
- Stored those embeddings in **ChromaDB**, a vector database built for similarity search
- Combined semantic similarity with keyword matching in the retrieval step, which measurably improved
  accuracy over pure vector search

### 3. Answer generation

- Used Microsoft's **Phi-3.5** to generate responses grounded in the retrieved context
- Engineered prompts that push the model toward identifying significant threats and concrete
  mitigations rather than summarising
- Built an evaluation framework measuring accuracy and relevance against human-reviewed baselines

## What the data showed: threat evolution, 2020-2024

Querying five years at once surfaced a clear trajectory.

### 2020: pandemic-driven threats

Human-operated ransomware spiked, frequently initiated through brute-force attacks on remote desktop
proxies. Phishing campaigns exploited COVID-19 anxiety by impersonating trusted sources such as the
World Health Organization. Banking trojans picked up modular capabilities for credential theft, and
the first examples of adversarial machine learning attacks appeared.

### 2021: supply chain vulnerabilities

Ransomware kept climbing, increasingly delivered via targeted spear-phishing. Supply chain
vulnerabilities in IoT and OT devices became prominent. Disinformation campaigns began targeting
organisational security posture as a precursor to an attack.

### 2022: legacy system exploitation

Legacy systems and poor security hygiene emerged as the primary vulnerability points. Nation-state
ransomware activity showed markedly more sophistication and targeting, and threat actor groups
started coordinating more visibly.

### 2023: identity-based attacks

Large-scale ransomware campaigns expanded to target both endpoints and cloud infrastructure. Identity
attacks adopted advanced techniques such as adversary-in-the-middle. Criminal activity increasingly
turned on zero-day software vulnerabilities.

### 2024: nation-state and cloud threats

Nation-state actors amplified attacks with geopolitical motivations. Cyber-enabled influence
operations grew more sophisticated, and attack paths targeting critical assets in cloud environments
became substantially more complex.

## Why build this rather than use an off-the-shelf tool

Tools like Azure Security Copilot offer streamlined workflows for analysing security documents. A
custom pipeline still bought me several things:

- **Customisation.** Retrieval parameters tuned to the specific shape of security analysis
- **Context preservation.** Better retention of relationships between concepts across different
  reports
- **Longitudinal analysis.** Tracking a threat's evolution across multiple years, which is exactly
  what general-purpose tools handle worst
- **Portability.** The same approach adapts to document types well beyond Microsoft's reports

## Practical applications

- **Rapid threat intelligence.** Security teams can query historical threat data to inform a decision
  they need to make today.
- **Mitigation strategy.** Generate evidence-based recommendations for specific threats.
- **Training.** Build targeted security awareness material from the threats that actually matter.
- **Executive reporting.** Produce concise summaries of a complex threat landscape for leadership.

## Where this goes next

- Integration with real-time threat intelligence feeds, so historical analysis sits alongside current
  data
- Support for multi-language reports
- Analysis of diagrams and charts, to recover the insights currently locked in non-textual content
- Custom visualisation tools for representing threat evolution over time

## Conclusion

Combining retrieval-augmented generation with Phi-3.5 changed what it costs to understand a complex
security corpus. The result gives practitioners a clearer read on the threat landscape and a concrete
set of strategies for protecting their organisations.

In a field where threats evolve continuously, tooling that can extract, contextualise and present
security intelligence quickly is no longer a luxury.

> If you are working on RAG pipelines for security intelligence, I would be glad to compare notes.
> [Get in touch](../index.html#contact).
