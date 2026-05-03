"use client";

// Must be a Client Component — manages selected amount state and handles clicks.
// Extracted from app/donate/page.tsx so the page itself stays server-rendered.

import { useState } from "react";

const amounts = [1000, 2500, 5000, 10000, 25000];

export default function DonateAmounts() {
  const [selected, setSelected] = useState<number | null>(null);

  // AWS INTEGRATION POINT (Phase 2):
  // When Stripe or JazzCash is ready:
  // 1. Install @stripe/stripe-js and @stripe/react-stripe-js
  // 2. On "Donate" click, call API Gateway → Lambda → Stripe.createPaymentIntent({ amount: selected })
  // 3. Use the returned client_secret to mount a Stripe Elements checkout
  // 4. STRIPE_SECRET_KEY lives only in the Lambda env — never send it to the browser
  return (
    <div className="border-2 border-dashed border-gold/40 p-6 text-center">
      <div className="text-gold font-semibold mb-2">Online Payment — Coming Soon</div>
      <div className="text-gray-400 text-sm mb-4">
        Secure online donations via card / mobile wallets will be available shortly.
      </div>
      <div className="flex flex-wrap gap-2 justify-center">
        {amounts.map((a) => (
          <button
            key={a}
            onClick={() => setSelected(a)}
            className={`border px-4 py-2 text-sm transition-colors ${
              selected === a
                ? "bg-gold text-green-dark border-gold"
                : "border-gold text-gold hover:bg-gold hover:text-green-dark"
            }`}
          >
            PKR {a.toLocaleString()}
          </button>
        ))}
        <button
          onClick={() => setSelected(null)}
          className="border border-gold text-gold px-4 py-2 text-sm hover:bg-gold hover:text-green-dark transition-colors"
        >
          Custom
        </button>
      </div>
    </div>
  );
}
