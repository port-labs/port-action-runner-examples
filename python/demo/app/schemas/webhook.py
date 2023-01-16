from typing import Optional, Union, Literal
from pydantic import BaseModel
from datetime import datetime


class Webhook(BaseModel):
    class Context(BaseModel):
        blueprint: Optional[str]
        entity: Optional[str]
        runId: Optional[str]

    class Trigger(BaseModel):
        class By(BaseModel):
            userId: str
            orgId: str

        by: By
        origin: Union[Literal['UI'], Literal['API']]
        at: datetime

    action: str
    status: str
    resourceType: Literal['run']
    context: Context
    payload: dict
    trigger: Trigger
