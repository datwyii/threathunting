# Week 3 — Data Processing and Exploitation

## Objective
This week focuses on preparing threat intelligence data so it can be reliably used in analysis tools.

Main goals:
- filtering noisy or incomplete indicators
- normalizing indicator formats
- enriching and correlating indicators
- preparing for MISP deployment and IOC import

## Input Data from Week 2
Week 2 data collection output is not available yet.

**To be completed:** When available, Week 2 data will provide indicators such as:
- IP addresses
- domains
- URLs
- SHA256 hashes

For now, this repository uses empty templates and clearly marked placeholders only.

## Data Filtering
Filtering removes rows that cannot be used for analysis.

Planned filtering checks include:
- remove empty rows
- remove records with missing `type` or `value`
- remove obvious duplicates

## Data Normalization
Normalization makes indicator formatting consistent.

Examples:
- trim leading/trailing whitespace
- lowercase domain values
- preserve valid indicator types and values

The script in `scripts/normalize_iocs.py` performs a basic starter normalization process.

## Data Enrichment and Correlation
Enrichment and correlation connect indicators to context (for example: source confidence, related events, or repeated sightings).

**To be completed:** Add enrichment/correlation logic after Week 2 data is available.

## MISP Deployment
MISP will be used to manage and analyze threat intelligence in a structured way.

**To be completed:** Deploy MISP in the local lab environment and document setup steps.

## IOC Import into MISP
After normalization, IOCs will be imported as MISP event attributes.

**To be completed:** Create a MISP event and import normalized IOC attributes from `data/normalized_iocs.csv`.

## Results
Current status:
- starter structure for Week 3 is prepared
- CSV templates are ready for Week 2 data
- normalization script is implemented for initial processing

**To be completed:** Add practical results after real Week 2 data is processed and imported into MISP.

## Conclusion
This Week 3 starter project establishes a clean workflow for threat intelligence processing.

It is intentionally lightweight and uses placeholders until Week 2 collection data is available.
