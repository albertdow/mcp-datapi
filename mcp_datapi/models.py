from datetime import datetime
from pydantic import BaseModel


class Response(BaseModel):
    message: str


class CollectionInfo(BaseModel):
    id: str
    title: str
    description: str
    published_at: datetime
    updated_at: datetime
    begin_datetime: datetime
    end_datetime: datetime
    bbox: tuple[float, float, float, float]


class DownloadRequest(BaseModel):
    id: str
    product_type: list[str]
    variable: list[str]
    year: list[str]
    month: list[str]
    day: list[str]
    # fmt: off
    time: list[str] = [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ]
    # fmt: on
    area: list[float] = [90, -180, -90, 180]
    data_format: str = "netcdf"
    download_format: str = "zip"
    pressure_level: list[str] | None = None


class DownloadResponse(BaseModel):
    message: str
    request_id: str
