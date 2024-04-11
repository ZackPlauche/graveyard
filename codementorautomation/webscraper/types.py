from pydantic import BaseModel, ConfigDict

BaseModel.model_config = ConfigDict(extra='forbid')


class LoginDetails(BaseModel):
    email: str
    password: str
