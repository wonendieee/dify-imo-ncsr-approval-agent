# Dify IMO/NCSR Approval Agent

> **Quick Access**
>
> The reusable Dify workflow DSL can be downloaded from the [`app/`](./app) folder:
>
> - [`app/approval-agent.yml`](./app/approval-agent.yml)
>
> The custom Excel plugin package can be found in the [`plugin/`](./plugin) folder.

A Dify-based approval workflow for IMO/NCSR review scenarios, covering:

- **SHIP REPORTING SYSTEMS**
- **PROPOSED SHIP ROUTEING SYSTEMS**
- **TRAFFIC SEPARATION SCHEMES AND ROUTEING MEASURES OTHER THAN TRAFFIC SEPARATION SCHEMES**

This project is intended as a **reproducible open-source workflow project**.  
It is **not** a hosted shared-API service.

Users are expected to run it with **their own API keys** or **their own local/self-hosted models**.

---

## Overview

This repository contains a complete Dify-based approval workflow for routeing-related IMO/NCSR review scenarios. It combines:

- document upload
- PDF-to-image conversion
- multimodal approval reasoning
- knowledge-base-assisted review
- structured JSON conversion
- fixed-format Excel approval output

The project is especially suitable for scenarios where the **final output must follow a strict institutional Excel template**, rather than a generic Markdown table or free-form text summary.

---

## Core Innovation

## Custom Excel Template-Filling Plugin

The biggest innovation of this project is the custom Dify plugin:

**`generic_excel_template_filler`**

This is not a normal JSON-to-Excel export tool.

It is designed for **fixed-format approval tables** and supports:

- filling complex Excel templates while preserving original formatting
- using **named ranges** for reliable mapping
- supporting multiple built-in approval templates
- trimming unused issue rows automatically
- preserving borders, merged cells, widths, heights, and layout as much as possible
- generating approval-ready Excel outputs instead of generic data tables

This plugin is the core reason why the workflow can produce **formal, reusable, fixed-format approval tables**.

---

## Main Features

- Supports three IMO/NCSR approval-table scenarios
- Uploads and processes PDF proposals
- Converts PDF pages to images for multimodal review
- Uses Dify workflow orchestration for branching logic
- Retrieves reference material from knowledge bases
- Produces structured reviewer decisions in JSON
- Maps structured decisions into fixed Excel templates
- Generates formal approval tables with preserved layout
- Supports custom file delivery via a minimal upload/download service

---

## Supported Approval Templates

This project currently includes three built-in Excel templates:

1. **SHIP REPORTING SYSTEMS**
2. **PROPOSED SHIP ROUTEING SYSTEMS**
3. **TRAFFIC SEPARATION SCHEMES AND ROUTEING MEASURES OTHER THAN TRAFFIC SEPARATION SCHEMES**

These templates use **named ranges** so that the plugin can fill them reliably without rebuilding layout from scratch.

---

## Repository Structure

