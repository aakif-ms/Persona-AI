import ActivityFeed from "@/components/dashboard/ActivityFeed";
import MemoryViewer from "@/components/dashboard/MemoryViewer";
import PlannedActions from "@/components/dashboard/PlannedActios";
import AgentStatus from "@/components/dashboard/AgentStatus";

export default function Dashboard() {
  return (
    <main className="min-h-screen p-8 bg-slate-50 dark:bg-slate-900">
      <div className="max-w-6xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Persona AI Dashboard</h1>
          <p className="text-muted-foreground">Autonomous Digital Chief of Staff</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ActivityFeed />
          <MemoryViewer />
          <PlannedActions />
          <AgentStatus />
        </div>
      </div>
    </main>
  );
}