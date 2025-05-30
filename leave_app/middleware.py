from django.db import connection
from django.http import HttpResponse
from django.conf import settings
import os

class ReadOnlyMiddleware:
    """Middleware to handle read-only database operations in Vercel environment.
    
    This middleware intercepts database write operations and provides appropriate
    responses when running in a read-only environment like Vercel.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Skip for static and media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
            
        # Allow read-only operations (GET, HEAD, OPTIONS)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return self.get_response(request)
            
        # For Vercel environment, handle write operations specially
        if 'VERCEL' in os.environ:
            # Allow authentication-related requests to pass through
            if request.path == '/' and request.method == 'POST':
                try:
                    response = self.get_response(request)
                    return response
                except Exception as e:
                    return HttpResponse(
                        "<h1>Login Error</h1>"
                        "<p>There was an error processing your login request.</p>"
                        "<p>Please try using these demo credentials:</p>"
                        "<ul>"
                        "<li>Username: admin, Password: admin123</li>"
                        "<li>Username: manager, Password: manager123</li>"
                        "<li>Username: security, Password: security123</li>"
                        "</ul>"
                        "<p><a href='/'>Return to login</a></p>",
                        content_type='text/html'
                    )
                
            # Allow register page to be displayed
            if request.path == '/register/' and request.method == 'POST':
                return HttpResponse(
                    "<h1>Registration Disabled</h1>"
                    "<p>Registration is disabled in the demo environment.</p>"
                    "<p>Please run the application locally for full functionality.</p>"
                    "<p><a href='/'>Return to login</a></p>",
                    content_type='text/html'
                )
                
            # For other write operations, return a friendly message
            return HttpResponse(
                "<h1>Read-Only Mode</h1>"
                "<p>This demo is running in read-only mode on Vercel.</p>"
                "<p>Database write operations are not supported in this environment.</p>"
                "<p>Please run the application locally for full functionality.</p>",
                content_type='text/html'
            )
            
        # For local environment, proceed normally
        return self.get_response(request)