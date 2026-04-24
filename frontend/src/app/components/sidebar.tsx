
'use client'

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { BarChart, Building, HeartPulse, LayoutDashboard, LucideIcon, Settings, ShieldAlert, Siren } from 'lucide-react';

const navItems = [
    { href: '/', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/services', label: 'Services', icon: Building },
    { href: '/incidents', label: 'Incidents', icon: Siren },
    { href: '/dependencies', label: 'Dependencies', icon: HeartPulse },
    { href: '/runbooks', label: 'Runbooks', icon: Settings },
    { href: '/dr-exercises', label: 'DR Exercises', icon: ShieldAlert },
];

const NavLink = ({ href, label, icon: Icon }: { href: string, label: string, icon: LucideIcon }) => {
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <Link href={href}>
            <span className={`flex items-center p-2 rounded-lg text-gray-300 hover:bg-gray-700 ${isActive ? 'bg-gray-700' : ''}`}>
                <Icon className="w-6 h-6" />
                <span className="ml-3">{label}</span>
            </span>
        </Link>
    );
};

export function Sidebar() {
    return (
        <aside className="w-64" aria-label="Sidebar">
            <div className="overflow-y-auto py-4 px-3 bg-gray-800 rounded-lg">
                <div className="flex items-center pl-2.5 mb-5">
                    <BarChart className="h-8 w-8 text-white" />
                    <span className="self-center text-xl font-semibold whitespace-nowrap text-white ml-2">
                        Resilience Center
                    </span>
                </div>
                <ul className="space-y-2">
                    {navItems.map((item) => (
                        <li key={item.label}>
                           <NavLink {...item} />
                        </li>
                    ))}
                </ul>
            </div>
        </aside>
    );
}
