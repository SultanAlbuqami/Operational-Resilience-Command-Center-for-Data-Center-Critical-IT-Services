import { fetchIncidentById, fetchRecoveryScores, fetchExecutiveBrief } from '../../../lib/api';
import { Incident, RecoveryScore, ExecutiveBrief } from '../../../lib/types';
import { notFound } from 'next/navigation';

export default async function ExecutiveBriefPage({ params }: { params: { id: string } }) {
    const incident: Incident = await fetchIncidentById(params.id);
    const brief: ExecutiveBrief = await fetchExecutiveBrief(params.id);
    const recoveryScores: RecoveryScore[] = await fetchRecoveryScores(params.id);

    if (!incident || !brief) {
        notFound();
    }

    return (
        <div className="bg-white text-black p-8 max-w-4xl mx-auto shadow-2xl rounded">
            <h1 className="text-3xl font-bold border-b-4 border-gray-800 pb-2 mb-6">Executive Incident Brief</h1>  
            <div className="flex justify-between items-center mb-6 text-gray-700 font-medium">
                <h2 className="text-2xl font-bold text-black">{incident.name}</h2>
                <p className="text-md">Declared: {new Date(incident.start_time).toLocaleString()}</p>
            </div>

            <div className="mb-8">
                <h3 className="text-xl font-bold mb-3 border-b border-gray-300 pb-1">Incident Summary</h3>
                <p className="text-lg leading-relaxed">{brief.incident_summary}</p>
                <p className="text-md mt-2 text-gray-600">{incident.description}</p>
            </div>

            <div className="mb-8">
                <h3 className="text-xl font-bold mb-3 border-b border-gray-300 pb-1">Top Business Impacts</h3>
                <ul className="list-disc list-inside space-y-2">
                    {brief.top_business_impacts.map((impact, i) => (
                        <li key={i} className="text-lg">{impact}</li>
                    ))}
                </ul>
            </div>

            <div className="mb-8">
                <h3 className="text-xl font-bold mb-3 border-b border-gray-300 pb-1">Affected Services</h3>
                <div className="flex flex-wrap gap-2">
                    {brief.affected_services.map((svc, i) => (
                        <span key={i} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-semibold">{svc}</span>
                    ))}
                </div>
            </div>

            <div className="mb-8">
                <h3 className="text-xl font-bold mb-3 border-b border-gray-300 pb-1">Recovery Prioritization Order</h3>
                <p className="text-md font-semibold text-gray-700 mb-2">{brief.recovery_recommendation}</p>
                <ol className="list-decimal list-inside space-y-1 bg-gray-50 p-4 rounded border border-gray-200">
                    {recoveryScores.map(s => (
                        <li key={s.service_id} className="text-lg font-medium">
                            {s.name} <span className="text-sm font-normal text-gray-500">(Score: {s.total_score})</span>
                        </li>
                    ))}
                </ol>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-6">
                <div className="bg-blue-50 p-4 rounded border border-blue-100">
                    <h3 className="text-xl font-bold mb-3 text-blue-900">Restoration Timeline Estimate</h3>
                    <p className="text-lg font-semibold text-blue-800">{brief.estimated_restoration_timeline}</p>
                </div>
                
                <div className="bg-yellow-50 p-4 rounded border border-yellow-100">
                    <h3 className="text-xl font-bold mb-3 text-yellow-900">Escalation Recommendation</h3>
                    <p className="text-lg font-semibold text-yellow-800">{brief.escalation_recommendation}</p>
                </div>
            </div>

            <div className="mb-4">
                <h3 className="text-xl font-bold mb-3 border-b border-gray-300 pb-1">Top Risks</h3>
                <ul className="list-disc list-inside space-y-2">
                    {brief.top_risks.map((risk, i) => (
                        <li key={i} className="text-lg text-red-700">{risk}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}