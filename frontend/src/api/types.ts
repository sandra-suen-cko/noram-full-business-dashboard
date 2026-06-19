/**
 * TypeScript types for API responses
 * Mirrors backend Pydantic models
 */

export interface MetricInfo {
  name: string
  display_name: string
  unit: string
  decimals: number
}

export interface DomainMetadata {
  metrics: MetricInfo[]
  columns: string[]
}

export interface ErrorDetail {
  row: number
  column: string
  error: string
}

export interface AnalyticsResponse {
  domain: string
  data: Record<string, unknown>[]
  errors: ErrorDetail[]
  columns: string[]
  last_updated: string
}

export interface MetadataResponse {
  frontbook: DomainMetadata
  backbook: DomainMetadata
}

export interface HealthResponse {
  status: string
  message: string
}
