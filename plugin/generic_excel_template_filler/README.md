# Generic Excel Template Filler

A Dify local tool plugin that preserves Excel template formatting while filling values.

## What it does
- Inspect an Excel template and discover sheets, visible sheets, defined names, merged ranges, issue sections, and placeholders like `{{title}}`.
- Fill an Excel template using four generic methods:
  - explicit cell mappings (`cells`)
  - named ranges (`named_cells`)
  - placeholder replacement (`placeholders`)
  - issue list auto-fill (`issues` or `issue_rows`)
- Automatically trim unused reserved issue rows while trying to preserve the closing row style.
- Return the finished `.xlsx` file directly or upload it to your own service and return a stable download URL.

## Built-in templates
- `SHIP REPORTING SYSTEMS`
- `PROPOSED SHIP ROUTEING SYSTEMS`
- `TRAFFIC SEPARATION SCHEMES AND ROUTEING MEASURES OTHER THAN TRAFFIC SEPARATION SCHEMES`

## Template source modes
- `builtin`: uses one of the bundled templates above
- `url`: downloads a public `.xlsx` template
- `base64`: decodes a base64-encoded `.xlsx`

## Recommended workflow pattern
1. User chooses a built-in template or provides a template URL/base64.
2. Run `inspect_excel_template` to discover named ranges and issue sections.
3. LLM or Code node prepares `payload_json`.
4. Run `fill_excel_template` to generate the final Excel file.
5. Optional: set `delivery_mode=upload_link` to return a stable download URL from your own service.

## Recommended payload structure
```json
{
  "named_cells": {
    "document_label_cell": "NCSR 10/3 (United Kingdom)",
    "context_description_cell": "Ship reporting system in the Pentland Firth"
  },
  "issues": [
    "The objective described in section 8 is not sufficiently clear.",
    "The proposal does not explain existing measures."
  ],
  "cells": {
    "Sheet1!B4": {"display": "U3", "symbol": "U", "footnote_ref": "3"}
  },
  "output_filename": "ship_reporting_systems_result"
}
```

## Important limitation
Dify tool parameters currently document support for `string`, `number`, `boolean`, `select`, and `secret-input` parameter types. There is no standard `file` parameter declaration for tool YAML. Because of that, the most portable design is built-in/URL/base64 templates rather than direct binary file upload into the tool node.

## Packaging
```bash
dify plugin package ./generic_excel_template_filler
```
Then install the generated `.difypkg` in Dify via local file.
