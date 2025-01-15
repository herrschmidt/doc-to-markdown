# API Key Security Implementation Plan

This document outlines the implementation of a dual API key system for the Magic-Markdown application, with:
1. A GUI-restricted API key for frontend access
2. A public API key for general API access

---

## 1. **Key Types and Usage**

### GUI API Key
- Used exclusively by the frontend application
- Restricted to same-origin requests
- Lower rate limits (60 requests/minute)
- Automatically injected into frontend requests
- Validated against request origin

### Public API Key
- Available for external API consumers
- No origin restrictions
- Stricter rate limits (30 requests/minute)
- Requires manual configuration by users
- Additional security validations

---

## 2. **Implementation Requirements**

### Backend Changes
1. Update security middleware to:
   - Accept both key types in Authorization header
   - Validate GUI key against request origin
   - Apply different rate limits per key type
   - Log usage separately for auditing
   - Reject expired or revoked keys

2. Add API key management endpoints:
   - `/api/v1/keys` - List active keys
   - `/api/v1/keys/{id}` - Manage specific key
   - `/api/v1/keys/rotate` - Rotate keys

### Frontend Changes
1. Inject GUI API key into all requests
2. Handle key-related errors gracefully
3. Provide UI feedback for rate limits
4. Add developer documentation for API usage

### Nginx Configuration
1. Add CORS restrictions for GUI key
2. Allow public key from any origin
3. Implement rate limiting per key type
4. Add security headers for API endpoints

---

## 3. **Security Considerations**

### Key Generation
- Use cryptographically secure random strings
- Store hashed versions in database
- Implement key rotation policy

### Rate Limiting
- GUI Key: 60 requests/minute
- Public Key: 30 requests/minute
- Implement sliding window algorithm
- Return appropriate HTTP headers

### Monitoring
- Track usage per key
- Detect and block suspicious activity
- Implement automatic key revocation

---

## 4. **Deployment Steps**

1. Add new environment variables:
```env
# GUI API Key
MARKDOWN_GUI_API_KEY=your-secure-gui-key
# Public API Key
MARKDOWN_PUBLIC_API_KEY=your-secure-public-key
```

2. Update security middleware implementation
3. Configure nginx rate limiting
4. Update frontend to use new key system
5. Add API documentation for public key usage
6. Test all security scenarios
7. Deploy to production

---

## 5. **Rollback Plan**

1. Maintain previous API key system
2. Keep old security middleware version
3. Provide migration path for existing users
4. Monitor new system before removing old one

---

## 6. **Documentation Updates**

1. Add API key usage guide
2. Document rate limits
3. Provide examples for both key types
4. Include security best practices
5. Add troubleshooting section

---

This plan provides a comprehensive approach to implementing the dual API key system while maintaining security and usability.
