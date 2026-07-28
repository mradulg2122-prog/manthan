import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";
import ReactGA from "react-ga4";
import Clarity from "@microsoft/clarity";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <p className="eyebrow justify-center">Error 404</p>
        <h1 className="mt-4 text-5xl font-serif text-foreground">Page not found</h1>
        <div className="gold-divider my-6 w-24 mx-auto" />
        <p className="mt-2 text-sm text-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div className="mt-8">
          <Link to="/" className="btn-primary">Return to Home</Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportLovableError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-2xl font-serif text-foreground">This page didn't load</h1>
        <div className="gold-divider my-6 w-24 mx-auto" />
        <p className="mt-2 text-sm text-muted-foreground">
          Something went wrong. Please try again or return home.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <button onClick={() => { router.invalidate(); reset(); }} className="btn-primary">Try again</button>
          <a href="/" className="btn-outline">Go home</a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "Youth Parliament 6.0 — Official Registration Portal | Saturangle × GLA University" },
      { name: "description", content: "Official registration for Youth Parliament 6.0, hosted by Saturangle, the official debate club of GLA University. Where voices become leaders." },
      { name: "author", content: "Saturangle Debate Club — GLA University" },
      { property: "og:title", content: "Youth Parliament 6.0 — Official Registration Portal" },
      { property: "og:description", content: "Join the flagship parliamentary debate experience hosted by Saturangle at GLA University." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "icon", type: "image/png", href: "/favicon.png" },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  const router = useRouter();

  useEffect(() => {
    const gaId = import.meta.env.VITE_GA_MEASUREMENT_ID;
    if (gaId && gaId !== "YOUR_MEASUREMENT_ID") {
      ReactGA.initialize(gaId);
      ReactGA.send({ hitType: "pageview", page: window.location.pathname });

      const unsubscribe = router.subscribe("onResolved", (event) => {
        ReactGA.send({ hitType: "pageview", page: event.toLocation.pathname });
      });
      return unsubscribe;
    }
  }, [router]);

  useEffect(() => {
    const clarityId = import.meta.env.VITE_CLARITY_PROJECT_ID;
    if (clarityId && clarityId !== "YOUR_CLARITY_PROJECT_ID") {
      Clarity.init(clarityId);
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <Outlet />
    </QueryClientProvider>
  );
}
