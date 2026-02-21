import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertTriangle, Flame, Activity, Wind, Snowflake, Mountain,
  MapPin, Clock, ShieldCheck, ChevronRight, Settings,
  Map, ShieldAlert, Users, Filter
} from 'lucide-react';
import { cn } from './lib/utils';

// --- MOCK DATA ---
const ALERTS = [
  {
    id: 'AL-1092',
    type: 'Flash Flood',
    severity: 'Critical',
    risk: 94,
    location: 'Sector C (Marina Bay)',
    time: '2 mins ago',
    icon: Wind,
    color: 'text-red-500',
    bg: 'bg-red-500/10',
    desc: 'Rapid water level rise detected across central district. Immediate evacuation protocols recommended for low-lying areas. Sensor anomaly matched with ground reports.'
  },
  {
    id: 'AL-1093',
    type: 'Wildfire Risk',
    severity: 'High',
    risk: 78,
    location: 'Sector A (North Hills)',
    time: '14 mins ago',
    icon: Flame,
    color: 'text-orange-500',
    bg: 'bg-orange-500/10',
    desc: 'Dry conditions and high winds have elevated wildfire probability. Thermal imaging satellites show localized hotspots near residential zones.'
  },
  {
    id: 'AL-1094',
    type: 'Seismic Anomaly',
    severity: 'Medium',
    risk: 45,
    location: 'Sector D (Plate Boundary)',
    time: '1 hr ago',
    icon: Activity,
    color: 'text-yellow-500',
    bg: 'bg-yellow-500/10',
    desc: 'Minor tremors detected. Magnitude 3.2 preliminary reading. Structural monitoring systems show nominal stress levels.'
  },
  {
    id: 'AL-1095',
    type: 'Volcanic Ash',
    severity: 'Low',
    risk: 12,
    location: 'Sector B (Highlands)',
    time: '3 hrs ago',
    icon: Mountain,
    color: 'text-slate-500',
    bg: 'bg-slate-500/10',
    desc: 'Light ash fall predicted based on current wind patterns from Mt. Aegis. Low impact to aviation expected at this time.'
  },
];

const SEVERITIES = ['All', 'Low', 'Medium', 'High', 'Critical'];

// --- COMPONENTS ---

const Sidebar = () => (
  <aside className="w-64 border-r border-slate-200 bg-white/50 backdrop-blur-xl h-screen fixed left-0 top-0 flex flex-col hidden md:flex">
    <div className="p-6 flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
        <ShieldAlert className="w-5 h-5 text-white" />
      </div>
      <span className="font-bold text-xl tracking-tight">Aegis AI</span>
    </div>

    <nav className="flex-1 px-4 py-6 space-y-1">
      {[
        { icon: AlertTriangle, label: 'Active Alerts', active: true },
        { icon: Activity, label: 'Predictions' },
        { icon: Map, label: 'Global Map' },
        { icon: Users, label: 'Verified Agencies' },
      ].map((item) => (
        <a
          key={item.label}
          href="#"
          className={cn(
            "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all group",
            item.active
              ? "bg-primary text-white shadow-md shadow-slate-200"
              : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
          )}
        >
          <item.icon className="w-4 h-4" />
          {item.label}
        </a>
      ))}
    </nav>

    <div className="p-4 border-t border-slate-100">
      <a href="#" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-600 hover:bg-slate-100 transition-all">
        <Settings className="w-4 h-4" />
        Settings
      </a>
    </div>
  </aside>
);

const AlertModal = ({ alert, onClose }: { alert: any, onClose: () => void }) => {
  if (!alert) return null;
  const Icon = alert.icon;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.95, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 20 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden border border-slate-100"
        >
          {/* Header */}
          <div className="p-6 border-b border-slate-100 flex items-start gap-4">
            <div className={cn("w-14 h-14 rounded-2xl flex items-center justify-center shrink-0", alert.bg)}>
              <Icon className={cn("w-7 h-7", alert.color)} />
            </div>
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">{alert.id}</span>
                <span className={cn("text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border", alert.color, alert.bg, "border-" + alert.color.split('-')[1] + "-200")}>
                  {alert.severity}
                </span>
              </div>
              <h2 className="text-2xl font-bold tracking-tight text-slate-900">{alert.type}</h2>
            </div>
          </div>

          {/* Body */}
          <div className="p-6 space-y-6 bg-slate-50/50">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs font-medium text-slate-500 mb-1">Location Radius</p>
                <p className="text-sm font-semibold flex items-center gap-1.5"><MapPin className="w-4 h-4 text-slate-400" /> {alert.location}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-slate-500 mb-1">Detection Time</p>
                <p className="text-sm font-semibold flex items-center gap-1.5"><Clock className="w-4 h-4 text-slate-400" /> {alert.time}</p>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-end mb-2">
                <span className="text-sm font-semibold text-slate-700">AI Risk Probability</span>
                <span className={cn("text-xl font-bold", alert.color)}>{alert.risk}%</span>
              </div>
              <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }} animate={{ width: `${alert.risk}%` }} transition={{ duration: 1, ease: 'easeOut' }}
                  className={cn("h-full rounded-full", alert.bg.replace('/10', ''))}
                />
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
              <p className="text-sm text-slate-600 leading-relaxed shadow-sm">{alert.desc}</p>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 bg-white border-t border-slate-100 flex flex-col sm:flex-row gap-3">
            <button className="flex-1 bg-primary text-white font-semibold py-3 rounded-xl shadow-md shadow-primary/20 hover:bg-slate-800 transition-colors">
              Deploy Response
            </button>
            <button onClick={onClose} className="flex-1 bg-white text-slate-700 font-semibold py-3 rounded-xl border border-slate-200 hover:bg-slate-50 transition-colors">
              Dismiss
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}

