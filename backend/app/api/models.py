"""Pydantic models for API responses."""
from typing import List, Dict, Any
from pydantic import BaseModel


class MetricInfo(BaseModel):
    """Metadata about a single metric."""
    name: str
    display_name: str
    unit: str
    decimals: int


class DomainMetadata(BaseModel):
    """Metadata for a domain (Frontbook/Backbook)."""
    metrics: List[MetricInfo]
    columns: List[str]


class ErrorDetail(BaseModel):
    """Details about a data error."""
    row: int
    column: str
    error: str


class AnalyticsResponse(BaseModel):
    """Response for analytics data endpoint."""
    domain: str
    data: List[Dict[str, Any]]
    errors: List[ErrorDetail]
    columns: List[str]
    last_updated: str


class MetadataResponse(BaseModel):
    """Response for metadata endpoint."""
    frontbook: DomainMetadata
    backbook: DomainMetadata


class HealthResponse(BaseModel):
    """Response for health check endpoint."""
    status: str
    message: str
