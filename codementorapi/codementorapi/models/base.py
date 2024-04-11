from typing import Optional
from pydantic import BaseModel, computed_field

class IDURLModel(BaseModel):
    """A URL model with an auto populated ID field."""
    url: str = ''

    @computed_field 
    @property
    def id(self) -> Optional[str]:
        return self.url.split('/')[-1]
