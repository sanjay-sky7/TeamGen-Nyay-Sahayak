"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Copy, Check, Download, Share2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import type { LegalRoadmap } from "@/lib/api/nyay-sahayak";

interface ResultCardProps {
  roadmap: LegalRoadmap;
}

export const ResultCard = ({ roadmap }: ResultCardProps) => {
  const [copied, setCopied] = useState(false);

  const getRoadmapText = () => {
    return `NYAY SAHAYAK - LEGAL ROADMAP

Crime Type: ${roadmap.crime_type}

Immediate Actions:
${roadmap.immediate_actions.map((action, i) => `${i + 1}. ${action}`).join("\n")}

FIR Steps:
${roadmap.fir_steps.map((step, i) => `${i + 1}. ${step}`).join("\n")}

Evidence to Preserve:
${roadmap.evidence_to_preserve.map((evidence, i) => `${i + 1}. ${evidence}`).join("\n")}

Relevant Laws:
${roadmap.relevant_laws.map((law, i) => `${i + 1}. ${law}`).join("\n")}

⚖️ Disclaimer: This tool is for informational purposes only and does not constitute legal advice.`;
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(getRoadmapText());
      setCopied(true);
      toast.success("Roadmap copied to clipboard!");
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error("Failed to copy to clipboard");
    }
  };

  const handleDownload = () => {
    const text = getRoadmapText();
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `legal-roadmap-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("Roadmap downloaded!");
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: "Nyay Sahayak - Legal Roadmap",
          text: getRoadmapText(),
        });
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          toast.error("Failed to share");
        }
      }
    } else {
      handleCopy();
    }
  };

  return (
    <Card className="shadow-lg border-border/50 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0 pb-4">
        <CardTitle className="text-2xl font-semibold">Your Legal Roadmap</CardTitle>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="gap-2"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4" />
                <span className="hidden sm:inline">Copied</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                <span className="hidden sm:inline">Copy</span>
              </>
            )}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleDownload}
            className="gap-2"
          >
            <Download className="h-4 w-4" />
            <span className="hidden sm:inline">Download</span>
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleShare}
            className="gap-2"
          >
            <Share2 className="h-4 w-4" />
            <span className="hidden sm:inline">Share</span>
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-foreground">Crime Type</h3>
          <p className="text-muted-foreground bg-muted/50 p-3 rounded-lg">
            {roadmap.crime_type}
          </p>
        </div>

        <div className="border-t pt-6 space-y-2">
          <h3 className="text-lg font-semibold text-foreground">
            Immediate Actions
          </h3>
          <ul className="space-y-2 list-disc list-inside text-muted-foreground">
            {roadmap.immediate_actions.map((action, index) => (
              <li key={index} className="leading-relaxed">
                {action}
              </li>
            ))}
          </ul>
        </div>

        <div className="border-t pt-6 space-y-2">
          <h3 className="text-lg font-semibold text-foreground">FIR Steps</h3>
          <ul className="space-y-2 list-disc list-inside text-muted-foreground">
            {roadmap.fir_steps.map((step, index) => (
              <li key={index} className="leading-relaxed">
                {step}
              </li>
            ))}
          </ul>
        </div>

        <div className="border-t pt-6 space-y-2">
          <h3 className="text-lg font-semibold text-foreground">
            Evidence to Preserve
          </h3>
          <ul className="space-y-2 list-disc list-inside text-muted-foreground">
            {roadmap.evidence_to_preserve.map((evidence, index) => (
              <li key={index} className="leading-relaxed">
                {evidence}
              </li>
            ))}
          </ul>
        </div>

        <div className="border-t pt-6 space-y-2">
          <h3 className="text-lg font-semibold text-foreground">
            Relevant Laws
          </h3>
          <ul className="space-y-2 list-disc list-inside text-muted-foreground">
            {roadmap.relevant_laws.map((law, index) => (
              <li key={index} className="leading-relaxed">
                {law}
              </li>
            ))}
          </ul>
        </div>

        <div className="border-t pt-6">
          <p className="text-sm text-muted-foreground text-center italic">
            ⚖️ Disclaimer: This tool is for informational purposes only and does
            not constitute legal advice.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};