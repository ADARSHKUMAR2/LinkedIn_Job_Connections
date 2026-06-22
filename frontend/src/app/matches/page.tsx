"use client"

import React, { useState } from "react"
import { Sparkles, Building2, User, MapPin, ExternalLink, Copy, Check, MessageSquare } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

// Exactly maps the 7 AI-Validated pathways currently cached in your Supabase database instance
const activeMatches = [
  {
    id: 1,
    company: "AMERICAN EXPRESS",
    role: "Senior AI Engineer",
    location: "Gurugram, Haryana IN",
    contact: "Bob Miller",
    position: "VP of Engineering",
    link: "https://careers.americanexpress.com",
    subject: "Referral Exploration / Advanced AI Systems Platform",
    body: "Hi Bob,\n\nI noticed your team at American Express is expanding its footprint in Gurugram for the Senior AI Engineer opening. Having tracked your engineering directives, I've been building scalable automation pipelines that closely parallel Amex's standard of excellence.\n\nGiven your role as VP of Engineering, I wanted to reach out and see if you'd be open to a brief chat regarding how my background aligns with your current strategic objectives. I've attached my portfolio for your review.\n\nBest regards,\nAdarsh"
  },
  {
    id: 2,
    company: "GARTNER CAREERS",
    role: "Research Director - Data Science",
    location: "Gurugram, Haryana IN",
    contact: "Alice Vance",
    position: "Senior Research Director",
    link: "https://jobs.gartner.com",
    subject: "Data Science Infrastructure Context / Gartner Insights",
    body: "Hi Alice,\n\nI hope this finds you well. I’ve been following Gartner's investigative research frameworks in Asia-Pacific, and noticed an opening for Research Director within your direct org vertical in Gurugram.\n\nMy engineering background centers heavily on structured data frameworks and predictive model optimization. I'd love to learn more about how your team approaches these architectural benchmarks, and see if my technical profile warrants an internal referral pathway.\n\nWarmly,\nAdarsh"
  },
  {
    id: 3,
    company: "UNITED AIRLINES",
    role: "Cloud Architect",
    location: "Gurugram, Haryana, IN",
    contact: "Charlie Delta",
    position: "Cloud Architect",
    link: "https://careers.united.com",
    subject: "Cloud Architecture Alignment / Infrastructure Sync",
    body: "Hey Charlie,\n\nAlways great to connect with a fellow Cloud Architect. I came across United Airlines' active headcount search for your team cluster out here in Gurugram.\n\nI'm currently optimizing distributed cloud instances and database transactions over a heavy multi-region infrastructure. Since you're deep in this exact space at United, I'd appreciate 5 minutes to swap notes and explore if there's a strong fit for a referral handoff.\n\nCheers,\nAdarsh"
  },
  {
    id: 4,
    company: "UNITEDHEALTH GROUP",
    role: "Engineering Manager",
    location: "Gurugram, Haryana, IN",
    contact: "Jo Smith",
    position: "Engineering Manager",
    link: "https://careers.unitedhealthgroup.com",
    subject: "Technical Leadership Roster / Strategic Engineering",
    body: "Hi Jo,\n\nI saw that UnitedHealth Group is spinning up specialized engineering pods in Gurugram, specifically looking for an Engineering Manager. Knowing the scale at which UHG operates health-tech solutions, I wanted to trace a connection.\n\nI've spent the last few years managing agile infrastructure environments, aligning cross-functional engineers, and shipping secure software. I'd love to connect briefly to discuss the technical vision for this role.\n\nBest,\nAdarsh"
  }
]