```text
.
├─ app/
│  └─ dify-imo-ncsr-approval-agent.yml
├─ plugin/
│  ├─ generic_excel_template_filler/
│  └─ generic_excel_template_filler.difypkg
├─ service/
│  └─ minimal_upload_service.py
├─ knowledge_base/
│  ├─ documents
│  └─ knowledge-base-setup.md
├─ examples/
│  ├─ sample_input.pdf
│  └─ sample_output.xlsx
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## Tested Environment

Tested on:

- **Dify 1.11.0**
- Windows host environment
- custom local plugin installation
- fixed-template Excel generation workflow

Recommended components:

- Dify workflow support
- local plugin installation enabled
- a working model provider configuration
- optional self-hosted or API-based model endpoints
- optional internal or public file service for stable download links

---

## Model Compatibility

This project does **not** include any shared model quota or bundled API access.

Users must configure their own model providers, for example:

- OpenAI-compatible APIs
- DeepSeek-compatible APIs
- SiliconFlow-compatible APIs
- local Ollama models
- self-hosted inference backends
- other providers supported by Dify

You may use:

- fully hosted model providers
- fully local/self-hosted models
- a hybrid architecture combining both

---

## Knowledge Base Compatibility

This repository does **not** bundle live Dify dataset IDs or private knowledge-base contents.

You should either:

- rebuild the knowledge base in your own Dify workspace
- replace the retrieval nodes with your own datasets
- or run a simplified version without retrieval first

For best results, prepare a domain-specific knowledge base containing:

- relevant IMO resolutions
- relevant circulars and guidelines
- previously adopted reporting or routeing documents
- internal review references if applicable

---

## Why This Project Matters

Many LLM workflows can extract structured data.  
Far fewer can generate **formal, fixed-format Excel approval tables** that preserve:

- complex borders
- merged cells
- vertical headers
- fixed layout
- issue rows
- remarks sections
- institutional formatting conventions

This project focuses on that gap.

It is intended for workflows where the **format of the final output matters as much as the content**.

---

## Quick Start

## 1. Deploy Dify

Deploy your own Dify instance.

This project assumes you already have a working Dify environment with workflow support.

---

## 2. Import the Workflow DSL

Import the Dify app DSL from:

```text
app/dify-imo-ncsr-approval-agent.yml
```

After import, review:

- model bindings
- plugin dependencies
- retrieval nodes
- workflow variables
- output behavior

---

## 3. Install Required Plugins

Install all marketplace plugins referenced by the workflow.

Then install the custom local plugin:

```text
plugin/generic_excel_template_filler.difypkg
```

If you prefer, you can also install the plugin from source by packaging it yourself.

---

## 4. Configure Your Own Model Providers

Replace all model bindings with your own available configuration.

Examples:

- your own API keys
- your own OpenAI-compatible endpoint
- your own local model backend
- your own reranker / embedding provider

Because this repository is intended for reproducibility, **users must provide their own model resources**.

---

## 5. Prepare the Knowledge Bases

Rebuild or replace the knowledge bases used by the workflow.

At minimum, check that each retrieval node points to a valid dataset in your own Dify workspace.

If you do not yet have a knowledge base ready, start with:

- workflow import
- plugin installation
- template testing
- local model setup

Then add retrieval later.

---

## 6. Start the Upload/Download Service

This project includes a minimal service for file upload and stable download naming.

Run:

```bash
uvicorn minimal_upload_service:app --host 0.0.0.0 --port 8000
```

If the file is stored under `service/`, start it from that directory or adjust the command accordingly.

Typical purpose of this service:

- store generated Excel files
- provide stable download URLs
- preserve logical filenames better than default platform-generated names

---

## 7. Test the Plugin First

Before running the entire workflow, test the plugin separately inside Dify.

Recommended order:

### Step A
Use **Inspect Excel Template** to verify:

- sheet names
- visible sheets
- named ranges
- placeholders
- template structure

### Step B
Use **Fill Excel Template** to verify:

- built-in template selection
- named-range filling
- issue-row trimming
- preserved formatting
- successful `.xlsx` generation

Once plugin tests pass, connect it to the full workflow.

---

## 8. Run the Workflow

Upload a proposal PDF and select one of the missions:

- ship reporting systems
- ship routeing systems
- traffic separation schemes

The workflow will then:

1. extract document text
2. convert PDF pages to images
3. run approval-oriented reasoning
4. generate structured JSON
5. map the JSON into template payloads
6. fill the selected Excel template
7. return a formal approval-style Excel file

---

## Workflow Logic

At a high level, the workflow consists of:

1. **User Input**
   - mission selection
   - file upload

2. **PDF Processing**
   - document extraction
   - PDF-to-image conversion

3. **Branching**
   - separate logic for the three approval-table types

4. **Knowledge Retrieval**
   - routeing/reporting-related reference lookup

5. **Approval Reasoning**
   - multimodal review
   - approval-conclusion memo generation

6. **Structured JSON Conversion**
   - strict schema-based output

7. **Code Mapping**
   - JSON to template payload conversion

8. **Excel Template Filling**
   - custom plugin fills built-in templates

9. **File Delivery**
   - either direct file output
   - or upload-link delivery through the minimal service

---

## Fixed-Template Output Strategy

This project does **not** rely on generic Markdown tables.

Instead, it uses a template-driven strategy:

- Excel template defines layout
- plugin preserves formatting
- workflow supplies semantic content only
- unused issue rows are trimmed automatically
- final output remains close to the institutional template design

This is much more suitable for regulatory or approval workflows.

---

## Plugin Design Notes

The custom plugin supports:

- built-in templates
- URL-based templates
- base64 templates
- `named_cells`
- `placeholders`
- direct `cells`
- issue row trimming
- partial preservation of closing row style
- optional upload-link delivery mode

Recommended usage in this project:

- use **built-in templates**
- use **named ranges**
- keep template title/subtitle fixed in the template itself
- let the workflow fill only variable approval content

---

## Files Not Included

For safety and reproducibility reasons, this repository should **not** include:

- your private API keys
- internal model endpoints
- private knowledge-base data
- sensitive approval documents
- internal-only service URLs
- secrets or deployment credentials

Use your own `.env` or local deployment configuration.

---

## Recommended Documentation Extensions

You may further expand this repository with:

- `docs/plugin-design.md`
- `docs/installation.md`
- `docs/knowledge-base-setup.md`
- `docs/workflow-overview.md`

These are especially useful if you want other users to reproduce the project with their own infrastructure.

---

## Suggested Use Cases

- IMO/NCSR document review support
- maritime administration approval workflows
- fixed-format table generation
- Dify-based regulatory workflow design
- Excel template automation
- multimodal document-review agents

---

## Known Limitations

- API keys are not bundled
- live Dify datasets are not bundled
- knowledge base content must be rebuilt by the user
- output quality depends on the chosen models
- structured review quality depends on prompt/model fit
- some environments may require prompt tuning
- some delivery behaviors depend on the local Dify/plugin runtime

---

## Roadmap

Possible future improvements:

- generalized template management UI
- better rich-text superscript handling in Excel cells
- broader template portability
- optional API-first deployment mode
- more robust issue-footnote synchronization
- support for additional IMO/NCSR table families

---

## License

**MIT License**

---

## Acknowledgements

Built with:

- Dify
- custom workflow design
- a custom Excel template-filling plugin
- PDF-to-image tooling
- local or API-based model backends
- fixed-format Excel approval design

---

## Final Note

This repository is best understood as a **reproducible workflow project**.

It is meant to help users:

- study the workflow design
- reproduce the pipeline locally
- connect their own models
- customize their own knowledge bases
- reuse the Excel template plugin in similar approval scenarios
