import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Our Team | CARE Pakistan" };

const coreTeam = [
  { name: "Dr. Junaid", role: "Founder & President" },
  { name: "Sana Khan", role: "General Secretary" },
  { name: "Ahmad Raza", role: "Operations Manager" },
];

const board = [
  { name: "Prof. Tariq Mehmood", role: "Chairman, Board of Governors" },
  { name: "Dr. Ayesha Siddiqui", role: "Board Member" },
  { name: "Mr. Kamran Ali", role: "Board Member" },
  { name: "Dr. Farrukh Nazar", role: "Board Member" },
];

const advisory = [
  { name: "Dr. Sara Malik", role: "Medical Advisor" },
  { name: "Mr. Bilal Chaudhry", role: "Legal Advisor" },
  { name: "Ms. Hina Javed", role: "Strategy Advisor" },
];

function TeamGrid({ members }: { members: { name: string; role: string }[] }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6">
      {members.map(({ name, role }) => (
        <div key={name} className="text-center group">
          <div className="w-28 h-28 rounded-full bg-green/10 mx-auto mb-3 flex items-center justify-center text-green/30 text-xs uppercase tracking-widest group-hover:bg-gold/10 transition-colors">
            Photo
          </div>
          <h4 className="font-semibold text-green">{name}</h4>
          <p className="text-gray-400 text-sm">{role}</p>
        </div>
      ))}
    </div>
  );
}

export default function TeamPage() {
  return (
    <>
      <div className="bg-green text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Our Team</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-gold">Home</Link> / Our Team
        </p>
      </div>

      <section id="core" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Core Team</h2>
          <div className="gold-divider" />
          <TeamGrid members={coreTeam} />
          <div className="text-center mt-10">
            <Link href="/team#board" className="btn-green inline-block">View All Team Members</Link>
          </div>
        </div>
      </section>

      <section id="board" className="py-20 bg-cream">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Board of Governors</h2>
          <div className="gold-divider" />
          <TeamGrid members={board} />
        </div>
      </section>

      <section id="advisory" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title">Advisory Board</h2>
          <p className="section-subtitle">Strategic (Advisory)</p>
          <div className="gold-divider" />
          <TeamGrid members={advisory} />
        </div>
      </section>
    </>
  );
}
