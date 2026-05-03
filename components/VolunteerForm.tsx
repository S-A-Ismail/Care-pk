"use client";

// Must be a Client Component — contains an onSubmit event handler.
// Extracted from app/join-us/page.tsx so the page itself stays server-rendered.

export default function VolunteerForm() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // AWS INTEGRATION POINT (Phase 1):
    // POST to API Gateway → Lambda → DynamoDB (store submission) + SES (confirmation email).
    // Example:
    //   const data = Object.fromEntries(new FormData(e.target as HTMLFormElement));
    //   await fetch(`${process.env.NEXT_PUBLIC_API_URL}/volunteer`, {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(data),
    //   });
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <input type="text" placeholder="First Name" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
        <input type="text" placeholder="Last Name" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      </div>
      <input type="email" placeholder="Email Address" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      <input type="tel" placeholder="Phone Number" className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      <select className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full text-gray-500">
        <option value="">Area of Interest</option>
        <option>Medical / Paramedic</option>
        <option>Community Outreach</option>
        <option>Administration</option>
        <option>Fundraising</option>
        <option>Social Media / Communications</option>
      </select>
      <textarea
        placeholder="Tell us about yourself and why you want to volunteer..."
        rows={4}
        className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full resize-none"
      />
      <button type="submit" className="btn-green w-full">Submit Application</button>
    </form>
  );
}
