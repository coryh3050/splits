import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';

// Middleware to verify JWT token and protect routes
export function middleware(request) {
  try {
    // Get token from Authorization header
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Unauthorized - No token provided' }, { status: 401 });
    }
    
    const token = authHeader.split(' ')[1];
    
    // Verify token
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key');
      
      // Add user ID to request headers for downstream handlers
      const requestHeaders = new Headers(request.headers);
      requestHeaders.set('X-User-ID', decoded.userId);
      
      // Return modified request
      return NextResponse.next({
        request: {
          headers: requestHeaders,
        },
      });
    } catch (error) {
      return NextResponse.json({ error: 'Unauthorized - Invalid token' }, { status: 401 });
    }
  } catch (error) {
    console.error('Auth middleware error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// Configure which routes use this middleware
export const config = {
  matcher: [
    '/api/users/:path*',
    '/api/upload/:path*',
    '/api/videos/:path*',
    '/api/analytics/:path*',
    '/api/settings/:path*',
    '/api/promotion/:path*',
  ],
};
