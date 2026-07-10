"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

const EVENTS_ENDPOINT = "/api/backend/events";

export default function ActivityFeed() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await fetch(EVENTS_ENDPOINT);

        if (!res.ok) {
          throw new Error(`Request failed with status ${res.status}`);
        }

        const data = await res.json();
        setEvents(data.events);
      } catch (error) {
        console.error("Failed to fetch events", error);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 30000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="col-span-1">
      <CardHeader>
        <CardTitle>Activity Feed</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-75 w-full pr-4">
          <div className="space-y-4">
            {events.map((evt) => (
              <div key={evt.id} className="flex flex-col space-y-1 border-b pb-2">
                <div className="flex items-center justify-between">
                  <Badge variant="outline">{evt.event_type}</Badge>
                  <span className="text-xs text-muted-foreground">
                    {new Date(evt.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <span className="text-sm">{evt.description}</span>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}