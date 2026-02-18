
from typing import Any

class Commands:
    def __init__(self, client: Any = None, groups: list = None):
        self.client = client
        self.groups = groups or []