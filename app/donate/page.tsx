import type { Metadata } from "next";
import Link from "next/link";
import { FaUniversity, FaHandHoldingUsd, FaDownload } from "react-icons/fa";
import DonateAmounts from "@/components/DonateAmounts";

export const metadata: Metadata = { title: "Donate | CARE Pakistan" };

const bankDetails = [
  { label: "Account Title", value: "CARE" },
  { label: "Account No", value: "PK46MEZN0001230104370178" },
  { label: "Bank Name", value: "Meezan Bank" },
  { label: "Branch Name", value: "Johar Town" },
  { label: "Branch Code", value: "1234 576 9702" },
  { label: "IBAN", value: "PK46MEZN0001234567890178" },
];

export default function DonatePage() {
  return (
    <>
      <div className="bg-dark text-white py-16 px-4 text-center">
        <h1 className="text-4xl font-serif mb-2">Donate</h1>
        <p className="text-white/60 text-sm">
          <Link href="/" className="hover:text-primary">Home</Link> / Donate
        </p>
      </div>

      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16">

          {/* Bank Details */}
          <div>
            <div className="flex items-center gap-3 mb-6">
              <FaUniversity className="text-primary text-2xl" />
              <h2 className="text-2xl font-serif text-dark">Bank Details</h2>
            </div>
            <p className="text-mid-gray text-sm mb-6">Transfer directly to our account. All donations are used transparently for patient care and operations.</p>
            <div className="space-y-3">
              {bankDetails.map(({ label, value }) => (
                <div key={label} className="flex justify-between border-b border-light-gray pb-3">
                  <span className="text-mid-gray text-sm">{label}</span>
                  <span className="text-dark font-medium text-sm">{value}</span>
                </div>
              ))}
            </div>
            <button className="btn-primary flex items-center gap-2 mt-6">
              <FaDownload /> Download Bank Details
            </button>
          </div>

          {/* Other ways + online form placeholder */}
          <div>
            <div className="flex items-center gap-3 mb-6">
              <FaHandHoldingUsd className="text-primary text-2xl" />
              <h2 className="text-2xl font-serif text-dark">Other Ways to Donate</h2>
            </div>

            <div className="space-y-4 mb-8">
              {[
                { title: "In-Person Donation", desc: "Visit our office and contribute directly. Our team will issue an official receipt." },
                { title: "JazzCash / EasyPaisa", desc: "Mobile wallet transfers accepted. Send to 0300-1234567 with reference 'CARE'." },
                { title: "Standing Collection", desc: "We can collect donations from your home or office. Contact us to arrange." },
              ].map(({ title, desc }) => (
                <div key={title} className="flex gap-4 bg-off-white p-4 rounded-card">
                  <span className="w-2 h-2 bg-primary rounded-full mt-2 shrink-0" />
                  <div>
                    <div className="font-semibold text-dark text-sm">{title}</div>
                    <div className="text-mid-gray text-sm">{desc}</div>
                  </div>
                </div>
              ))}
            </div>

            <DonateAmounts />
          </div>
        </div>
      </section>

      {/* Trust statement */}
      <section className="py-12 bg-dark text-white text-center px-4">
        <div className="max-w-2xl mx-auto">
          <p className="text-white/80 italic">
            &ldquo;Your support can save lives. All donations are used transparently for patient care and operations. We are proud to share regular impact reports with all donors.&rdquo;
          </p>
        </div>
      </section>
    </>
  );
}
