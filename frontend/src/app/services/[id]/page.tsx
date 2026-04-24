
import { fetchServiceById } from '../../lib/api';
import { Service } from '../../lib/types';
import { notFound } from 'next/navigation';
import Link from 'next/link';

const InfoCard = ({ title, children }) => (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4 text-gray-300">{title}</h3>
        {children}
    </div>
);

export default async function ServiceDetailPage({ params }: { params: { id: string } }) {
    const service: Service = await fetchServiceById(params.id);

    if (!service) {
        notFound();
    }

    return (
        <div>
            <h1 className="text-4xl font-bold mb-2">{service.name}</h1>
            <p className="text-lg text-gray-400 mb-8">Owner: {service.owner} | Business Unit: {service.business_unit}</p>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column */}
                <div className="lg:col-span-2 space-y-8">
                    <InfoCard title="Business Impact Analysis">
                        <div className="grid grid-cols-2 gap-4">
                            <div><p className="font-semibold">RTO:</p> <p>{service.bia.rto_target_hours} hours</p></div>
                            <div><p className="font-semibold">RPO:</p> <p>{service.bia.rpo_target_minutes} minutes</p></div>
                            <div><p className="font-semibold">Financial Impact:</p> <p>{service.bia.financial_impact}</p></div>
                            <div><p className="font-semibold">Regulatory Impact:</p> <p>{service.bia.regulatory_impact}</p></div>
                        </div>
                    </InfoCard>

                    <InfoCard title="Runbook">
                        <ul className="space-y-2">
                            {service.runbook_tasks.map(task => (
                                <li key={task.id} className="flex justify-between items-center p-2 bg-gray-700 rounded">
                                    <span>{task.step_number}. {task.task_description}</span>
                                    <span className="font-mono text-sm bg-gray-600 px-2 py-1 rounded">{task.status}</span>
                                </li>
                            ))}
                        </ul>
                    </InfoCard>
                </div>

                {/* Right Column */}
                <div className="space-y-8">
                     <InfoCard title="Dependencies">
                        <h4 className="font-bold text-gray-400 mb-2">Depends On (Downstream)</h4>
                        <ul className="space-y-2 mb-4">
                            {service.downstream_dependencies.map(dep => (
                                <li key={dep.id} className="p-2 bg-gray-700 rounded">
                                   <Link href={`/services/${dep.depends_on_id}`} className="hover:underline">
                                        {dep.depends_on_name}
                                    </Link>
                                </li>
                            ))}
                        </ul>

                        <h4 className="font-bold text-gray-400 mb-2">Dependency For (Upstream)</h4>
                        <ul className="space-y-2">
                             {service.upstream_dependencies.map(dep => (
                                <li key={dep.id} className="p-2 bg-gray-700 rounded">
                                    <Link href={`/services/${dep.service_id}`} className="hover:underline">
                                        {dep.service_name} 
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </InfoCard>
                </div>
            </div>
        </div>
    );
}
