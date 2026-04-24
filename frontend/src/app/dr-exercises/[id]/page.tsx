
import { fetchDRExerciseById } from '../../lib/api';
import { DRExercise } from '../../lib/types';
import { notFound } from 'next/navigation';
import Link from 'next/link';

const InfoCard = ({ title, children }: { title: string, children: React.ReactNode }) => (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4 text-gray-300">{title}</h3>
        {children}
    </div>
);

export default async function DRExerciseDetailPage({ params }: { params: { id: string } }) {
    const exercise: DRExercise = await fetchDRExerciseById(params.id);

    if (!exercise) {
        notFound();
    }

    return (
        <div>
            <h1 className="text-4xl font-bold mb-2">{exercise.name}</h1>
            <p className="text-lg text-gray-400 mb-8">Tested on: {new Date(exercise.test_date).toLocaleDateString()}</p>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <InfoCard title="Scorecard">
                    <div className="grid grid-cols-2 gap-4">
                        <div><p className="font-semibold">Target RTO:</p> {exercise.target_rto_minutes} mins</div>
                        <div><p className="font-semibold">Actual RTO:</p> {exercise.actual_rto_minutes ?? 'N/A'} mins</div>
                        <div><p className="font-semibold">Target RPO:</p> {exercise.target_rpo_minutes} mins</div>
                        <div><p className="font-semibold">Actual RPO:</p> {exercise.actual_rpo_minutes ?? 'N/A'} mins</div>
                        <div><p className="font-semibold">Result:</p> <span className={exercise.passed ? 'text-green-400' : 'text-red-400'}>{exercise.passed ? 'Pass' : 'Fail'}</span></div>
                    </div>
                </InfoCard>

                <InfoCard title="Affected Services">
                     <ul className="space-y-2">
                        {exercise.services.map(service => (
                            <li key={service.id} className="p-2 bg-gray-700 rounded">
                                <Link href={`/services/${service.id}`} className="hover:underline">{service.name}</Link>
                            </li>
                        ))}
                    </ul>
                </InfoCard>

                <div className="lg:col-span-2">
                    <InfoCard title="Details">
                        <p><span className="font-bold">Scenario:</span> {exercise.scenario}</p>
                        <p><span className="font-bold">Issues Observed:</span> {exercise.issues_observed ?? 'None'}</p>
                        <p><span className="font-bold">Lessons Learned:</span> {exercise.lessons_learned ?? 'None'}</p>
                        <p><span className="font-bold">Corrective Actions:</span> {exercise.corrective_actions ?? 'None'}</p>
                    </InfoCard>
                </div>
            </div>
        </div>
    );
}
