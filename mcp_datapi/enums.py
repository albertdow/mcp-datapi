from enum import StrEnum


class JobStatus(StrEnum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCESSFUL = "successful"
    FAILED = "failed"
