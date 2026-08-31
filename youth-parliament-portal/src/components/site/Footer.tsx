import { Link } from "@tanstack/react-router";
import glaLogo from "@/assets/gla-logo.png";
import saturangleLogo from "@/assets/saturangle-logo.png";
import { Phone, MapPin, Mail, Mic } from "lucide-react";

export function Footer() {
  return (
    <footer className="mt-20 border-t border-[#DDD7C9] bg-[#FFFFFF]">
      <div className="mx-auto max-w-7xl px-6 lg:px-10 py-14">
        <div className="grid gap-10 md:grid-cols-12">
          {/* Col 1: Brand */}
          <div className="md:col-span-5 space-y-4">
            <div className="flex items-center gap-4">
              <img src={glaLogo} alt="GLA University" className="h-12 w-auto object-contain" loading="lazy" />
              <div className="h-7 w-px bg-[#DDD7C9]" />
              <img src={saturangleLogo} alt="Saturangle — The Debate Club" className="h-10 w-auto object-contain" loading="lazy" />
            </div>
            <div className="pt-2">
              <div className="text-xs font-bold tracking-[0.2em] uppercase text-[#C49A45]">
                PRARAMBH 2K26
              </div>
              <h3 className="text-xl font-serif font-bold text-[#102A43] mt-1">
                MANTHAN <span className="text-sm font-sans font-medium text-[#627D98]">| The Freshers' Showdown</span>
              </h3>
              <p className="mt-2 text-sm text-[#627D98] max-w-sm leading-relaxed">
                A prestigious debate and public-speaking competition for freshers hosted by Saturangle – The Debate Club of GLA University.
              </p>
              <p className="mt-2 text-xs italic font-serif text-[#C49A45]">
                "Speak. Stand out. Conquer."
              </p>
            </div>
          </div>

          {/* Col 2: Navigation Links */}
          <div className="md:col-span-3">
            <div className="eyebrow">Quick Links</div>
            <ul className="mt-4 space-y-2.5 text-sm text-[#102A43]/85 font-medium">
              <li>
                <Link to="/register" className="hover:text-[#C49A45] transition-colors">
                  Participant Registration
                </Link>
              </li>
              <li>
                <Link to="/volunteer-login" className="hover:text-[#C49A45] transition-colors">
                  Volunteer Portal & Scanner
                </Link>
              </li>
              <li>
                <Link to="/admin-login" className="hover:text-[#C49A45] transition-colors">
                  Admin Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Coordinators & Contact */}
          <div className="md:col-span-4">
            <div className="eyebrow">Event Coordinators</div>
            <ul className="mt-4 space-y-3 text-sm text-[#102A43]/85">
              <li className="flex items-start gap-2.5">
                <Phone className="h-4 w-4 text-[#C49A45] shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-[#102A43]">Mradul Gaur</span>
                  <div className="text-xs text-[#627D98] font-mono">+91 7417255432</div>
                </div>
              </li>
              <li className="flex items-start gap-2.5">
                <Phone className="h-4 w-4 text-[#C49A45] shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold text-[#102A43]">Nakshtra Chaudhary</span>
                  <div className="text-xs text-[#627D98] font-mono">+91 9258626362</div>
                </div>
              </li>
              <li className="flex items-center gap-2.5 pt-1 text-xs text-[#627D98]">
                <MapPin className="h-3.5 w-3.5 text-[#C49A45] shrink-0" />
                <span>GLA University, Mathura</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="gold-divider mt-10" />

        <div className="mt-6 flex flex-wrap items-center justify-between gap-4 text-xs text-[#627D98]">
          <span>© {new Date().getFullYear()} Saturangle – The Debate Club, GLA University. All rights reserved.</span>
          <span className="font-semibold tracking-wider uppercase text-[#102A43]">
            PRARAMBH 2K26 · MANTHAN
          </span>
        </div>
      </div>
    </footer>
  );
}
