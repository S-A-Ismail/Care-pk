import Hero from "@/components/Hero";
import Stats from "@/components/Stats";
import WhatWeDo from "@/components/WhatWeDo";
import ImpactSection from "@/components/ImpactSection";
import CallToAction from "@/components/CallToAction";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Stats />
      <WhatWeDo />
      <ImpactSection />
      <CallToAction />
    </>
  );
}
