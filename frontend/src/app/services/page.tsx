
import Link from 'next/link';
import { fetchServices } from '../lib/api';
import { ServiceSimple } from '../lib/types';

const getStatusColor = (status: string) => {
    switch (status) {
        case 'Operational': return 'bg-green-500';
        case 'Degraded': return 'bg-yellow-500';
        case 'Offline': return 'bg-red-500';
        default: return 'bg-gray-500';
    }
};

const getPostureColor = (posture: string) => {
    switch (posture) {
        case 'Healthy': return 'text-green-400';
        case 'At Risk': return 'text-yellow-400';
        case 'Degraded': return 'text-red-400';
        default: return 'text-gray-400';
    }
};

export default async function ServicesPage() {
    const services: ServiceSimple[] = await fetchServices();

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Service Registry</h1>
            <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                <table className="w-full text-left">
                    <thead>
                        <tr className="text-gray-400 border-b border-gray-700">
                            <th className="p-4">Name</th>
                            <th className="p-4">Criticality</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Continuity Posture</th>
                            <th className="p-4">RTO (Hours)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {services.map(service => (
                            <tr key={service.id} className="border-b border-gray-700 hover:bg-gray-700">
                                <td className="p-4">
                                    <Link href={`/services/${service.id}`} className="hover:underline">
                                        {service.name}
                                    </Link>
                                </td>
                                <td className="p-4">Tier {service.criticality_tier}</td>
                                <td className="p-4">
                                    <span className={`inline-block w-3 h-3 mr-2 rounded-full ${getStatusColor(service.current_status)}`}></span>
                                    {service.current_status}
                                </td>
                                <td className={`p-4 font-semibold ${getPostureColor(service.continuity_posture)}`}>
                                    {service.continuity_posture}
                                </td>
                                <td className="p-4">{service.rto_target_hours ?? 'N/A'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
