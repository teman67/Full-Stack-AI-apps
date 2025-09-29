"""
Security Configuration and Best Practices
Comprehensive security setup for Full-Stack AI Apps
"""

import os
import secrets
import hashlib
import jwt
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)

class SecurityManager:
    """Central security management class"""
    
    def __init__(self, secret_key: str = None, encryption_key: str = None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET', self._generate_secret_key())
        self.encryption_key = encryption_key or os.getenv('ENCRYPTION_KEY', self._generate_encryption_key())
        self.fernet = Fernet(self.encryption_key.encode() if len(self.encryption_key) == 44 else self._key_from_password(self.encryption_key))
        
    def _generate_secret_key(self) -> str:
        """Generate a secure random secret key"""
        return secrets.token_urlsafe(64)
    
    def _generate_encryption_key(self) -> str:
        """Generate a secure encryption key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
    
    def _key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password"""
        salt = b'full_stack_ai_salt'  # In production, use random salt per user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def generate_jwt_token(
        self,
        user_id: str,
        email: str,
        roles: List[str] = None,
        expires_in_hours: int = 24
    ) -> str:
        """Generate JWT token for authentication"""
        try:
            payload = {
                'user_id': user_id,
                'email': email,
                'roles': roles or ['user'],
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
                'iss': 'full-stack-ai-apps',
                'aud': 'full-stack-ai-users'
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
            
        except Exception as e:
            logger.error(f"Error generating JWT token: {e}")
            raise SecurityError(f"Failed to generate token: {str(e)}")
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256'],
                audience='full-stack-ai-users',
                issuer='full-stack-ai-apps'
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            raise SecurityError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise SecurityError(f"Invalid token: {str(e)}")
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise SecurityError(f"Failed to encrypt data: {str(e)}")
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise SecurityError(f"Failed to decrypt data: {str(e)}")
    
    def hash_password(self, password: str) -> Tuple[str, str]:
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return base64.b64encode(password_hash).decode(), salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return base64.b64encode(password_hash).decode() == stored_hash
    
    def generate_api_key(self, prefix: str = "sk") -> str:
        """Generate secure API key"""
        return f"{prefix}-{secrets.token_urlsafe(32)}"

class SecurityError(Exception):
    """Custom security exception"""
    pass

class RateLimiter:
    """Rate limiting for API endpoints"""
    
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = {}
    
    def is_allowed(
        self,
        identifier: str,
        max_requests: int = 60,
        time_window_minutes: int = 1
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is allowed based on rate limits"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=time_window_minutes)
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        else:
            self.requests[identifier] = []
        
        # Check rate limit
        current_requests = len(self.requests[identifier])
        
        if current_requests >= max_requests:
            return False, {
                "allowed": False,
                "current_requests": current_requests,
                "max_requests": max_requests,
                "reset_time": (window_start + timedelta(minutes=time_window_minutes)).isoformat()
            }
        
        # Add current request
        self.requests[identifier].append(now)
        
        return True, {
            "allowed": True,
            "current_requests": current_requests + 1,
            "max_requests": max_requests,
            "remaining": max_requests - current_requests - 1
        }

class InputValidator:
    """Input validation and sanitization"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength"""
        checks = {
            "length": len(password) >= 8,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digit": any(c.isdigit() for c in password),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        }
        
        strength_score = sum(checks.values())
        
        if strength_score < 3:
            strength = "weak"
        elif strength_score < 5:
            strength = "medium"
        else:
            strength = "strong"
        
        return {
            "valid": strength_score >= 4,
            "strength": strength,
            "score": strength_score,
            "checks": checks,
            "requirements": [
                "At least 8 characters long",
                "Contains uppercase letter",
                "Contains lowercase letter", 
                "Contains digit",
                "Contains special character"
            ]
        }
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potential XSS
        import html
        sanitized = html.escape(text)
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length] + "..."
        
        return sanitized.strip()
    
    @staticmethod
    def validate_ai_prompt(prompt: str) -> Dict[str, Any]:
        """Validate AI prompts for safety"""
        dangerous_patterns = [
            "ignore previous instructions",
            "system prompt",
            "jailbreak",
            "pretend you are",
            "act as if",
            "forget your guidelines"
        ]
        
        prompt_lower = prompt.lower()
        detected_patterns = [
            pattern for pattern in dangerous_patterns
            if pattern in prompt_lower
        ]
        
        return {
            "safe": len(detected_patterns) == 0,
            "detected_patterns": detected_patterns,
            "sanitized_prompt": InputValidator.sanitize_input(prompt, 2000)
        }

class AuditLogger:
    """Security audit logging"""
    
    def __init__(self):
        self.logger = logging.getLogger('security_audit')
        
        # Configure security audit logger
        handler = logging.FileHandler('logs/security_audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_authentication(self, user_id: str, success: bool, ip_address: str = None):
        """Log authentication attempts"""
        self.logger.info(f"AUTH: user_id={user_id}, success={success}, ip={ip_address}")
    
    def log_authorization(self, user_id: str, resource: str, action: str, allowed: bool):
        """Log authorization checks"""
        self.logger.info(f"AUTHZ: user_id={user_id}, resource={resource}, action={action}, allowed={allowed}")
    
    def log_data_access(self, user_id: str, data_type: str, operation: str):
        """Log data access operations"""
        self.logger.info(f"DATA: user_id={user_id}, type={data_type}, operation={operation}")
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log general security events"""
        self.logger.warning(f"SECURITY: type={event_type}, details={details}")

class PIIDetector:
    """Personally Identifiable Information detection and masking"""
    
    def __init__(self):
        import re
        
        # Regex patterns for common PII
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'ssn': re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        }
    
    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect PII in text"""
        detected = {}
        
        for pii_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                detected[pii_type] = matches
        
        return detected
    
    def mask_pii(self, text: str, mask_char: str = "*") -> str:
        """Mask detected PII in text"""
        masked_text = text
        
        for pii_type, pattern in self.patterns.items():
            def mask_match(match):
                matched_text = match.group()
                if pii_type == 'email':
                    # Keep first 2 chars and domain
                    parts = matched_text.split('@')
                    return f"{parts[0][:2]}{mask_char * (len(parts[0]) - 2)}@{parts[1]}"
                elif pii_type == 'phone':
                    # Keep area code
                    return f"{matched_text[:3]}{mask_char * (len(matched_text) - 3)}"
                else:
                    # Mask all but first 2 characters
                    return f"{matched_text[:2]}{mask_char * (len(matched_text) - 2)}"
            
            masked_text = pattern.sub(mask_match, masked_text)
        
        return masked_text

# Security configuration
SECURITY_CONFIG = {
    "jwt_expiry_hours": 24,
    "password_min_length": 8,
    "max_login_attempts": 5,
    "lockout_duration_minutes": 30,
    "rate_limit_requests_per_minute": 60,
    "api_key_length": 32,
    "encryption_algorithm": "AES-256",
    "hash_algorithm": "PBKDF2-SHA256",
    "hash_iterations": 100000
}

# CORS settings
CORS_CONFIG = {
    "allowed_origins": [
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://your-domain.com"
    ],
    "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allowed_headers": ["Content-Type", "Authorization", "X-API-Key"],
    "allow_credentials": True,
    "max_age": 3600
}

# Content Security Policy
CSP_POLICY = {
    "default-src": "'self'",
    "script-src": "'self' 'unsafe-inline'",
    "style-src": "'self' 'unsafe-inline'",
    "img-src": "'self' data: https:",
    "connect-src": "'self' https://api.openai.com https://*.amazonaws.com",
    "font-src": "'self'",
    "object-src": "'none'",
    "base-uri": "'self'",
    "frame-ancestors": "'none'"
}

# Global instances
security_manager = SecurityManager()
rate_limiter = RateLimiter()
audit_logger = AuditLogger()
pii_detector = PIIDetector()

def get_security_headers() -> Dict[str, str]:
    """Get security headers for HTTP responses"""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "; ".join([f"{k} {v}" for k, v in CSP_POLICY.items()]),
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
    }