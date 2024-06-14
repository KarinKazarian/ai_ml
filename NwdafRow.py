from pydantic import BaseModel
from typing import List

class NwdafRow(BaseModel):
  t: int
  cell_id: int
  cat_id: int
  pe_id: int
  load: float
  has_anomaly: int

class NwdafRowList(BaseModel):
    data: List[NwdafRow]