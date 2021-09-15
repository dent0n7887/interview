from typing import Any, Dict, Optional

import pydantic


class WebClientResponse(pydantic.BaseModel):
    body: Optional[Dict[str, Any]] = None
    headers: dict = None
    status: int = None
