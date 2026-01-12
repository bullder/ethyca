from pydantic import BaseModel, Field

class Move(BaseModel):
    x: int = Field(..., ge=0, le=2, description="X coordinate (0, 1, 2)")
    y: int = Field(..., ge=0, le=2, description="Y coordinate (0, 1, 2)")

    @property
    def position(self) -> int:
        return self.y * 3 + self.x

    @classmethod
    def from_index(cls, index: int) -> 'Move':
        x = index % 3
        y = index // 3
        return cls(x=x, y=y)