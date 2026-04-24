
import { fetchDRExercises } from '../lib/api';
import { DRExercise } from '../lib/types';
import Link from 'next/link';
import { CheckCircle, AlertTriangle } from 'lucide-react';

export default async function DRExercisesPage() {
    const exercises: DRExercise[] = await fetchDRExercises();

    return (
        <div>
            <h1 className="text-3xl font-bold mb-6">DR Exercise Scorecards</h1>
            <div className="bg-gray-800 rounded-lg shadow-lg p-6">
                <table className="w-full text-left">
                    <thead>
                        <tr className="text-gray-400 border-b border-gray-700">
                            <th className="p-4">Exercise</th>
                            <th className="p-4">Date</th>
                            <th className="p-4">Result</th>
                            <th className="p-4">Target RTO (Mins)</th>
                            <th className="p-4">Actual RTO (Mins)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {exercises.map(ex => (
                            <tr key={ex.id} className="border-b border-gray-700 hover:bg-gray-700">
                                <td className="p-4">
                                    <Link href={`/dr-exercises/${ex.id}`} className="hover:underline">
                                        {ex.name}
                                    </Link>
                                </td>
                                <td className="p-4">{new Date(ex.test_date).toLocaleDateString()}</td>
                                <td className="p-4">
                                    {ex.passed ? (
                                        <span className="flex items-center text-green-400"><CheckCircle className="mr-2" /> Pass</span>
                                    ) : (
                                        <span className="flex items-center text-red-400"><AlertTriangle className="mr-2" /> Fail</span>
                                    )}
                                </td>
                                <td className="p-4">{ex.target_rto_minutes}</td>
                                <td className="p-4">{ex.actual_rto_minutes ?? 'N/A'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
