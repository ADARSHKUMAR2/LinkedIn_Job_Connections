"use client"

import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown, CheckCircle2, XCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

// Define the data model structure matching your backend
export type ConnectionRecord = {
  id: number
  name: string
  company: string
  position: string
  hasReferralPipeline: boolean // Highlights high-intent corporate ties
}

export const columns: ColumnDef<ConnectionRecord>[] = [
  {
    accessorKey: "name",
    header: "Full Name",
    cell: ({ row }) => <span className="font-semibold text-white">{row.getValue("name")}</span>,
  },
  {
    accessorKey: "company",
    header: ({ column }) => (
      <Button 
        variant="ghost" 
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        className="hover:bg-zinc-800 text-zinc-400 font-medium -ml-4"
      >
        Company
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => <span className="text-zinc-300 font-medium">{row.getValue("company")}</span>,
  },
  {
    accessorKey: "position",
    header: "Role / Position",
    cell: ({ row }) => <span className="text-zinc-400 text-sm">{row.getValue("position")}</span>,
  },
  {
    accessorKey: "hasReferralPipeline",
    header: "Referral Link Status",
    cell: ({ row }) => {
      const hasPipeline = row.getValue("hasReferralPipeline") as boolean
      return hasPipeline ? (
        <Badge className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-1 rounded-full flex items-center space-x-1 w-fit">
          <CheckCircle2 className="h-3 w-3 mr-1 text-emerald-400" />
          Active Referral Pipeline
        </Badge>
      ) : (
        <Badge className="bg-zinc-800/40 text-zinc-500 border border-zinc-800 px-2 py-1 rounded-full flex items-center space-x-1 w-fit">
          <XCircle className="h-3 w-3 mr-1 text-zinc-600" />
          Standard Contact
        </Badge>
      )
    },
  },
]