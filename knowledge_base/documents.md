
# Knowledge Base Documents

This folder contains the recommended reference documents for the Dify knowledge base used by the IMO/NCSR approval workflow.

## Purpose

The workflow relies on the knowledge base to support three review branches:

- SHIP REPORTING SYSTEMS
- PROPOSED SHIP ROUTEING SYSTEMS
- TRAFFIC SEPARATION SCHEMES AND ROUTEING MEASURES OTHER THAN TRAFFIC SEPARATION SCHEMES

These files are intended to provide:

- governing conventions and regulations
- IMO resolutions and circulars
- proposal-preparation guidance
- preliminary assessment examples from NCSR sessions
- supplementary routeing guidance materials

## Current document set

The `knowledge_base/` folder currently includes the following categories of materials:

### 1. Core conventions and regulations

- `1972 CONVENTION ON THE INTERNATIONAL REGULATIONS.docx`
- `Reg__10__99_00_Amendment____Ships__routeing_20260409_103323.docx`
- `Reg__11__99_00_Amendment____Ship_reporting_systems_20260409_103329.docx`

These documents are useful for the legal and rule-based baseline of routeing systems and ship reporting systems.

### 2. Core IMO resolutions and guidance documents

- `A 20-Res.851 - General Principles For Ship Reporting Systems And Ship ReportingRequirements, Including Gu... (Secretariat).pdf`
- `A.572(14) .pdf`
- `MSC.1-Circ.1060 - Guidance Note On The Preparation Of Proposals On Ships' Routeing Systems And Ship Reportin... (Secretariat).pdf`
- `MSC.1-Circ.1060-Add.1 - Amendment To The Guidance Note On The Preparation Of Proposals On Ships. Routeing Systems... (Secretariat).pdf`
- `MSC.1-Circ.1608 - Procedure For The Submission Of Documents Containing Proposals For The Establishment Of, O... (Secretariat).pdf`
- `MSC.71(69).pdf`

These are the most important normative and procedural references for this project.

### 3. NCSR preliminary assessment working papers

- `NCSR 1-WP.2 - Preliminary assessment of proposals on Ships' routeing systems and ship reporting systems... (Secretariat).pdf`
- `NCSR 2-WP.3 - Preliminary assessment of proposals on Ships' routeing systems and ship reporting systems... (the Chairman).pdf`
- `NCSR 3-WP.3 - Preliminary assessment of proposals on Ships' routeing systems and ship reporting systems... (Chairman).pdf`
- `NCSR 4-WP.3 - Preliminary assessment of proposals on Ships' routeing systems and ship reporting systems... (Chair).pdf`
- `NCSR 5-WP.3 - Preliminary assessment of proposals onships' routeing systems and ship reporting systems f... (Chair).pdf`
- `NCSR 6-WP.3 - Preliminary assessment of proposals on ships' routeing systems for submission to the Sub-C... (Chair).pdf`
- `NCSR 7-WP.3 - Preliminary assessment of proposals on ships' routeing systems for submission to the Sub-C... (Chair).pdf`
- `NCSR 9-WP.3 - Preliminary assessment of proposals on ships' routeing and ship reporting systems (Chair).pdf`
- `NCSR 10-WP.3 - Preliminary assessment of proposals on ships' routeing and ship reporting systems (Chair).pdf`
- `NCSR 11-WP.3 - Preliminary assessment of proposals on ships' routeing systems (Secretariat).pdf`
- `NCSR 12-WP.3 - Preliminary assessment of proposals on ships' routeing and ship reporting systems (Chair).pdf`

These working papers are especially valuable because they reflect actual committee-style preliminary assessment logic and are highly relevant to the output style of this workflow.

### 4. Supplementary routeing-related circulars

- `SN.1-Circ.200-Add.1 - Adoption, Designation And Substitution Of Archipelagic Sea Lanes (Secretariat).pdf`
- `SN.1-Circ.204 - Amendments To The General Provisions On Ships' Routeing (Secretariat).PDF`
- `SN.1-Circ.206 - Guidance For Ships Transiting Archipelagic Waters (Secretariat).PDF`

These documents are useful as supplementary references for specialized routeing scenarios.

## Recommended knowledge base setup in Dify

When creating the knowledge base in Dify, it is recommended to:

1. Upload all files in this folder into the same knowledge base.
2. Use a document-processing strategy suitable for long regulatory and IMO meeting documents.
3. Prefer chunking that preserves section continuity rather than overly aggressive small chunks.
4. Enable reranking if available.
5. Keep the knowledge base focused on IMO/NCSR routeing and ship reporting review materials.

## Recommended use in the workflow

This knowledge base is designed to support three workflow branches:

### Branch 1: SHIP REPORTING SYSTEMS
Use the knowledge base to retrieve:

- SOLAS regulation 11 related materials
- A.851(20)
- MSC.1/Circ.1060 and Add.1
- preliminary assessment papers involving ship reporting systems

### Branch 2: PROPOSED SHIP ROUTEING SYSTEMS
Use the knowledge base to retrieve:

- SOLAS regulation 10 related materials
- A.572(14)
- MSC.1/Circ.1060 and Add.1
- MSC.1/Circ.1608
- routeing-related preliminary assessment papers

### Branch 3: TRAFFIC SEPARATION SCHEMES AND ROUTEING MEASURES OTHER THAN TRAFFIC SEPARATION SCHEMES
Use the knowledge base to retrieve:

- A.572(14)
- MSC.1/Circ.1060 and Add.1
- MSC.1/Circ.1608
- routeing-related working papers
- supplementary circulars relevant to traffic separation schemes and associated routeing measures

## Notes

- This folder is a recommended reference collection, not a mandatory fixed list.
- Users may add more IMO resolutions, circulars, adopted routeing measures, or internal review materials.
- If some documents are unavailable in a deployment environment, the workflow can still run, but retrieval quality may decrease.
- For open-source sharing, users should rebuild the knowledge base in their own Dify workspace rather than relying on exported dataset IDs.

## Suggested maintenance practice

When updating this folder, keep documents organized around these priorities:

- governing legal basis
- proposal preparation guidance
- committee preliminary assessment examples
- supplementary scenario-specific circulars

This makes the knowledge base easier to maintain and easier for other users to reproduce.
