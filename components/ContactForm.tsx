"use client";

// Must be a Client Component — contains an onSubmit event handler.
// Extracted from app/contact/page.tsx so the page itself stays server-rendered.

export default function ContactForm() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // AWS INTEGRATION POINT (Phase 1):
    // POST to API Gateway → Lambda → SES (forwards message to info@care.org.pk).
    // Example:
    //   const data = Object.fromEntries(new FormData(e.target as HTMLFormElement));
    //   await fetch(`${process.env.NEXT_PUBLIC_API_URL}/contact`, {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(data),
    //   });
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <input type="text" placeholder="Your Name" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
        <input type="email" placeholder="Email Address" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      </div>
      <input type="tel" placeholder="Phone Number (optional)" className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      <input type="text" placeholder="Subject" required className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full" />
      <textarea
        placeholder="Your message..."
        rows={5}
        required
        className="border border-gray-200 px-4 py-3 focus:outline-none focus:border-gold w-full resize-none"
      />
      <button type="submit" className="btn-green w-full">Send Message</button>
    </form>
  );
}
