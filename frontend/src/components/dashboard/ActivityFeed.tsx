import { Card, CardHeader, CardTitle, CardContent } from "../ui/card";
import { ScrollArea } from "../ui/scroll-area";
import { Badge } from "../ui/badge";

export default function ActivityFeed() {
    const events = [
        {id: 1, type: "email_received", desc: "Mock Interview Scheduled for Tomorrow", time: "10 minutes ago"},
        {id: 2, type: "calendar_event_detected", desc: "Blocked 3 hours for prep", time: "2 mins ago"},
    ];

    return (
        <Card className="col-span-1">
            <CardHeader>
                <CardTitle>Actiity Feed</CardTitle>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-75 w-full pr-4">
                    <div className="space-y-4">
                        {events.map((evt) =>(
                            <div key={evt.id} className="flex flex-col space-y-1 border-b pb-2">
                                <div className="flex items-center justify-between">
                                    <Badge variant="outline">{evt.type}</Badge>
                                    <span className="text-xs text-muted-foreground">{evt.time}</span>
                                </div>
                                <span className="text-sm">{evt.desc}</span>
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    );
}