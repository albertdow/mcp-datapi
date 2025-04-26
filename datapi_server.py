import os
from enum import StrEnum
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from datapi import ApiClient
from pydantic import BaseModel

mcp = FastMCP("DatapiServer", dependencies=["datapi"])

load_dotenv()
DATAPI_URL = os.getenv("DATAPI_URL")
DATAPI_KEY = os.getenv("DATAPI_KEY")


class JobStatus(StrEnum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class Response(BaseModel):
    message: str


@mcp.tool()
def get_jobs(
    status: JobStatus | None = None,
) -> list[str]:
    """Fetch list of jobs."""
    params: dict[str, Any] = {
        "sortby": "-created",
    }
    if status:
        params["status"] = str(status)

    client = ApiClient(url=DATAPI_URL, key=DATAPI_KEY)
    client.check_authentication()
    jobs = client.get_jobs(**params)
    jobs.response.raise_for_status()

    return jobs.request_ids


@mcp.tool()
def download_job_result(
    job_id: str,
) -> Response:
    """Download finished job using job id."""

    client = ApiClient(url=DATAPI_URL, key=DATAPI_KEY)
    client.check_authentication()
    client.download_results(job_id)

    return Response(message="success")


if __name__ == "__main__":
    mcp.run()