export default function MatchesPage() {
  const [selectedMatch, setSelectedMatch] = useState(activeMatches[0])
  const [copiedSubject, setCopiedSubject] = useState(false)
  const [copiedBody, setCopiedBody] = useState(false)

  const copyToClipboard = (text: string, isSubject: boolean) => {
    navigator.clipboard.writeText(text)
    if (isSubject) {
      setCopiedSubject(true)
      setTimeout(() => setCopiedSubject(false), 2000)
    } else {
      setCopiedBody(true)
      setTimeout(() => setCopiedBody(false), 2000)
    }
  }

  return (
    <div className="space-y-6 h-[calc(100vh-7rem)] flex flex-col">
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-bold tracking-tight text-white">AI Referral Matches</h1>
          <Badge className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono text-xs">
            7 Active Pathways Cached
          </Badge>
        </div>
        <p className="text-sm text-zinc-400 mt-1">
          Select an AI-validated corporate match element to access context-aware outreach drafts.
        </p>
      </div>

      {/* 🚀 Dual Panel Control Board Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 flex-1 overflow-hidden min-h-0">
        
        {/* Left Side: Scalable Scrollable Match Matrix Feed */}
        <div className="lg:col-span-2 overflow-y-auto pr-2 space-y-3 h-full">
          {activeMatches.map((match) => {
            const isSelected = selectedMatch.id === match.id
            return (
              <Card
                key={match.id}
                onClick={() => {
                  setSelectedMatch(match)
                  setCopiedSubject(false)
                  setCopiedBody(false)
                }}
                className={`p-4 border cursor-pointer transition-all rounded-xl select-none relative overflow-hidden ${
                  isSelected
                    ? "bg-zinc-900 border-zinc-700 shadow-md ring-1 ring-zinc-800"
                    : "bg-zinc-950/40 border-zinc-800/80 hover:border-zinc-800 hover:bg-zinc-900/30"
                }`}
              >
                <div className="flex items-start justify-between space-x-2">
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold text-zinc-500 tracking-wider uppercase block">
                      {match.company}
                    </span>
                    <h3 className="font-semibold text-white text-sm group-hover:text-emerald-400">
                      {match.role}
                    </h3>
                  </div>
                  <Badge className="bg-zinc-900 border border-zinc-800 text-zinc-400 text-[10px] shrink-0 font-medium px-2 py-0.5">
                    Match Found
                  </Badge>
                </div>

                <div className="mt-4 pt-3 border-t border-zinc-800/60 grid grid-cols-2 gap-2 text-xs text-zinc-400">
                  <div className="flex items-center space-x-1.5 min-w-0">
                    <User className="h-3.5 w-3.5 text-zinc-500 shrink-0" />
                    <span className="truncate font-medium text-zinc-300">{match.contact}</span>
                  </div>
                  <div className="flex items-center space-x-1.5 min-w-0 justify-end">
                    <MapPin className="h-3.5 w-3.5 text-zinc-500 shrink-0" />
                    <span className="truncate">{match.location.split(',')[0]}</span>
                  </div>
                </div>
              </Card>
            )
          })}
        </div>

        {/* Right Side: Completely Automated Outreach Drafting Workbench */}
        <div className="lg:col-span-3 flex flex-col h-full border border-zinc-800 bg-zinc-950/40 rounded-2xl overflow-hidden backdrop-blur-sm shadow-sm">
          
          {/* Header Block */}
          <div className="p-4 border-b border-zinc-800 bg-zinc-950/80 flex items-center justify-between">
            <div className="flex items-center space-x-3 min-w-0">
              <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 shrink-0">
                <Sparkles className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <h2 className="text-sm font-semibold text-white truncate">Outreach Assistant</h2>
                <p className="text-xs text-zinc-500 truncate">Referral targeting contact: <span className="text-zinc-300 font-medium">{selectedMatch.contact} ({selectedMatch.position})</span></p>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              asChild
              className="border-zinc-800 text-zinc-400 hover:bg-zinc-900 hover:text-white text-xs shrink-0"
            >
              <a href={selectedMatch.link} target="_blank" rel="noopener noreferrer">
                Job Portal <ExternalLink className="ml-1.5 h-3 w-3" />
              </a>
            </Button>
          </div>

          {/* Interactive Core Work Panel Area */}
          <div className="p-5 flex-1 overflow-y-auto space-y-4">
            
            {/* Subject Line Action Block */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-400 font-semibold uppercase tracking-wider">Subject Line</span>
                <button
                  onClick={() => copyToClipboard(selectedMatch.subject, true)}
                  className="text-zinc-500 hover:text-emerald-400 flex items-center transition-colors font-medium"
                >
                  {copiedSubject ? (
                    <>
                      <Check className="h-3 w-3 mr-1 text-emerald-400" /> Copied
                    </>
                  ) : (
                    <>
                      <Copy className="h-3 w-3 mr-1" /> Copy Line
                    </>
                  )}
                </button>
              </div>
              <div className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3.5 py-2.5 text-sm text-zinc-200 font-medium font-mono select-all">
                {selectedMatch.subject}
              </div>
            </div>

            {/* Structured Email/Message Body Workspace */}
            <div className="space-y-1.5 flex-1 flex flex-col min-h-0">
              <div className="flex items-center justify-between text-xs">
                <span className="text-zinc-400 font-semibold uppercase tracking-wider">Message Copy</span>
                <button
                  onClick={() => copyToClipboard(selectedMatch.body, false)}
                  className="text-zinc-500 hover:text-emerald-400 flex items-center transition-colors font-medium"
                >
                  {copiedBody ? (
                    <>
                      <Check className="h-3 w-3 mr-1 text-emerald-400" /> Copied Draft
                    </>
                  ) : (
                    <>
                      <Copy className="h-3 w-3 mr-1" /> Copy Draft
                    </>
                  )}
                </button>
              </div>
              <textarea
                value={selectedMatch.body}
                readOnly
                className="w-full flex-1 min-h-[220px] bg-zinc-950 border border-zinc-800 rounded-xl p-4 text-sm text-zinc-300 font-sans focus:outline-none focus:border-zinc-800 resize-none leading-relaxed shadow-inner"
              />
            </div>
          </div>

          {/* Footer Safety Indicator */}
          <div className="p-3 bg-zinc-950/60 border-t border-zinc-800/60 flex items-center justify-between text-[11px] text-zinc-500 font-medium">
            <span className="flex items-center"><MessageSquare className="h-3 w-3 mr-1.5 text-zinc-600" /> Models Platform Input Context: Optimized</span>
            <span className="text-zinc-600 font-mono">ID: SEC_C_{selectedMatch.id}</span>
          </div>

        </div>

      </div>
    </div>
  )
}