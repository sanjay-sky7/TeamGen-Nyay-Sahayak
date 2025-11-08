/**
 * Nyay Sahayak Backend API Client
 * Handles all communication with the backend API
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const API_BASE_URL = `${BACKEND_URL}/api/v1`;

export interface LegalRoadmap {
  crime_type: string;
  immediate_actions: string[];
  fir_steps: string[];
  evidence_to_preserve: string[];
  relevant_laws: string[];
}

export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  crime_type?: string;
  immediate_actions?: string[];
  fir_steps?: string[];
  evidence_to_preserve?: string[];
  relevant_laws?: string[];
  response?: LegalRoadmap;
  roadmap?: LegalRoadmap;
  data?: LegalRoadmap;
}

/**
 * Check if the backend is available
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const response = await fetch(`${API_BASE_URL}/health`, {
      signal: controller.signal,
      mode: 'cors',
      method: 'GET',
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.error("Health check failed:", error);
    return false;
  }
}

/**
 * Send a query to the backend API
 */
export async function sendQuery(query: string): Promise<LegalRoadmap> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s timeout for AI processing

  try {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
      signal: controller.signal,
      mode: 'cors'
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
        errorData.message ||
        `Backend request failed: ${response.status} ${response.statusText}`
      );
    }

    const result: QueryResponse = await response.json();

    // Handle different response formats from backend
    let roadmapData: LegalRoadmap;

    if (result.crime_type || result.immediate_actions) {
      // Direct roadmap format
      roadmapData = result as LegalRoadmap;
    } else if (result.response) {
      // Wrapped in response field
      roadmapData = result.response;
    } else if (result.roadmap) {
      // Wrapped in roadmap field
      roadmapData = result.roadmap;
    } else if (result.data) {
      // Wrapped in data field
      roadmapData = result.data;
    } else {
      // Try to use as-is
      roadmapData = result as LegalRoadmap;
    }

    // Validate roadmap structure
    if (!roadmapData || (!roadmapData.crime_type && !roadmapData.immediate_actions)) {
      throw new Error("Invalid response format from backend - missing required fields");
    }

    return roadmapData;
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error("Request timeout - the backend took too long to respond");
    }
    throw error;
  }
}

/**
 * Rebuild the index (admin function)
 */
export async function rebuildIndex(): Promise<{ message: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/ingest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      mode: 'cors'
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
        errorData.message ||
        `Failed to rebuild index: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("Unknown error occurred while rebuilding index");
  }
}

/**
 * Send FIR draft to user's email
 */
export async function sendFirEmail(query: string, email: string): Promise<{ message: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/send-fir-email`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query, email }),
      mode: 'cors'
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
        errorData.message ||
        `Failed to send FIR email: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error("Unknown error occurred while sending FIR email");
  }
}

/**
 * Build a query string from form data
 */
export function buildQueryString(
  description: string,
  state?: string,
  incident_type?: string
): string {
  let query = description.trim();

  if (state?.trim()) {
    query += `. Location: ${state.trim()}.`;
  }

  if (incident_type?.trim()) {
    query += ` Incident type: ${incident_type.trim()}.`;
  }

  return query;
}

