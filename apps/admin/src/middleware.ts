import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const password = process.env.ADMIN_PASSWORD;
  if (!password) {
    return NextResponse.next();
  }

  const auth = request.headers.get("authorization");
  if (auth?.startsWith("Basic ")) {
    try {
      const decoded = atob(auth.slice(6));
      const colon = decoded.indexOf(":");
      const pass = colon >= 0 ? decoded.slice(colon + 1) : decoded;
      if (pass === password) {
        return NextResponse.next();
      }
    } catch {
      // invalid auth header
    }
  }

  return new NextResponse("Authentication required", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="ColourPages Control Center", charset="UTF-8"',
    },
  });
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/health).*)"],
};
