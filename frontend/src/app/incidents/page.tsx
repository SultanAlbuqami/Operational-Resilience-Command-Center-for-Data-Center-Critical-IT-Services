
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

const scenarios = [
    { name: 'Primary Data Center Power Failure', description: 'A complete loss of power at the primary data center.' },
    { name: 'Ransomware on Virtualization Cluster', description: 'A ransomware attack has encrypted the main virtualization cluster.' },
    { name: 'Core DNS Service Unavailability', description: 'The core DNS service is not resolving requests.' },
];

export default function IncidentsPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleTriggerIncident = async (scenarioName: string, description: string) => {
        setIsLoading(true);
        setError(null);

        try {
            const res = await fetch('/api/v1/incidents/trigger', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: scenarioName, description }),
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || 'Failed to trigger incident');
            }

            const incident = await res.json();
            router.push(`/incidents/${incident.id}`);

        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Incident Simulator</h1>
            {error && <div className="bg-red-900 text-white p-4 rounded-lg mb-6">{error}</div>}
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {scenarios.map(scenario => (
                    <div key={scenario.name} className="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col">
                        <h2 className="text-xl font-bold mb-2">{scenario.name}</h2>
                        <p className="text-gray-400 mb-4 flex-grow">{scenario.description}</p>
                        <button 
                            onClick={() => handleTriggerIncident(scenario.name, scenario.description)}
                            disabled={isLoading}
                            className="mt-auto bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded disabled:bg-gray-600"
                        >
                            {isLoading ? 'Simulating...' : 'Trigger Scenario'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
