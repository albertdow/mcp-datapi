import os
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from datapi import ApiClient
from enums import JobStatus
from exceptions import CdsEnvironmentVariablesNotSetError
from models import (
    Response,
    CollectionInfo,
    DownloadRequest,
    DownloadResponse,
)

mcp = FastMCP("DatapiServer", dependencies=["datapi"])

load_dotenv()
DATAPI_URL = os.getenv("DATAPI_URL")
DATAPI_KEY = os.getenv("DATAPI_KEY")

if not DATAPI_URL or not DATAPI_KEY:
    raise CdsEnvironmentVariablesNotSetError()


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

    return Response(message="Successfully downloaded job results.")


@mcp.tool()
def get_all_collections() -> list[str]:
    """Get the ids of all collections available in the catalogue."""

    client = ApiClient(url=DATAPI_URL, key=DATAPI_KEY)
    client.check_authentication()
    collections = client.get_collections(sortby="update")

    return collections.collection_ids


@mcp.tool()
def get_collection_by_id(collection_id: str) -> CollectionInfo:
    """Get more details for a specific collection."""

    client = ApiClient(url=DATAPI_URL, key=DATAPI_KEY)
    client.check_authentication()
    collection = client.get_collection(collection_id)

    return CollectionInfo.model_validate(
        {
            "id": collection.id,
            "title": collection.title,
            "description": collection.description,
            "published_at": collection.published_at,
            "updated_at": collection.updated_at,
            "begin_datetime": collection.begin_datetime,
            "end_datetime": collection.end_datetime,
            "bbox": collection.bbox,
        }
    )


@mcp.tool()
def submit_job(download_request: DownloadRequest) -> DownloadResponse:
    """Submit a download request."""

    client = ApiClient(url=DATAPI_URL, key=DATAPI_KEY)
    client.check_authentication()

    request = client.submit(
        download_request.id,
        download_request.model_dump(exclude={"id"}, exclude_none=True),
    )
    return DownloadResponse(
        request_id=request.request_id, message="Successfully submitted job request."
    )


if __name__ == "__main__":
    mcp.run()
