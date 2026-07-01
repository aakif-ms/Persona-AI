import { Card, CardHeader, CardTitle, CardContent } from "../ui/card";

export default function MemoryViewer() {
    const relationships = [
        {source: "USER", relation: "WEAK_AI", target: "DSA"},
        {source: "USER", relation: "INTERVIEWING_WITH", target: "Google"},
    ];

    return(
        <Card className="col-span-1">
            <CardHeader>
                <CardTitle>Sematic Memory (Graph)</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-2 text-sm font-mono bg-slate-950 text-slate-50 p-4 rounded-md">
                    {relationships.map((rel, i) => (
                        <div key={i}>
                            <span className="text-blue-400">{rel.source}</span>
                            <span className="text-green-400">{rel.relation}</span>
                            <span className="text-yellow-400">{rel.target}</span>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}