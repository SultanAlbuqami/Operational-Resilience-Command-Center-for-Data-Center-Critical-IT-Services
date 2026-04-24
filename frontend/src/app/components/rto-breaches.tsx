
'use client'

import { useState, useEffect } from 'react';
import { ServiceSimple } from '../lib/types';

const RTOBreaches = ({ services }: { services: ServiceSimple[] }) => {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    const offlineServices = services.filter(s => s.current_status !== 'Operational' && s.rto_target_hours);

    const getRtoBreachTime = (service: ServiceSimple) => {
        // This is a placeholder for a real implementation that would use the incident start time.
        // For now, we'll use a dummy start time.
        const incidentStartTime = new Date(time.getTime() - 15 * 60 * 1000); // 15 minutes ago
        const rtoMilliseconds = service.rto_target_hours! * 60 * 60 * 1000;
        const breachTime = new Date(incidentStartTime.getTime() + rtoMilliseconds);
        const timeLeft = breachTime.getTime() - time.getTime();

        if (timeLeft < 0) {
            return { timeLeft: 0, breachTime };
        }
        return { timeLeft, breachTime };
    };

    const formatTimeLeft = (milliseconds: number) => {
        const totalSeconds = Math.floor(milliseconds / 1000);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        return `${hours}h ${minutes}m ${seconds}s`;
    }

    if (offlineServices.length === 0) {
        return <p className="text-gray-500">No services currently offline.</p>;
    }

    return (
        <ul className="space-y-4">
            {offlineServices.map(service => {
                const { timeLeft } = getRtoBreachTime(service);
                return (
                    <li key={service.id} className="p-3 bg-gray-700 rounded-lg">
                        <p className="font-semibold">{service.name}</p>
                        <p className={`font-mono text-lg ${timeLeft < 30 * 60 * 1000 ? 'text-red-400' : 'text-yellow-400'}`}>
                            {formatTimeLeft(timeLeft)}
                        </p>
                    </li>
                )
            })}
        </ul>
    );
}

export default RTOBreaches;
