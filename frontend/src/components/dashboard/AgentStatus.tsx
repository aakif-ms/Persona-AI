import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "../ui/badge";

export default function AgentStatus() {
    const agents = [
        {name: "Research Agent", status: "Completed"},
        {name: "Scheduler Agent", status: "Running"},
        {name: "Reminder Agent", status: "Waiting"},
    ];

    return (
        <Card className="col-span-1">
            <CardHeader>
                <CardTitle>Agent Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {agents.map((agent, i) => (
                    <div key={i} className="flex justify-between items-center">
                        <span className="text-sm font-medium">{agent.name}</span>
                        <Badge variant={agent.status === 'Completed' ? 'default' : agent.status === 'Running' ? 'secondary' : 'outline'}>{agent.status}
                        </Badge>
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}