import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // Accept either `description` (old) or `query` (new) for the user's text input.
    // Also accept optional `city` and `incident_type`. `state` is still supported for
    // backward compatibility — `city` will be used if `state` is not provided.
    const { description, query, state, city, incident_type } = body;

    const text = (description || query || "").trim();
    const resolvedState = state || city || undefined;

    if (!text) {
      return NextResponse.json(
        { error: "Description or query is required" },
        { status: 400 }
      );
    }

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Mock response - replace with actual FastAPI endpoint
    const mockResponse = {
      // use provided incident_type if available
      crime_type: incident_type || "General Legal Matter",
      immediate_actions: [
        "Ensure your safety and move to a secure location if necessary",
        "Contact local police immediately or visit the nearest police station",
        "Document the incident with photographs, videos, or written notes",
        "Gather contact information of any witnesses present at the scene",
        "Preserve all physical evidence related to the incident",
      ],
      fir_steps: [
        "Visit the nearest police station in your jurisdiction" + (resolvedState ? ` (${resolvedState})` : ""),
        "Provide a detailed written complaint describing the incident",
        "Request a copy of the FIR for your records",
        "Note down the FIR number and the investigating officer's details",
        "Follow up regularly on the investigation progress",
      ],
      evidence_to_preserve: [
        "Physical evidence (if any) related to the incident",
        "Digital records: emails, messages, call logs, screenshots",
        "CCTV footage from the location if available",
        "Medical reports or certificates if injuries were sustained",
        "Financial records or transaction receipts if applicable",
      ],
      relevant_laws: [
        "Indian Penal Code (IPC) - relevant sections based on the nature of the crime",
        "Code of Criminal Procedure (CrPC) - procedural law for criminal matters",
        "Indian Evidence Act - rules regarding admissibility of evidence",
        resolvedState ? `State-specific laws applicable in ${resolvedState}` : "State-specific laws applicable in your jurisdiction",
        "Victim Compensation Scheme - for eligible cases",
      ],
    };

    return NextResponse.json(mockResponse);
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json(
      { error: "Failed to generate legal roadmap" },
      { status: 500 }
    );
  }
}
