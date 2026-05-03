"use client";

// Must be a Client Component — contains an onSubmit event handler.
// The parent Footer is a Server Component; only this small form is client-side.

export default function NewsletterForm() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // AWS INTEGRATION POINT (Phase 1):
    // POST to API Gateway → Lambda → SES or Mailchimp.
    // Example:
    //   const data = Object.fromEntries(new FormData(e.target as HTMLFormElement));
    //   await fetch(`${process.env.NEXT_PUBLIC_API_URL}/newsletter`, {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(data),
    //   });
  };

  return (
    <form className="flex flex-col gap-2" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Your Name"
        className="bg-green px-3 py-2 text-sm text-white placeholder-white/40 border border-white/20 focus:outline-none focus:border-gold"
      />
      <input
        type="email"
        placeholder="Your Email"
        className="bg-green px-3 py-2 text-sm text-white placeholder-white/40 border border-white/20 focus:outline-none focus:border-gold"
      />
      <button type="submit" className="btn-gold text-center">Subscribe</button>
    </form>
  );
}
