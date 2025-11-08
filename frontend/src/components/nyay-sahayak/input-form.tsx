"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, RotateCcw, Send } from "lucide-react";

interface InputFormProps {
  onSubmit: (data: {
    description: string;
    state?: string;
    incident_type?: string;
  }) => void;
  isLoading: boolean;
}

const incidentTypes = [
  "Theft",
  "Cyber Fraud",
  "Domestic Violence",
  "Assault",
  "Property Damage",
  "Harassment",
  "Other",
];

export const InputForm = ({ onSubmit, isLoading }: InputFormProps) => {
  const [description, setDescription] = useState("");
  const [state, setState] = useState("");
  const [incidentType, setIncidentType] = useState("");
  const descriptionRef = useRef<HTMLTextAreaElement>(null);

  // Auto-focus description field on mount
  useEffect(() => {
    descriptionRef.current?.focus();
  }, []);

  // Keyboard shortcut: Ctrl/Cmd + Enter to submit
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        if (description.trim() && !isLoading) {
          handleSubmit(e as any);
        }
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [description, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!description.trim()) return;

    onSubmit({
      description: description.trim(),
      state: state.trim() || undefined,
      incident_type: incidentType || undefined,
    });
  };

  const handleReset = () => {
    setDescription("");
    setState("");
    setIncidentType("");
    descriptionRef.current?.focus();
  };

  return (
    <Card className="shadow-lg border-border/50">
      <CardHeader>
        <CardTitle className="text-2xl font-semibold">
          Generate Legal Roadmap
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="description" className="text-base font-medium">
              Describe what happened <span className="text-destructive">*</span>
            </Label>
            <Textarea
              ref={descriptionRef}
              id="description"
              placeholder="e.g., Someone stole my phone while I was on the bus."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              rows={5}
              className="resize-none"
            />
            <p className="text-xs text-muted-foreground">
              💡 Be concise. Avoid sharing highly sensitive personal info.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="state" className="text-base font-medium">
                State / Jurisdiction (optional)
              </Label>
              <Input
                id="state"
                placeholder="e.g., Goa, Delhi"
                value={state}
                onChange={(e) => setState(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="incident-type" className="text-base font-medium">
                Incident type (optional)
              </Label>
              <Select value={incidentType} onValueChange={setIncidentType}>
                <SelectTrigger id="incident-type">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  {incidentTypes.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex gap-3">
            <Button
              type="submit"
              disabled={isLoading || !description.trim()}
              className="flex-1 gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Generating your roadmap...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Generate Roadmap
                  <span className="hidden sm:inline text-xs opacity-70 ml-1">
                    (Ctrl+Enter)
                  </span>
                </>
              )}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={handleReset}
              disabled={isLoading}
              className="gap-2"
            >
              <RotateCcw className="h-4 w-4" />
              <span className="hidden sm:inline">Reset</span>
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};