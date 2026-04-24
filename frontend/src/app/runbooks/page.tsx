
import { fetchRunbookTasks } from '../lib/api';
import { RunbookTask } from '../lib/types';
import Link from 'next/link';

const getStatusColor = (status: string) => {
    switch (status) {
        case 'Not Started': return 'bg-gray-500';
        case 'In Progress': return 'bg-blue-500';
        case 'Blocked': return 'bg-red-500';
        case 'Completed': return 'bg-green-500';
        default: return 'bg-gray-500';
    }
};

export default async function RunbooksPage() {
    const tasks: RunbookTask[] = await fetchRunbookTasks();

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Runbook Execution Tracker</h1>
            <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                <table className="w-full text-left">
                    <thead>
                        <tr className="text-gray-400 border-b border-gray-700">
                            <th className="p-4">Task</th>
                            <th className="p-4">Service</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Owner</th>
                            <th className="p-4">ETA (Mins)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tasks.map(task => (
                            <tr key={task.id} className="border-b border-gray-700 hover:bg-gray-700">
                                <td className="p-4">
                                    <Link href={`/runbooks/${task.id}`} className="hover:underline">
                                        {task.step_number}. {task.task_description}
                                    </Link>
                                </td>
                                <td className="p-4">{task.service?.name || 'N/A'}</td>
                                <td className="p-4">
                                    <span className={`inline-block w-3 h-3 mr-2 rounded-full ${getStatusColor(task.status)}`}></span>
                                    {task.status}
                                </td>
                                <td className="p-4">{task.owner}</td>
                                <td className="p-4">{task.eta_minutes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
