import Link from "next/link";

export default function CallToAction() {
  return (
    <section className="bg-green py-16 text-white text-center px-4">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-serif mb-4">Ready to Make a Difference?</h2>
        <p className="text-white/70 mb-8 text-lg">
          Your support — whether through donations, volunteering, or spreading the word — helps us reach more people in need.
        </p>
        <div className="flex flex-wrap gap-4 justify-center">
          <Link href="/donate" className="btn-gold">Donate Now</Link>
          <Link href="/join-us" className="btn-outline">Volunteer With Us</Link>
        </div>
      </div>
    </section>
  );
}
