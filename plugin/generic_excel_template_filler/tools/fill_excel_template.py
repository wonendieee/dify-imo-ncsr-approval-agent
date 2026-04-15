from __future__ import annotations

import io
from collections.abc import Generator
from pathlib import Path
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.excel_ops import (
    apply_cells,
    apply_issue_rows,
    apply_named_cells,
    apply_placeholders,
    infer_issue_count,
    load_json_object,
    load_payload,
    sanitize_output_filename,
    trim_unused_issue_rows,
    workbook_from_source,
)


# Fixed behavior defaults for cleaner Dify node UI
USE_UNICODE_SUPERSCRIPT = True
AUTO_TRIM_ISSUE_ROWS = True
PRESERVE_CLOSING_ROW_STYLE = True


class FillExcelTemplateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        source_type = str(tool_parameters.get("template_source_type", "builtin") or "builtin")
        builtin_template = tool_parameters.get("builtin_template") or "ship_reporting_systems"
        template_url = tool_parameters.get("template_url") or ""
        template_base64 = tool_parameters.get("template_base64") or ""
        payload_json = tool_parameters.get("payload_json", "")
        output_filename = tool_parameters.get("output_filename") or ""
        delivery_mode = str(tool_parameters.get("delivery_mode", "upload_link") or "upload_link")

        if not payload_json:
            yield self.create_text_message("Error: payload_json is required.")
            return

        try:
            plugin_root = Path(__file__).resolve().parent.parent

            workbook, source_label = workbook_from_source(
                plugin_root=plugin_root,
                source_type=source_type,
                builtin_template=builtin_template,
                template_url=template_url,
                template_base64=template_base64,
            )

            payload = load_payload(payload_json)

            issue_auto_fill_count = apply_issue_rows(
                workbook,
                payload,
                USE_UNICODE_SUPERSCRIPT,
            )

            filled_cell_count = 0
            placeholder_replacement_count = 0

            cells = payload.get("cells", {})
            if cells:
                if not isinstance(cells, dict):
                    raise ValueError('"cells" must be an object mapping cell references to values.')
                filled_cell_count += apply_cells(
                    workbook,
                    cells,
                    USE_UNICODE_SUPERSCRIPT,
                )

            named_cells = payload.get("named_cells", {})
            if named_cells:
                if not isinstance(named_cells, dict):
                    raise ValueError('"named_cells" must be an object mapping defined names to values.')
                filled_cell_count += apply_named_cells(
                    workbook,
                    named_cells,
                    USE_UNICODE_SUPERSCRIPT,
                )

            placeholders = payload.get("placeholders", {})
            if placeholders:
                if not isinstance(placeholders, dict):
                    raise ValueError('"placeholders" must be an object mapping tokens to values.')
                placeholder_replacement_count += apply_placeholders(
                    workbook,
                    placeholders,
                    USE_UNICODE_SUPERSCRIPT,
                )

            issue_count = infer_issue_count(payload)
            deleted_issue_rows = 0
            if AUTO_TRIM_ISSUE_ROWS:
                deleted_issue_rows = trim_unused_issue_rows(
                    workbook,
                    issue_count,
                    preserve_closing_style=PRESERVE_CLOSING_ROW_STYLE,
                )

            if workbook.worksheets and not any(ws.sheet_state == "visible" for ws in workbook.worksheets):
                workbook.worksheets[0].sheet_state = "visible"

            final_name = sanitize_output_filename(
                output_filename or payload.get("output_filename") or "filled_template",
                default_name="filled_template",
            )
            final_file_name = f"{final_name}.xlsx"

            buffer = io.BytesIO()
            workbook.save(buffer)
            excel_bytes = buffer.getvalue()

            sheet_names = [ws.title for ws in workbook.worksheets]
            result = {
                "generated_file_name": final_file_name,
                "template_source_type": source_type,
                "filled_cell_count": filled_cell_count + issue_auto_fill_count,
                "placeholder_replacement_count": placeholder_replacement_count,
                "workbook_sheet_names": sheet_names,
                "template_source": source_label,
                "delivery_mode": delivery_mode,
                "issue_count": issue_count if issue_count is not None else 0,
                "deleted_issue_rows": deleted_issue_rows,
                "use_unicode_superscript": USE_UNICODE_SUPERSCRIPT,
                "auto_trim_issue_rows": AUTO_TRIM_ISSUE_ROWS,
                "preserve_closing_row_style": PRESERVE_CLOSING_ROW_STYLE,
            }

            yield self.create_text_message(f"Excel file generated successfully: {final_file_name}")

            if delivery_mode == "upload_link":
                provider_credentials = getattr(self.runtime, "credentials", {}) or {}

                upload_url = str(provider_credentials.get("upload_url", "") or "").strip()
                upload_token = str(provider_credentials.get("upload_token", "") or "").strip()
                upload_file_field_name = (
                    str(provider_credentials.get("upload_file_field_name", "file") or "file").strip() or "file"
                )
                response_download_url_field = (
                    str(provider_credentials.get("response_download_url_field", "download_url") or "download_url").strip()
                    or "download_url"
                )
                response_file_name_field = (
                    str(provider_credentials.get("response_file_name_field", "file_name") or "file_name").strip()
                    or "file_name"
                )
                upload_headers_json = str(provider_credentials.get("upload_headers_json", "") or "").strip()
                upload_form_data_json = str(provider_credentials.get("upload_form_data_json", "") or "").strip()

                if not upload_url:
                    raise ValueError(
                        "Provider credential 'upload_url' is required when delivery_mode=upload_link."
                    )

                headers = load_json_object(upload_headers_json, {})
                form_data = load_json_object(upload_form_data_json, {})

                if not isinstance(headers, dict):
                    raise ValueError("Provider credential 'upload_headers_json' must decode to a JSON object.")
                if not isinstance(form_data, dict):
                    raise ValueError("Provider credential 'upload_form_data_json' must decode to a JSON object.")

                form_data.setdefault("desired_name", final_file_name)
                if upload_token:
                    headers.setdefault("Authorization", f"Bearer {upload_token}")

                files = {
                    upload_file_field_name: (
                        final_file_name,
                        excel_bytes,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                }

                resp = requests.post(
                    upload_url,
                    headers=headers,
                    data=form_data,
                    files=files,
                    timeout=120,
                )
                resp.raise_for_status()

                resp_json = resp.json() if resp.content else {}
                if not isinstance(resp_json, dict):
                    raise ValueError("Upload service must return a JSON object.")

                download_url = resp_json.get(response_download_url_field)
                uploaded_name = resp_json.get(response_file_name_field) or final_file_name

                if not download_url:
                    raise ValueError(
                        f"Upload succeeded but response field '{response_download_url_field}' was not found."
                    )

                result["download_url"] = download_url
                result["returned_file_name"] = uploaded_name

                yield self.create_json_message(result)
                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_text_message(f"Download URL: {download_url}")
                return

            yield self.create_json_message(result)
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_blob_message(
                blob=excel_bytes,
                meta={
                    "file_name": final_file_name,
                    "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                },
            )

        except Exception as e:
            yield self.create_text_message(f"Error generating Excel file: {e}")
            return