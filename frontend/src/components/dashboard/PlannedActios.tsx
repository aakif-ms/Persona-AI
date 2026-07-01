import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function PlannedActions() {
    const actions = [
        "Research Interview process",
        "Schedule preparation at 8 PM",
        "Send Telegram reminder"
    ];

    return (
        <Card className="col-span-1">
            <CardHeader>
                <CardTitle>Planned Actions (Goal: Prepare User)</CardTitle>
            </CardHeader>
            <CardContent>
                <ul className="list-disc pl-5 space-y-2 text-sm">
                    {actions.map((action, i) => (
                        <li key={i}>{action}</li>
                    ))}
                </ul>
            </CardContent>
        </Card>
    );
}