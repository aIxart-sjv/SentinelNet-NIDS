import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell,
  BarChart, Bar
} from "recharts";

interface Log {
  timestamp: string;
  prediction: string;
}

export default function App() {
  const [logs, setLogs] = useState<Log[]>([]);

  useEffect(() => {
    const fetchLogs = async () => {
      const res = await axios.get("http://localhost:8000/api/logs");
      setLogs(res.data);
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  const attacks = logs.filter(l => l.prediction === "ATTACK").length;
  const benign = logs.length - attacks;

  // timeline
  const grouped: any = {};
  logs.forEach(log => {
    const t = new Date(log.timestamp).toLocaleTimeString();
    if (!grouped[t]) grouped[t] = 0;
    if (log.prediction === "ATTACK") grouped[t]++;
  });

  const timelineData = Object.keys(grouped).map(t => ({
    time: t,
    attacks: grouped[t],
    benign: Math.floor(Math.random() * 5)
  }));

  const eventTypes = [
    { name: "normal", value: benign },
    { name: "dos", value: Math.floor(attacks * 0.4) },
    { name: "probe", value: Math.floor(attacks * 0.3) },
    { name: "r2l", value: Math.floor(attacks * 0.2) },
    { name: "u2r", value: Math.floor(attacks * 0.1) },
  ];

  const httpMethods = [
    { name: "GET", value: 70 },
    { name: "POST", value: 20 },
    { name: "PUT", value: 10 },
  ];

  const tlsVersions = [
    { name: "TLS 1.2", value: 80 },
    { name: "TLS 1.3", value: 20 },
  ];

  const dnsTypes = [
    { name: "A", value: 70 },
    { name: "AAAA", value: 20 },
    { name: "MX", value: 10 },
  ];

  const statusCodes = [
    { name: "200", value: 60 },
    { name: "404", value: 20 },
    { name: "500", value: 10 },
    { name: "302", value: 10 },
  ];

  return (
    <div className="min-h-screen bg-[#0b0f14] text-gray-300 p-4 text-sm">

      {/* HEADER */}
      <div className="flex justify-between mb-4">
        <h1 className="text-gray-200">SentinelNet SOC</h1>
        <span className="text-green-400 text-xs">● LIVE</span>
      </div>

      <div className="grid grid-cols-12 gap-3">

        {/* TIMELINE */}
        <Panel title="Events Over Time" className="col-span-8">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={timelineData}>
              <XAxis dataKey="time" stroke="#6b7280" fontSize={10} />
              <YAxis stroke="#6b7280" fontSize={10} />
              <Tooltip contentStyle={{ backgroundColor: "#11161c" }} />
              <Line type="monotone" dataKey="attacks" stroke="#4ade80" dot={false} />
              <Line type="monotone" dataKey="benign" stroke="#60a5fa" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </Panel>

        {/* ALERTS */}
        <Panel title="Alerts" className="col-span-2">
          <div className="text-red-400 text-lg">{attacks}</div>
          <div className="text-xs text-gray-500">Intrusions</div>
        </Panel>

        {/* TERMS */}
        <Panel title="Top Events" className="col-span-2">
          {eventTypes.map((e, i) => (
            <div key={i} className="flex justify-between text-xs">
              <span>{e.name}</span>
              <span>{e.value}</span>
            </div>
          ))}
        </Panel>

        {/* 🔥 DONUT GRID FIX */}
        <Panel title="Distributions" className="col-span-12">
          <div className="grid grid-cols-2 gap-4">

            <Donut title="Event Types" data={eventTypes} />
            <Donut title="HTTP Methods" data={httpMethods} />

            <Donut title="TLS Versions" data={tlsVersions} />
            <Donut title="DNS Types" data={dnsTypes} />

          </div>
        </Panel>

        {/* BAR */}
        <Panel title="HTTP Status Codes" className="col-span-4">
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={statusCodes}>
              <XAxis dataKey="name" stroke="#6b7280" fontSize={10} />
              <YAxis stroke="#6b7280" fontSize={10} />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </Panel>

        {/* USER AGENTS */}
        <Panel title="User Agents" className="col-span-4">
          <div className="text-xs space-y-2">
            <div>Mozilla Firefox — 240</div>
            <div>Chrome — 180</div>
            <div>curl — 60</div>
          </div>
        </Panel>

        {/* TLS SUBJECT */}
        <Panel title="TLS Subjects" className="col-span-4">
          <div className="text-xs space-y-2">
            <div>CN=google.com</div>
            <div>CN=facebook.com</div>
            <div>CN=twitter.com</div>
          </div>
        </Panel>

      </div>
    </div>
  );
}

/* DONUT COMPONENT */
function Donut({ title, data }: any) {
  const colors = ["#22c55e", "#eab308", "#ef4444", "#3b82f6"];

  return (
    <div>
      <div className="text-xs text-gray-400 mb-1">{title}</div>
      <ResponsiveContainer width="100%" height={180}>
        <PieChart>
          <Pie data={data} dataKey="value" innerRadius={40} outerRadius={60}>
            {data.map((_: any, i: number) => (
              <Cell key={i} fill={colors[i % colors.length]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

/* PANEL */
function Panel({ title, children, className = "" }: any) {
  return (
    <div className={`bg-[#11161c] border border-[#2a2f36] rounded p-3 ${className}`}>
      <div className="flex justify-between border-b border-[#2a2f36] pb-1 mb-2 text-xs text-gray-400">
        <span>{title}</span>
        <span>● ● ●</span>
      </div>
      {children}
    </div>
  );
}