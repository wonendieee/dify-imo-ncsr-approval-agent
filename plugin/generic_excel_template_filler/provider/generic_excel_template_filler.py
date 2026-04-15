from __future__ import annotations

from typing import Any

from dify_plugin import ToolProvider


class GenericExcelTemplateFillerProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # This provider does not require credentials.
        return None
