
import { fetchServicesFull } from '../lib/api';
import { Service } from '../lib/types';
import Link from 'next/link';

export default async function DependenciesPage() {
    const services: Service[] = await fetchServicesFull();

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Dependency Matrix</h1>
            
            <div className="space-y-8">
                {services.map(service => (
                    <div key={service.id} className="bg-gray-800 rounded-lg shadow-lg p-6">
                        <h2 className="text-2xl font-bold mb-4">
                            <Link href={`/services/${service.id}`} className="hover:underline">{service.name}</Link>
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h3 className="text-lg font-semibold mb-2 text-gray-400">Depends On (Downstream)</h3>
                                <ul className="space-y-2">
                                    {service.downstream_dependencies.map(dep => (
                                        <li key={dep.id} className="p-2 bg-gray-700 rounded">
                                            <Link href={`/services/${dep.depends_on_id}`} className="hover:underline">
                                                {dep.depends_on_name}
                                            </Link>
                                        </li>
                                    ))}
                                    {service.downstream_dependencies.length === 0 && <p className="text-gray-500">No downstream dependencies</p>}
                                </ul>
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold mb-2 text-gray-400">Dependency For (Upstream)</h3>
                                <ul className="space-y-2">
                                    {service.upstream_dependencies.map(dep => (
                                        <li key={dep.id} className="p-2 bg-gray-700 rounded">
                                            <Link href={`/services/${dep.service_id}`} className="hover:underline">
                                                {dep.service_name}
                                            </Link>
                                        </li>
                                    ))}
                                    {service.upstream_dependencies.length === 0 && <p className="text-gray-500">No upstream dependencies</p>}
                                </ul>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
