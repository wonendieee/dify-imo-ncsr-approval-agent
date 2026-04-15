from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.excel_ops import inspect_workbook, workbook_from_source


class InspectExcelTemplateTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        source_type = str(tool_parameters.get('template_source_type', 'builtin'))
        builtin_template = tool_parameters.get('builtin_template') or 'demo_template'
        template_url = tool_parameters.get('template_url') or ''
        template_base64 = tool_parameters.get('template_base64') or ''
        max_cells = int(tool_parameters.get('max_non_empty_cells_per_sheet', 50))

        try:
            plugin_root = Path(__file__).resolve().parent.parent
            workbook, source_label = workbook_from_source(
                plugin_root=plugin_root,
                source_type=source_type,
                builtin_template=builtin_template,
                template_url=template_url,
                template_base64=template_base64,
            )
            result = inspect_workbook(workbook, max_non_empty_cells_per_sheet=max_cells)
            result['template_source'] = source_label
            yield self.create_text_message('Excel template inspected successfully.')
            yield self.create_json_message(result)
            for key, value in result.items():
                yield self.create_variable_message(key, value)
        except Exception as e:
            yield self.create_text_message(f'Error inspecting Excel template: {e}')
            return
