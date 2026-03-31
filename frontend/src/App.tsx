import { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { motion } from "framer-motion";

interface Log {
  timestamp: string;
  prediction: string;
}

function App() {
  const [logs, setLogs] = useState<Log[]>([]);

  const fetchLogs = async () => {
    const res = await axios.get("http://localhost:8000/api/logs");
    setLogs(res.data);
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 2000);
    return () => clearInterval(interval);
  }, []);

  // Metrics
  const total = logs.length;
  const attacks = logs.filter(l => l.prediction === "ATTACK").length;
  const benign = logs.filter(l => l.prediction === "BENIGN").length;

  // Chart aggregation (important fix)
  const grouped: any = {};
  logs.forEach(log => {
    const t = new Date(log.timestamp).toLocaleTimeString();
    if (!grouped[t]) grouped[t] = 0;
    if (log.prediction === "ATTACK") grouped[t]++;
  });

  const chartData = Object.keys(grouped).map(t => ({
    time: t,
    attacks: grouped[t]
  }));

  const recentAttacks = logs.slice(-10).filter(l => l.prediction === "ATTACK").length;
  const isAlert = recentAttacks > 3;

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono p-4 relative overflow-hidden">

      {/* Background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,0,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,0,0.05)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

      {/* Header */}
      <div className="flex justify-between items-center mb-4 relative z-10">
        <h1 className="text-2xl text-cyan-400">SentinelNet - AI IDS</h1>
        <div className="text-green-500 animate-pulse">● LIVE</div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
        <Card title="Total Traffic" value={total} />
        <Card title="Attacks" value={attacks} red />
        <Card title="Benign" value={benign} />
      </div>

      {/* Middle */}
      <div className="grid grid-cols-3 gap-4 relative z-10">

        {/* Chart */}
        <div className="col-span-2 bg-black/40 backdrop-blur p-4 rounded-xl border border-cyan-500">
          <h2 className="text-cyan-300 mb-2">Attack Timeline</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <XAxis dataKey="time" stroke="#00ffff" />
              <YAxis stroke="#00ffff" />
              <Tooltip />
              <Line type="monotone" dataKey="attacks" stroke="#ff0033" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Alerts */}
        <div className="bg-black/40 backdrop-blur p-4 rounded-xl border border-red-500">
          <h2 className="text-red-400">Alerts</h2>

          {isAlert ? (
            <motion.div
              className="mt-4 text-red-500 text-xl"
              animate={{ opacity: [0.2, 1, 0.2] }}
              transition={{ repeat: Infinity, duration: 1 }}
            >
              ⚠ INTRUSION DETECTED
            </motion.div>
          ) : (
            <div className="text-green-400 mt-4">No threats</div>
          )}
        </div>
      </div>

      {/* Logs */}
      <div className="mt-4 bg-black/60 backdrop-blur p-4 rounded-xl border border-green-500 h-64 overflow-y-auto relative z-10">
        <h2 className="text-green-300 mb-2">Event Feed</h2>

        {logs.slice().reverse().map((log, i) => (
          <div
            key={i}
            className={
              log.prediction === "ATTACK"
                ? "text-red-400"
                : "text-green-400"
            }
          >
            [{new Date(log.timestamp).toLocaleTimeString()}] {log.prediction}
          </div>
        ))}
      </div>

    </div>
  );
}

function Card({ title, value, red }: any) {
  return (
    <div className={`p-4 rounded-xl border ${red ? "border-red-500" : "border-green-500"} bg-black/40 backdrop-blur`}>
      <h3 className="text-sm text-gray-400">{title}</h3>
      <p className={`text-2xl ${red ? "text-red-400" : "text-green-400"}`}>
        {value}
      </p>
    </div>
  );
}

export default App;