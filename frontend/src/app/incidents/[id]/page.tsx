
import { fetchIncidentById, fetchRecoveryScores } from '../../lib/api';
import { Incident, RecoveryScore } from '../../lib/types';
import { notFound } from 'next/navigation';
import Link from 'next/link';

export default async function IncidentDetailPage({ params }: { params: { id: string } }) {
    const incident: Incident = await fetchIncidentById(params.id);
    const recoveryScores: RecoveryScore[] = await fetchRecoveryScores(params.id);

    if (!incident) {
        notFound();
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-2">
                 <h1 className="text-4xl font-bold">Incident: {incident.name}</h1>
                 <Link href={`/reports/executive-brief/${incident.id}`} legacyBehavior>
                    <a className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" target="_blank">Generate Executive Brief</a>
                </Link>
            </div>
            <p className="text-lg text-gray-400 mb-8">Declared at: {new Date(incident.start_time).toLocaleString()}</p>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div>
                    <h2 className="text-2xl font-bold mb-4">Recovery Prioritization</h2>
                    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                         <table className="w-full text-left">
                            <thead>
                                <tr className="text-gray-400 border-b border-gray-700">
                                    <th className="p-4">Rank</th>
                                    <th className="p-4">Service</th>
                                    <th className="p-4">Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recoveryScores.map((score, index) => (
                                    <tr key={score.service_id} className="border-b border-gray-700 hover:bg-gray-700">
                                        <td className="p-4 font-bold text-xl">{index + 1}</td>
                                        <td className="p-4">
                                            <Link href={`/services/${score.service_id}`} className="hover:underline">
                                                {score.name}
                                            </Link>
                                        </td>
                                        <td className="p-4 font-mono">{score.total_score}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div>
                    <h2 className="text-2xl font-bold mb-4">Affected Services ({incident.affected_services.length})</h2>
                    <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                        <ul className="space-y-2">
                            {incident.affected_services.map(service => (
                                <li key={service.id} className="flex justify-between items-center p-2 bg-gray-700 rounded">
                                    <Link href={`/services/${service.id}`} className="hover:underline">
                                        {service.name}
                                    </Link>
                                    <span className="font-semibold text-red-400">{service.current_status}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
