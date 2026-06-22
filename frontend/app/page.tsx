"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Briefcase, Target, TrendingUp, RefreshCw, WifiOff } from "lucide-react";
import { connectionsApi, jobsApi } from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription } from "@/components/ui/alert";
import api from "@/lib/api";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    connections: 0,
    jobs: 0,
    matches: 0,
    loading: true,
  });
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);

  const checkBackendHealth = async () => {
    try {
      await api.get("/");
      setBackendOnline(true);
      return true;
    } catch {
      setBackendOnline(false);
      return false;
    }
  };

  const fetchStats = async () => {
    setStats((prev) => ({ ...prev, loading: true }));
    setError(null);
    
    const isOnline = await checkBackendHealth();
    if (!isOnline) {
      setStats((prev) => ({ ...prev, loading: false }));
      setError("Cannot connect to the backend server. Please ensure the FastAPI server is running on port 8000.");
      return;
    }

    try {
      const [connectionsRes, jobsRes] = await Promise.all([
        connectionsApi.getAll(),
        jobsApi.getAll(),
      ]);

      setStats({
        connections: connectionsRes.data.length,
        jobs: jobsRes.data.length,
        matches: 0,
        loading: false,
      });
      setError(null);
    } catch (err: any) {
      console.error("Failed to fetch stats:", err);
      setError(err?.message || "Failed to fetch data from the backend.");
      setStats((prev) => ({ ...prev, loading: false }));
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const statCards = [
    {
      title: "Total Connections",
      value: stats.connections,
      icon: Users,
      description: "LinkedIn network contacts",
      color: "text-blue-600",
    },
    {
      title: "Active Jobs",
      value: stats.jobs,
      icon: Briefcase,
      description: "Tracked opportunities",
      color: "text-green-600",
    },
    {
      title: "AI Matches",
      value: stats.matches,
      icon: Target,
      description: "Referral pathways found",
      color: "text-purple-600",
    },
    {
      title: "Success Rate",
      value: stats.jobs > 0 ? Math.round((stats.matches / stats.jobs) * 100) : 0,
      icon: TrendingUp,
      description: "Match percentage",
      color: "text-orange-600",
      suffix: "%",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Your AI-powered job hunting intelligence center
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchStats} disabled={stats.loading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${stats.loading ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      {error && (
        <Alert variant={backendOnline === false ? "default" : "destructive"}>
          <WifiOff className="h-4 w-4" />
          <AlertDescription>
            {backendOnline === false ? (
              <div className="flex items-center justify-between">
                <span>
                  Cannot connect to the backend server. Make sure the FastAPI server is running at{" "}
                  <code className="rounded bg-muted px-1 py-0.5 text-sm font-mono">
                    http://localhost:8000
                  </code>
                </span>
                <Button variant="outline" size="sm" onClick={fetchStats}>
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Retry
                </Button>
              </div>
            ) : (
              error
            )}
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              {stats.loading ? (
                <Skeleton className="h-8 w-20" />
              ) : (
                <div className="text-2xl font-bold">
                  {stat.value}
                  {stat.suffix}
                </div>
              )}
              <p className="text-xs text-muted-foreground">
                {stat.description}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <a
              href="/connections"
              className="block rounded-lg border p-4 transition-colors hover:bg-accent"
            >
              <h3 className="font-semibold">Manage Connections</h3>
              <p className="text-sm text-muted-foreground">
                View and organize your LinkedIn network
              </p>
            </a>
            <a
              href="/jobs"
              className="block rounded-lg border p-4 transition-colors hover:bg-accent"
            >
              <h3 className="font-semibold">Scrape Jobs</h3>
              <p className="text-sm text-muted-foreground">
                Fetch latest opportunities from JSearch API
              </p>
            </a>
            <a
              href="/matches"
              className="block rounded-lg border p-4 transition-colors hover:bg-accent"
            >
              <h3 className="font-semibold">Run AI Matching</h3>
              <p className="text-sm text-muted-foreground">
                Find referral pathways with semantic analysis
              </p>
            </a>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>System Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Backend API</span>
              <span className="flex items-center gap-2 text-sm">
                <span
                  className={`h-2 w-2 rounded-full ${
                    backendOnline === null
                      ? "bg-yellow-500"
                      : backendOnline
                      ? "bg-green-500"
                      : "bg-red-500"
                  }`}
                ></span>
                {backendOnline === null
                  ? "Checking..."
                  : backendOnline
                  ? "Online"
                  : "Offline"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Database</span>
              <span className="flex items-center gap-2 text-sm">
                <span
                  className={`h-2 w-2 rounded-full ${
                    backendOnline ? "bg-green-500" : "bg-gray-300"
                  }`}
                ></span>
                {backendOnline ? "Connected" : "Unknown"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">AI Engine</span>
              <span className="flex items-center gap-2 text-sm">
                <span
                  className={`h-2 w-2 rounded-full ${
                    backendOnline ? "bg-green-500" : "bg-gray-300"
                  }`}
                ></span>
                {backendOnline ? "Ready" : "Unknown"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Job Scraper</span>
              <span className="flex items-center gap-2 text-sm">
                <span
                  className={`h-2 w-2 rounded-full ${
                    backendOnline ? "bg-green-500" : "bg-gray-300"
                  }`}
                ></span>
                {backendOnline ? "Active" : "Unknown"}
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}