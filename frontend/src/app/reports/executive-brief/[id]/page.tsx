
import { fetchIncidentById, fetchRecoveryScores } from '../../../lib/api';
import { Incident, RecoveryScore } from '../../../lib/types';
import { notFound } from 'next/navigation';

export default async function ExecutiveBriefPage({ params }: { params: { id: string } }) {
    const incident: Incident = await fetchIncidentById(params.id);
    const recoveryScores: RecoveryScore[] = await fetchRecoveryScores(params.id);

    if (!incident) {
        notFound();
    }

    const topBusinessImpacts = incident.affected_services
        .filter(s => s.criticality_tier === 1)
        .slice(0, 5);

    return (
        <div className="bg-white text-black p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold border-b-2 border-black pb-2 mb-4">Executive Incident Brief</h1>
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-semibold">{incident.name}</h2>
                <p className="text-lg">Declared: {new Date(incident.start_time).toLocaleString()}</p>
            </div>

            <div className="mb-6">
                <h3 className="text-xl font-bold mb-2">Incident Summary</h3>
                <p>{incident.description}</p>
            </div>

            <div className="mb-6">
                <h3 className="text-xl font-bold mb-2">Top Business Impacts</h3>
                <ul className="list-disc list-inside">
                    {topBusinessImpacts.map(s => <li key={s.id}>{s.name}</li>)}
                </ul>
            </div>

             <div className="mb-6">
                <h3 className="text-xl font-bold mb-2">Recovery Recommendation</h3>
                <ol className="list-decimal list-inside">
                    {recoveryScores.map(s => <li key={s.service_id}>{s.name}</li>)}
                </ol>
            </div>

            <div className="grid grid-cols-2 gap-6">
                 <div>
                    <h3 className="text-xl font-bold mb-2">Restoration Timeline Estimate</h3>
                    <p>4-6 hours</p>
                </div>
                <div>
                    <h3 className="text-xl font-bold mb-2">Top Risks</h3>
                    <p>Data corruption, extended downtime</p>
                </div>
            </div>
            
        </div>
    );
}