function App() {
  const [activeFilter, setActiveFilter] = useState('All');
  const [selectedAlert, setSelectedAlert] = useState<any>(null);

  const filteredAlerts = ALERTS.filter(a => activeFilter === 'All' || a.severity === activeFilter);

  return (
    <div className="min-h-screen flex bg-background text-slate-900 font-sans selection:bg-blue-100">
      <Sidebar />

      <main className="flex-1 md:pl-64">
        <div className="max-w-6xl mx-auto p-6 lg:p-10 space-y-10">

          {/* Header Section */}
          <header className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold tracking-tight mb-2">Defense Intelligence</h1>
              <p className="text-slate-500 text-lg">Real-time monitoring of global disaster incidents</p>
            </div>

            {/* Filter Tabs */}
            <div className="flex items-center gap-4 border-b border-slate-200 pb-px">
              <div className="flex gap-6 relative">
                {SEVERITIES.map((sev) => (
                  <button
                    key={sev}
                    onClick={() => setActiveFilter(sev)}
                    className={cn(
                      "pb-4 text-sm font-semibold transition-colors relative",
                      activeFilter === sev ? "text-primary" : "text-slate-500 hover:text-slate-800"
                    )}
                  >
                    {sev}
                    {activeFilter === sev && (
                      <motion.div layoutId="underline" className="absolute left-0 right-0 bottom-0 h-0.5 bg-primary" />
                    )}
                  </button>
                ))}
              </div>

              <div className="ml-auto mb-4">
                <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-600 hover:bg-slate-50 shadow-sm transition-all">
                  <Filter className="w-4 h-4" /> Filter
                </button>
              </div>
            </div>
          </header>

          {/* Alert Grid */}
          <motion.div layout className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence mode='popLayout'>
              {filteredAlerts.map((alert) => {
                const Icon = alert.icon;
                return (
                  <motion.div
                    key={alert.id}
                    layout // Animate sorting/filtering
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.2 }}
                    className="glass rounded-3xl p-6 group cursor-pointer hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] transition-all flex flex-col"
                    onClick={() => setSelectedAlert(alert)}
                  >
                    <div className="flex justify-between items-start mb-6">
                      <div className={cn("w-12 h-12 rounded-2xl flex items-center justify-center transition-transform group-hover:scale-110", alert.bg)}>
                        <Icon className={cn("w-6 h-6", alert.color)} />
                      </div>
                      <span className={cn("text-[10px] uppercase font-bold px-2.5 py-1 rounded-full border backdrop-blur-md", alert.color, alert.bg, "border-" + alert.color.split('-')[1] + "-200")}>
                        {alert.severity}
                      </span>
                    </div>

                    <div className="flex-1 mb-6">
                      <h3 className="text-xl font-bold tracking-tight mb-2 group-hover:text-primary transition-colors">{alert.type}</h3>
                      <div className="flex items-center gap-4 text-xs font-medium text-slate-500">
                        <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" />{alert.location}</span>
                        <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{alert.time}</span>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-xs font-bold mb-1.5">
                          <span className="text-slate-600">Risk Matrix</span>
                          <span className={alert.color}>{alert.risk}%</span>
                        </div>
                        <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }} animate={{ width: `${alert.risk}%` }}
                            className={cn("h-full rounded-full transition-all", alert.bg.replace('/10', ''))}
                          />
                        </div>
                      </div>

                      <div className="pt-2 flex gap-2">
                        <button className="flex-1 bg-slate-900 text-white text-xs font-bold py-2.5 rounded-lg shadow-sm hover:bg-slate-800 transition-colors flex justify-center items-center gap-2">
                          View Intel <ChevronRight className="w-3 h-3" />
                        </button>
                        <button
                          onClick={(e) => { e.stopPropagation(); alert('Safe') }}
                          className="flex flex-1 justify-center items-center gap-1.5 border border-slate-200 text-slate-700 bg-white hover:bg-slate-50 text-xs font-bold py-2.5 rounded-lg transition-colors"
                        >
                          <ShieldCheck className="w-4 h-4 text-emerald-500" /> Mark Safe
                        </button>
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </AnimatePresence>
          </motion.div>

        </div>
      </main>

      <AlertModal alert={selectedAlert} onClose={() => setSelectedAlert(null)} />
    </div>
  )
}

export default App;
