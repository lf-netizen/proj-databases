from pydantic import BaseModel, Field
import nanoid
from datetime import datetime
from typing import List, Optional

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_enabled: bool = True