
import { fetchServices, fetchDRExercises } from './lib/api';
import { ServiceSimple, DRExercise } from './lib/types';
import { Server, ShieldCheck, ShieldOff, AlertTriangle, CheckCircle } from 'lucide-react';
import RTOBreaches from './components/rto-breaches';

// Stat Card Component
const StatCard = ({ title, value, icon: Icon, color = 'text-white' }) => (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <div className="flex items-center">
            <div className={`p-3 rounded-full bg-gray-700 ${color}`}>
                <Icon className="h-6 w-6" />
            </div>
            <div className="ml-4">
                <p className="text-sm font-medium text-gray-400">{title}</p>
                <p className="text-2xl font-bold">{value}</p>
            </div>
        </div>
    </div>
);

export default async function DashboardPage() {
    const services: ServiceSimple[] = await fetchServices();
    const drExercises: DRExercise[] = await fetchDRExercises();

    const criticalServices = services.filter(s => s.criticality_tier === 1).length;
    const servicesAtRisk = services.filter(s => s.continuity_posture !== 'Healthy').length;
    const offlineServices = services.filter(s => s.current_status !== 'Operational').length;
    const latestExercises = drExercises.slice(0, 5);

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Executive Dashboard</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard title="Total Critical Services" value={criticalServices} icon={Server} color="text-blue-400" />
                <StatCard title="Services Offline" value={offlineServices} icon={AlertTriangle} color="text-red-400" />
                <StatCard title="Services At Risk" value={servicesAtRisk} icon={ShieldOff} color="text-yellow-400" />
                <StatCard title="DR Exercises Passed" value={`${drExercises.filter(e => e.passed).length} / ${drExercises.length}`} icon={ShieldCheck} color="text-green-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                    <h2 className="text-xl font-bold mb-4">Latest DR Exercises</h2>
                    <ul className="space-y-4">
                        {latestExercises.map(exercise => (
                            <li key={exercise.id} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                                <div>
                                    <p className="font-semibold">{exercise.name}</p>
                                    <p className="text-sm text-gray-400">{new Date(exercise.test_date).toLocaleDateString()}</p>
                                </div>
                                {exercise.passed ? (
                                    <span className="flex items-center text-green-400"><CheckCircle className="mr-2" /> Pass</span>
                                ) : (
                                    <span className="flex items-center text-red-400"><AlertTriangle className="mr-2" /> Fail</span>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
                
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                    <h2 className="text-xl font-bold mb-4">Services with Upcoming RTO Breaches</h2>
                    <RTOBreaches services={services} />
                </div>
            </div>
        </div>
    );
}
