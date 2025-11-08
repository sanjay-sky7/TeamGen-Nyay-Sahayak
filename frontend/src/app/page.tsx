"use client";

import { useState, useEffect } from "react";
import { Header } from "@/components/nyay-sahayak/header";
import { InputForm } from "@/components/nyay-sahayak/input-form";
import { ResultCard } from "@/components/nyay-sahayak/result-card";
import { FirEmailForm } from "@/components/nyay-sahayak/fir-email-form";
import { ThemeToggle } from "@/components/nyay-sahayak/theme-toggle";
import { toast } from "sonner";
import {
  checkHealth,
  sendQuery,
  buildQueryString,
  type LegalRoadmap
} from "@/lib/api/nyay-sahayak";

// Mock response for fallback
const getMockResponse = (description: string, state?: string, incident_type?: string): LegalRoadmap => {
  return {
    crime_type: incident_type || "General Legal Matter",
    immediate_actions: [
      "Ensure your safety and move to a secure location if necessary",
      "Contact local police immediately or visit the nearest police station",
      "Document the incident with photographs, videos, or written notes",
      "Gather contact information of any witnesses present at the scene",
      "Preserve all physical evidence related to the incident",
    ],
    fir_steps: [
      "Visit the nearest police station in your jurisdiction" + (state ? ` (${state})` : ""),
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
      state ? `State-specific laws applicable in ${state}` : "State-specific laws applicable in your jurisdiction",
      "Victim Compensation Scheme - for eligible cases",
    ],
  };
};

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [roadmap, setRoadmap] = useState<LegalRoadmap | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);
  const [originalQuery, setOriginalQuery] = useState<string>("");

  // Check backend connection on mount
  useEffect(() => {
    const checkBackendConnection = async () => {
      const isConnected = await checkHealth();
      setBackendConnected(isConnected);
    };

    checkBackendConnection();
  }, []);

  const handleSubmit = async (data: {
    description: string;
    state?: string;
    incident_type?: string;
  }) => {
    setIsLoading(true);
    setRoadmap(null);
    setOriginalQuery(""); // Reset original query

    try {
      // Build query string for backend API
      const query = buildQueryString(data.description, data.state, data.incident_type);

      // Store the original query for FIR email
      setOriginalQuery(query);

      // Try backend API
      const roadmapData = await sendQuery(query);

      setRoadmap(roadmapData);
      setBackendConnected(true);
      toast.success("Legal roadmap generated successfully!");
    } catch (error) {
      // Fallback to mock response
      console.error("Backend request failed:", error);
      setBackendConnected(false);

      const errorMessage = error instanceof Error ? error.message : "Unknown error";

      // Build query even for mock response (for FIR email)
      const query = buildQueryString(data.description, data.state, data.incident_type);
      setOriginalQuery(query);

      // Simulate processing time
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const mockResponse = getMockResponse(
        data.description,
        data.state,
        data.incident_type
      );

      setRoadmap(mockResponse);
      toast.warning(`Backend unavailable: ${errorMessage}. Showing mock response.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <ThemeToggle />

      {/* Backend Status Indicator */}
      {backendConnected !== null && (
        <div className="fixed top-4 left-4 z-50">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${backendConnected
            ? "bg-green-500/10 text-green-600 dark:text-green-400 border border-green-500/20"
            : "bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20"
            }`}>
            <span className={`w-2 h-2 rounded-full ${backendConnected ? "bg-green-500" : "bg-amber-500"}`} />
            {backendConnected ? "Backend Connected" : "Offline Mode"}
          </div>
        </div>
      )}

      <main className="container mx-auto px-4 py-12 max-w-3xl">
        <Header />

        <div className="space-y-8">
          <InputForm onSubmit={handleSubmit} isLoading={isLoading} />

          {roadmap && (
            <>
              <ResultCard roadmap={roadmap} />

              {originalQuery && (
                <FirEmailForm query={originalQuery} />
              )}
            </>
          )}
        </div>

        <footer className="mt-16 text-center text-sm text-muted-foreground">
          <p>🇮🇳 Built for the citizens of India</p>
          <p className="mt-2">AI for Trust & Transparency • Legal AI Track</p>
        </footer>
      </main>
    </div>
  );
}