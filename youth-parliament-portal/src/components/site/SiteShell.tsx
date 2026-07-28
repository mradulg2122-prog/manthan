import type { ReactNode } from "react";
import { Navbar } from "./Navbar";
import { Footer } from "./Footer";

export function SiteShell({
  children,
  hideFooter,
  transparentNav,
}: {
  children: ReactNode;
  hideFooter?: boolean;
  transparentNav?: boolean;
}) {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar transparent={transparentNav} />
      <main className="flex-1">{children}</main>
      {!hideFooter && <Footer />}
    </div>
  );
}
