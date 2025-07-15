from pydantic import BaseModel, HttpUrl, validator
from typing import Optional
from datetime import datetime


class RandomUrlBase(BaseModel):
    """Base schema for random URL"""

    url: HttpUrl
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True

    @validator("category")
    def validate_category(cls, v):
        if v:
            allowed_categories = [
                "social",
                "news",
                "shopping",
                "entertainment",
                "sports",
                "technology",
                "education",
                "travel",
                "finance",
                "other",
            ]
            if v.lower() not in allowed_categories:
                raise ValueError(
                    f'Category must be one of: {", ".join(allowed_categories)}'
                )
        return v.lower() if v else v


class RandomUrlCreate(RandomUrlBase):
    """Schema for creating a new random URL"""

    pass


class RandomUrlUpdate(BaseModel):
    """Schema for updating a random URL"""

    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

    @validator("category")
    def validate_category(cls, v):
        if v:
            allowed_categories = [
                "social",
                "news",
                "shopping",
                "entertainment",
                "sports",
                "technology",
                "education",
                "travel",
                "finance",
                "other",
            ]
            if v.lower() not in allowed_categories:
                raise ValueError(
                    f'Category must be one of: {", ".join(allowed_categories)}'
                )
        return v.lower() if v else v


class RandomUrlInDB(RandomUrlBase):
    """Schema for random URL in database"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RandomUrlResponse(RandomUrlInDB):
    """Schema for random URL response"""

    pass


class RandomUrlListResponse(BaseModel):
    """Schema for paginated random URL list response"""

    items: list[RandomUrlResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class RandomUrlBulkCreate(BaseModel):
    """Schema for bulk creating random URLs"""

    urls: list[RandomUrlCreate]


class RandomUrlBulkDelete(BaseModel):
    """Schema for bulk deleting random URLs"""

    url_ids: list[int]


class RandomUrlsByCategory(BaseModel):
    """Schema for getting random URLs by category"""

    category: str
    urls: list[RandomUrlResponse]
