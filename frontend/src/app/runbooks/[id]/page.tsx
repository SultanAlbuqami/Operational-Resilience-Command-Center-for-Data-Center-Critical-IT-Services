
import { fetchRunbookTaskById } from '../../lib/api';
import { RunbookTask } from '../../lib/types';
import { notFound } from 'next/navigation';

export default async function RunbookDetailPage({ params }: { params: { id: string } }) {
    const task: RunbookTask = await fetchRunbookTaskById(params.id);

    if (!task) {
        notFound();
    }

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">Runbook Task Details</h1>
            <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                <p><span className="font-bold">Task:</span> {task.step_number}. {task.task_description}</p>
                <p><span className="font-bold">Service:</span> {task.service?.name || 'N/A'}</p>
                <p><span className="font-bold">Status:</span> {task.status}</p>
                <p><span className="font-bold">Owner:</span> {task.owner}</p>
                <p><span className="font-bold">ETA:</span> {task.eta_minutes} minutes</p>
            </div>
        </div>
    );
}
