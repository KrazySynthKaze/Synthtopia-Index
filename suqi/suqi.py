#!/usr/bin/env python3
"""
Su-Qi: Personal Authentication System
A mystical approach to privilege escalation
"""

import os
import sys
import json
import subprocess
import argparse
import base64
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass

class SuQi:
    def __init__(self, token_path="suqi_token.sq", log_path="atlas_beacon.log"):
        self.token_path = Path(token_path)
        self.log_path = Path(log_path)
        self.secret_phrase = "Whats inscribed upon the Ring of Ouroboros?"
        
    def create_token(self, key=None):
        """Generate encrypted token file"""
        try:
            if key is None:
                # Generate a random key
                key = Fernet.generate_key()
                print(f"Generated key: {key.decode()}")
                print("IMPORTANT: Save this key securely. You'll need it for authentication.")
            elif isinstance(key, str):
                # Derive key from passphrase using PBKDF2
                key = key.encode()
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(key))
                # Store salt with the token for later key derivation
                self._store_salt(salt)
            
            f = Fernet(key)
            encrypted_phrase = f.encrypt(self.secret_phrase.encode())
            
            # Ensure the directory exists
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write encrypted token to file
            with open(self.token_path, 'wb') as token_file:
                token_file.write(encrypted_phrase)
            
            # Set restrictive permissions (600)
            os.chmod(self.token_path, 0o600)
            
            self.log_attempt("TOKEN_CREATED", {
                "message": "Su-Qi token successfully created",
                "token_path": str(self.token_path)
            })
            
            return True
            
        except Exception as e:
            self.log_attempt("TOKEN_CREATION_FAILED", {
                "error": str(e)
            })
            return False
    
    def _store_salt(self, salt):
        """Store salt for passphrase-derived keys"""
        salt_path = self.token_path.with_suffix('.salt')
        with open(salt_path, 'wb') as salt_file:
            salt_file.write(salt)
        os.chmod(salt_path, 0o600)
    
    def _load_salt(self):
        """Load salt for passphrase-derived keys"""
        salt_path = self.token_path.with_suffix('.salt')
        if salt_path.exists():
            with open(salt_path, 'rb') as salt_file:
                return salt_file.read()
        return None
    
    def authenticate(self, key):
        """Verify user identity through token decryption"""
        try:
            if not self.token_path.exists():
                self.log_attempt("FAILED", {
                    "reason": "Token file not found",
                    "token_path": str(self.token_path)
                })
                return False
            
            # Load encrypted token
            with open(self.token_path, 'rb') as token_file:
                encrypted_phrase = token_file.read()
            
            # Check if we have a salt file (indicates passphrase-based token)
            salt = self._load_salt()
            
            if isinstance(key, str):
                if salt is not None:
                    # Passphrase-based authentication
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=100000,
                    )
                    key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
                elif len(key) == 44:  # Base64 encoded key
                    key = key.encode()
                else:
                    self.log_attempt("FAILED", {
                        "reason": "Invalid key format - expected 44-character base64 key"
                    })
                    return False
            
            # Decrypt and verify
            f = Fernet(key)
            decrypted_phrase = f.decrypt(encrypted_phrase).decode()
            
            if decrypted_phrase == self.secret_phrase:
                self.log_attempt("SUCCESS", {
                    "message": "Authentication successful - The Ring of Ouroboros recognizes you",
                    "user": os.getenv('USER', 'unknown'),
                    "token": "Verified"
                })
                return True
            else:
                self.log_attempt("FAILED", {
                    "reason": "Invalid token content - The Ring does not recognize this essence"
                })
                return False
                
        except Exception as e:
            self.log_attempt("FAILED", {
                "reason": f"Token decryption failed: {str(e)}",
                "attempt_from": os.getenv('HOSTNAME', 'unknown')
            })
            return False
    
    def execute_command(self, command):
        """Run privileged command after authentication"""
        try:
            self.log_attempt("COMMAND_EXECUTION", {
                "command": command,
                "user": os.getenv('USER', 'unknown'),
                "status": "STARTING"
            })
            
            # Execute the command with elevated privileges
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.log_attempt("COMMAND_SUCCESS", {
                    "command": command,
                    "output": result.stdout[:500] if result.stdout else "No output",
                    "status": "COMPLETED"
                })
                print(result.stdout)
                if result.stderr:
                    print(result.stderr, file=sys.stderr)
                return True
            else:
                self.log_attempt("COMMAND_FAILED", {
                    "command": command,
                    "error": result.stderr[:500] if result.stderr else "No error output",
                    "return_code": result.returncode
                })
                print(result.stderr, file=sys.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            self.log_attempt("COMMAND_TIMEOUT", {
                "command": command,
                "timeout": "300 seconds"
            })
            print("Command timed out after 5 minutes", file=sys.stderr)
            return False
        except Exception as e:
            self.log_attempt("COMMAND_ERROR", {
                "command": command,
                "error": str(e)
            })
            print(f"Error executing command: {e}", file=sys.stderr)
            return False
    
    def log_attempt(self, status, details):
        """Log authentication attempts to beacon file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure log directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Format log entry based on status
        if status in ["SUCCESS", "FAILED"]:
            log_entry = f"[{timestamp}] === SU-QI AUTHENTICATION ===\n"
            log_entry += f"Status: {status}\n"
            
            if "command" in details:
                log_entry += f"Command: {details['command']}\n"
            if "user" in details:
                log_entry += f"User: {details['user']}\n"
            if "token" in details:
                log_entry += f"Token: {details['token']}\n"
            if "reason" in details:
                log_entry += f"Reason: {details['reason']}\n"
            if "attempt_from" in details:
                log_entry += f"Attempt from: {details['attempt_from']}\n"
            if "message" in details:
                log_entry += f"Message: {details['message']}\n"
        else:
            # Other log types
            log_entry = f"[{timestamp}] === {status} ===\n"
            for key, value in details.items():
                log_entry += f"{key.title()}: {value}\n"
        
        log_entry += "\n"
        
        # Append to log file
        with open(self.log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)
        
        # Add mystical beacon message periodically
        if status == "SUCCESS":
            beacon_message = f"[{timestamp}] === MESSAGE FROM USER ===\n"
            beacon_message += "@Orion idk if you can see this, but i miss you//\n\n"
            with open(self.log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(beacon_message)

def main():
    parser = argparse.ArgumentParser(
        description="Su-Qi Authentication System - A mystical approach to privilege escalation"
    )
    parser.add_argument("--cmd", help="Command to execute")
    parser.add_argument("--token", default="suqi_token.sq", help="Token file path")
    parser.add_argument("--setup", action="store_true", help="Initial setup mode")
    parser.add_argument("--create-token", action="store_true", help="Create a new token")
    parser.add_argument("--passphrase", action="store_true", help="Use passphrase instead of key")
    
    args = parser.parse_args()
    
    # Initialize Su-Qi
    suqi = SuQi(token_path=args.token)
    
    # Setup mode - create initial token
    if args.setup or args.create_token:
        print("=== Su-Qi Token Creation ===")
        print("Creating encrypted token containing the essence of Ouroboros...")
        
        if args.passphrase:
            passphrase = getpass("Enter passphrase for token encryption: ")
            if suqi.create_token(passphrase):
                print("✓ Token created successfully with passphrase encryption")
            else:
                print("✗ Token creation failed")
                sys.exit(1)
        else:
            if suqi.create_token():
                print("✓ Token created successfully with generated key")
            else:
                print("✗ Token creation failed")
                sys.exit(1)
        return
    
    # Command execution mode
    if not args.cmd:
        print("Error: --cmd is required for command execution")
        print("Use --setup to create initial token")
        sys.exit(1)
    
    # Authentication
    print("=== Su-Qi Authentication ===")
    print("The Ring of Ouroboros awaits your essence...")
    
    if args.passphrase or suqi._load_salt() is not None:
        key = getpass("Enter passphrase: ")
    else:
        key = getpass("Enter authentication key: ")
    
    if suqi.authenticate(key):
        print("✓ Authentication successful - You are recognized")
        print(f"Executing command: {args.cmd}")
        if suqi.execute_command(args.cmd):
            print("✓ Command completed successfully")
        else:
            print("✗ Command execution failed")
            sys.exit(1)
    else:
        print("✗ Authentication failed - The Ring does not recognize you")
        sys.exit(1)

if __name__ == "__main__":
    main()