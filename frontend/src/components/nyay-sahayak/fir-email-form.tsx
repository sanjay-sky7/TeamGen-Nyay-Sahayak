"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Mail, Send, Loader2, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";
import { sendFirEmail } from "@/lib/api/nyay-sahayak";

interface FirEmailFormProps {
  query: string;
}

export const FirEmailForm = ({ query }: FirEmailFormProps) => {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSent, setIsSent] = useState(false);

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email.trim()) {
      toast.error("Please enter your email address");
      return;
    }

    if (!validateEmail(email)) {
      toast.error("Please enter a valid email address");
      return;
    }

    setIsLoading(true);

    try {
      await sendFirEmail(query, email.trim());
      setIsSent(true);
      toast.success("FIR draft sent to your email successfully!");
    } catch (error) {
      console.error("Failed to send FIR email:", error);
      const errorMessage = error instanceof Error ? error.message : "Failed to send email";
      toast.error(`Failed to send FIR email: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSent) {
    return (
      <Card className="shadow-lg border-border/50 bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800">
        <CardContent className="pt-6">
          <div className="flex items-center gap-3 text-green-700 dark:text-green-400">
            <CheckCircle2 className="h-5 w-5" />
            <div>
              <p className="font-medium">FIR draft sent successfully!</p>
              <p className="text-sm text-green-600 dark:text-green-500 mt-1">
                Please check your email at <span className="font-semibold">{email}</span>
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg border-border/50">
      <CardHeader>
        <CardTitle className="text-xl font-semibold flex items-center gap-2">
          <Mail className="h-5 w-5" />
          Get FIR Draft via Email
        </CardTitle>
        <CardDescription>
          Enter your email address to receive a draft of the FIR (First Information Report) based on your query.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-base font-medium">
              Email Address <span className="text-destructive">*</span>
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="your-email@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground">
              We'll send the FIR draft to this email address. Your email will only be used for this purpose.
            </p>
          </div>

          <Button
            type="submit"
            disabled={isLoading || !email.trim()}
            className="w-full gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Sending FIR draft...
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                Send FIR Draft to Email
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

