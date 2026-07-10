"use client";

import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const SEMANTIC_MEMORY_ENDPOINT = "/api/backend/memory/semantic";

export default function MemoryViewer() {
  const [relationships, setRelationships] = useState<any[]>([]);

  useEffect(() => {
    const fetchMemory = async () => {
      try {
        const res = await fetch(SEMANTIC_MEMORY_ENDPOINT);

        if (!res.ok) {
          throw new Error(`Request failed with status ${res.status}`);
        }

        const data = await res.json();
        setRelationships(data.relationships);
      } catch (error) {
        console.error("Failed to fetch semantic memory", error);
      }
    };

    fetchMemory();
    const interval = setInterval(fetchMemory, 30000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="col-span-1">
      <CardHeader>
        <CardTitle>Semantic Memory (Graph)</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-sm font-mono bg-slate-950 text-slate-50 p-4 rounded-md h-75 overflow-y-auto">
          {relationships.map((rel, i) => (
            <div key={i}>
              <span className="text-blue-400">{rel.source}</span>{" "}
              <span className="text-green-400">→ {rel.relation} →</span>{" "}
              <span className="text-yellow-400">{rel.target}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}