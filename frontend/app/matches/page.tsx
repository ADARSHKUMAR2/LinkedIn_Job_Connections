"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Target,
  Search,
  Sparkles,
  Loader2,
  Mail,
  Building2,
  MapPin,
  User,
  Copy,
  Check,
  ExternalLink,
} from "lucide-react";
import { matchesApi, connectionsApi, jobsApi, Match, Connection, Job } from "@/lib/api";

export default function MatchesPage() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(false);
  const [sweeping, setSweeping] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [connectionsCount, setConnectionsCount] = useState(0);
  const [jobsCount, setJobsCount] = useState(0);

  // Outreach dialog state
  const [selectedMatch, setSelectedMatch] = useState<Match | null>(null);
  const [outreachDraft, setOutreachDraft] = useState<{ subject_line: string | null; message_body: string } | null>(null);
  const [drafting, setDrafting] = useState(false);
  const [copied, setCopied] = useState(false);

  // Filter state
  const [filters, setFilters] = useState({
    target_location: "",
    target_company: "",
    min_connections: 1,
  });

  useEffect(() => {
    fetchCounts();
  }, []);

  const fetchCounts = async () => {
    try {
      const [connRes, jobRes] = await Promise.all([
        connectionsApi.getAll(),
        jobsApi.getAll(),
      ]);
      setConnectionsCount(connRes.data.length);
      setJobsCount(jobRes.data.length);
    } catch (err) {
      console.error("Failed to fetch counts:", err);
    }
  };

  const handleRunSweep = async () => {
    try {
      setSweeping(true);
      setError(null);
      const filterPayload = {
        ...(filters.target_location && { target_location: filters.target_location }),
        ...(filters.target_company && { target_company: filters.target_company }),
        min_connections: filters.min_connections,
      };
      const response = await matchesApi.sweep(filterPayload);
      setMatches(response.data);
    } catch (err) {
      console.error("Failed to run match sweep:", err);
      setError("Failed to run AI matching. Check backend and try again.");
    } finally {
      setSweeping(false);
    }
  };

  const handleDraftOutreach = async (match: Match) => {
    try {
      setDrafting(true);
      setSelectedMatch(match);
      setCopied(false);
      const response = await matchesApi.draftOutreach(match);
      setOutreachDraft(response.data);
    } catch (err) {
      console.error("Failed to draft outreach:", err);
      setError("Failed to generate outreach draft. Please try again.");
    } finally {
      setDrafting(false);
    }
  };

  const handleCopyMessage = () => {
    if (outreachDraft) {
      const text = outreachDraft.subject_line
        ? `Subject: ${outreachDraft.subject_line}\n\n${outreachDraft.message_body}`
        : outreachDraft.message_body;
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const filteredMatches = matches.filter(
    (m) =>
      m.Company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      m["Target Role"].toLowerCase().includes(searchTerm.toLowerCase()) ||
      m["Inside Contact"].toLowerCase().includes(searchTerm.toLowerCase()) ||
      m.Location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const companyStats = matches.reduce((acc: Record<string, number>, m) => {
    acc[m.Company] = (acc[m.Company] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">AI Matchmaker</h2>
          <p className="text-muted-foreground">
            Semantic analysis for referral pathways and outreach
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Badge variant="secondary">{connectionsCount} connections</Badge>
          <Badge variant="secondary">{jobsCount} jobs</Badge>
        </div>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Matching Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <label className="text-sm font-medium mb-1 block">
                Target Location
              </label>
              <Input
                placeholder="e.g., Gurugram, Remote"
                value={filters.target_location}
                onChange={(e) =>
                  setFilters({ ...filters, target_location: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">
                Target Company
              </label>
              <Input
                placeholder="e.g., Google, Microsoft"
                value={filters.target_company}
                onChange={(e) =>
                  setFilters({ ...filters, target_company: e.target.value })
                }
              />
            </div>
            <div className="flex items-end">
              <Button
                onClick={handleRunSweep}
                disabled={sweeping}
                className="w-full"
                size="lg"
              >
                {sweeping ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Target className="mr-2 h-5 w-5" />
                    Run AI Match Sweep
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {matches.length > 0 && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Matches</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{matches.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Companies</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {Object.keys(companyStats).length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Unique Contacts</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {new Set(matches.map((m) => m["Inside Contact"])).size}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Unique Roles</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {new Set(matches.map((m) => m["Target Role"])).size}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Match Results {matches.length > 0 && `(${filteredMatches.length})`}
            </CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search matches..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {sweeping ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <Skeleton key={i} className="h-24 w-full" />
              ))}
            </div>
          ) : filteredMatches.length === 0 ? (
            <div className="py-12 text-center">
              <Target className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-4 text-lg font-semibold">No matches yet</h3>
              <p className="text-sm text-muted-foreground">
                {searchTerm
                  ? "Try adjusting your search"
                  : "Configure filters and run an AI match sweep to discover referral pathways"}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredMatches.map((match, index) => (
                <Card key={index}>
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="space-y-2 flex-1">
                        <div className="flex items-center gap-2">
                          <Building2 className="h-4 w-4 text-primary" />
                          <span className="font-semibold">{match.Company}</span>
                          <Badge variant="outline">{match["Target Role"]}</Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {match["Inside Contact"]}
                          </span>
                          <span className="text-xs">
                            ({match["Contact Position"]})
                          </span>
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {match.Location}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {match["Application Link"] !== "No Link Available" && (
                          <a
                            href={match["Application Link"]}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            <Button variant="outline" size="sm">
                              <ExternalLink className="mr-1 h-3 w-3" />
                              Apply
                            </Button>
                          </a>
                        )}
                        <Dialog>
                          <DialogTrigger
                            className="inline-flex items-center justify-center rounded-md bg-primary px-3 py-1.5 text-sm font-medium text-primary-foreground shadow hover:bg-primary/90"
                            onClick={() => handleDraftOutreach(match)}
                          >
                            <Mail className="mr-1 h-3 w-3" />
                            Draft
                          </DialogTrigger>
                          <DialogContent className="max-w-2xl">
                            <DialogHeader>
                              <DialogTitle>
                                Outreach Draft for {match["Inside Contact"]}
                              </DialogTitle>
                            </DialogHeader>
                            {drafting ? (
                              <div className="flex items-center justify-center py-12">
                                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                                <span className="ml-2 text-muted-foreground">
                                  AI is crafting your message...
                                </span>
                              </div>
                            ) : outreachDraft ? (
                              <div className="space-y-4">
                                <div className="rounded-lg border bg-muted p-4">
                                  <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium">
                                      Match Context
                                    </span>
                                  </div>
                                  <div className="grid grid-cols-2 gap-2 text-sm">
                                    <div>
                                      <span className="text-muted-foreground">Contact: </span>
                                      {match["Inside Contact"]}
                                    </div>
                                    <div>
                                      <span className="text-muted-foreground">Role: </span>
                                      {match["Contact Position"]}
                                    </div>
                                    <div>
                                      <span className="text-muted-foreground">Company: </span>
                                      {match.Company}
                                    </div>
                                    <div>
                                      <span className="text-muted-foreground">Target: </span>
                                      {match["Target Role"]}
                                    </div>
                                  </div>
                                </div>
                                {outreachDraft.subject_line && (
                                  <div>
                                    <label className="text-sm font-medium">
                                      Subject Line
                                    </label>
                                    <Input
                                      value={outreachDraft.subject_line}
                                      readOnly
                                      className="mt-1"
                                    />
                                  </div>
                                )}
                                <div>
                                  <label className="text-sm font-medium">
                                    Message Body
                                  </label>
                                  <Textarea
                                    value={outreachDraft.message_body}
                                    readOnly
                                    rows={8}
                                    className="mt-1"
                                  />
                                </div>
                                <Button
                                  onClick={handleCopyMessage}
                                  className="w-full"
                                >
                                  {copied ? (
                                    <>
                                      <Check className="mr-2 h-4 w-4" />
                                      Copied!
                                    </>
                                  ) : (
                                    <>
                                      <Copy className="mr-2 h-4 w-4" />
                                      Copy to Clipboard
                                    </>
                                  )}
                                </Button>
                              </div>
                            ) : (
                              <div className="py-12 text-center text-muted-foreground">
                                Failed to generate draft. Please try again.
                              </div>
                            )}
                          </DialogContent>
                        </Dialog>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {matches.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Company Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              {Object.entries(companyStats)
                .sort(([, a], [, b]) => b - a)
                .map(([company, count]) => (
                  <div
                    key={company}
                    className="flex items-center justify-between rounded-lg border p-3"
                  >
                    <span className="text-sm font-medium">{company}</span>
                    <Badge>{count} match{count > 1 ? "es" : ""}</Badge>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}