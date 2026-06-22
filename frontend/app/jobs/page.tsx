"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Briefcase, Search, Plus, ExternalLink, Loader2 } from "lucide-react";
import { jobsApi, Job, ScrapeRequest } from "@/lib/api";

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [scraping, setScraping] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [scrapeForm, setScrapeForm] = useState<ScrapeRequest>({
    search_query: "Software Engineer",
    location: "India",
  });

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await jobsApi.getAll();
      setJobs(response.data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch jobs. Please check if the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleScrapeJobs = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setScraping(true);
      setError(null);
      await jobsApi.scrape(scrapeForm);
      setTimeout(() => {
        fetchJobs();
        setScraping(false);
      }, 3000);
    } catch (err) {
      console.error("Failed to scrape jobs:", err);
      setError("Failed to initiate job scraping. Please try again.");
      setScraping(false);
    }
  };

  const filteredJobs = jobs.filter(
    (job) =>
      job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (job.location && job.location.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Jobs</h2>
          <p className="text-muted-foreground">
            Track and scrape job opportunities
          </p>
        </div>
        <Dialog>
          <DialogTrigger className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">
            <Plus className="mr-2 h-4 w-4" />
            Scrape Jobs
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Scrape New Jobs</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleScrapeJobs} className="space-y-4">
              <div>
                <label className="text-sm font-medium">Search Query</label>
                <Input
                  required
                  value={scrapeForm.search_query}
                  onChange={(e) =>
                    setScrapeForm({ ...scrapeForm, search_query: e.target.value })
                  }
                  placeholder="e.g., AI ML Engineer, Software Engineer"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Location</label>
                <Input
                  required
                  value={scrapeForm.location}
                  onChange={(e) =>
                    setScrapeForm({ ...scrapeForm, location: e.target.value })
                  }
                  placeholder="e.g., Remote, India, Gurugram"
                />
              </div>
              <Button type="submit" className="w-full" disabled={scraping}>
                {scraping ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Scraping...
                  </>
                ) : (
                  "Start Scraping"
                )}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Briefcase className="h-5 w-5" />
              Active Listings ({filteredJobs.length})
            </CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search jobs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : filteredJobs.length === 0 ? (
            <div className="py-12 text-center">
              <Briefcase className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-4 text-lg font-semibold">No jobs found</h3>
              <p className="text-sm text-muted-foreground">
                {searchTerm
                  ? "Try adjusting your search"
                  : "Scrape jobs to get started"}
              </p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Title</TableHead>
                  <TableHead>Company</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead className="text-center">Apply</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredJobs.map((job) => (
                  <TableRow key={job.id}>
                    <TableCell className="font-medium max-w-md">
                      {job.title}
                    </TableCell>
                    <TableCell>
                      <Badge variant="secondary">{job.company}</Badge>
                    </TableCell>
                    <TableCell>{job.location || "Remote"}</TableCell>
                    <TableCell className="text-center">
                      {job.apply_link ? (
                        <a
                          href={job.apply_link}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <Button variant="ghost" size="icon">
                            <ExternalLink className="h-4 w-4" />
                          </Button>
                        </a>
                      ) : (
                        <span className="text-xs text-muted-foreground">N/A</span>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}