import dynamic from "next/dynamic";

const CarbonMap = dynamic(() => import("@/components/CarbonMap"), {
  ssr: false
});

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl space-y-8 p-6">
      <header className="space-y-2">
        <p className="text-sm uppercase tracking-wide text-emerald-700">CarbonEye Agent</p>
        <h1 className="text-3xl font-bold text-slate-900">Monitor carbon and biomass from satellite imagery</h1>
        <p className="max-w-3xl text-sm text-slate-600">
          Draw or upload a project boundary to trigger the AI-driven workflow. The map captures your area,
          the backend orchestrates Google Earth Engine, biomass modelling, and carbon credit estimation, and the
          dashboard returns transparent metrics and metadata.
        </p>
      </header>
      <CarbonMap />
    </main>
  );
}
