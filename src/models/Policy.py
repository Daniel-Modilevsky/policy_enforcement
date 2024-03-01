from pydantic import BaseModel, constr


class Policy(BaseModel):
    id: str
    name: constr(min_length=1, max_length=32)
    description: constr(min_length=0)
