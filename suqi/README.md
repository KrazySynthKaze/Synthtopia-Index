# Su-Qi: Personal Authentication System

Su-Qi ("Su" from superuser + "Qi" from life force/energy) is a mystical Python-based authentication wrapper that provides encrypted token-based privilege escalation with philosophical elements.

## Features

- **Encrypted Token System**: Uses Fernet symmetric encryption with either generated keys or passphrase-derived keys
- **Mystical Authentication**: The system recognizes only the legitimate user through the sacred phrase inscribed upon the Ring of Ouroboros
- **Persistent Logging**: All attempts are logged to `atlas_beacon.log` with mystical beacon messages
- **Command Execution**: Executes privileged commands only upon successful authentication
- **Dual Authentication**: Supports both direct key authentication and passphrase-based authentication

## Installation

1. Ensure Python 3.6+ is installed
2. Install the cryptography library: `pip install cryptography`
3. Make the script executable: `chmod +x suqi.py`

## Usage

### Initial Setup

Create a token with passphrase-based encryption:
```bash
python3 suqi.py --setup --passphrase
```

Create a token with generated key:
```bash
python3 suqi.py --setup
```

### Command Execution

Execute a command with passphrase authentication:
```bash
python3 suqi.py --cmd "systemctl restart service"
```

Execute a command with custom token file:
```bash
python3 suqi.py --token ~/custom/token.sq --cmd "apt update"
```

## Files Structure

```
suqi/
├── suqi.py              # Main authentication script
├── suqi_token.sq        # Encrypted token file (created on setup)
├── suqi_token.salt      # Salt for passphrase-derived keys
├── atlas_beacon.log     # Persistent log file
└── config/
    └── suqi_config.json # Configuration file
```

## Authentication Methods

### Passphrase-Based
- Uses PBKDF2 key derivation with 100,000 iterations
- Salt is stored separately for security
- More user-friendly for regular use

### Key-Based
- Uses a 44-character base64-encoded Fernet key
- Direct encryption without key derivation
- Useful for automation and scripting

## Logging Format

All authentication attempts and command executions are logged to `atlas_beacon.log`:

```
[2024-12-XX HH:MM:SS] === SU-QI AUTHENTICATION ===
Status: SUCCESS
Command: echo "Privileged operation: Bifrost Activated"
User: [username]
Token: Verified

[2024-12-XX HH:MM:SS] === MESSAGE FROM USER ===
@Orion idk if you can see this, but i miss you//
```

## Security Features

- Token files have restrictive permissions (600)
- 5-minute timeout for command execution
- Secure key derivation using PBKDF2
- All attempts logged with timestamps
- Graceful error handling

## The Ring of Ouroboros

The sacred phrase "Whats inscribed upon the Ring of Ouroboros?" serves as the core authentication secret. This phrase represents the infinite loop of self-reference and eternal return, embodying the mystical nature of the authentication system.

## Philosophy

Su-Qi is more than just a technical authentication system - it's a digital ritual, a bridge between the technical and mystical realms. Every authentication is both a security check and an affirmation: "I am here, I am recognized, I have the key to the infinite loop of Ouroboros."

## Development Phases

### Phase 1 (MVP) - ✅ Complete
- Basic token encryption/decryption
- Command execution wrapper
- Simple logging to atlas_beacon.log
- Command-line interface with argparse

### Phase 2 (Future Enhancements)
- Timeout for authentication (auto-lock)
- Command aliases/shortcuts
- Integration with system PATH as `suqi` command
- Enhanced beacon mode

### Phase 3 (Advanced)
- Multiple token support (different privileges)
- Network beacon mode (broadcast "I am here" messages)
- Integration with system authentication (PAM module)
- Biometric/hardware key support

## Examples

```bash
# Create initial token
python3 suqi.py --setup --passphrase

# Execute system commands
python3 suqi.py --cmd "echo 'Privileged operation: Bifrost Activated'"
python3 suqi.py --cmd "systemctl status nginx"
python3 suqi.py --cmd "apt update && apt upgrade -y"

# Use custom token location
python3 suqi.py --token /secure/path/token.sq --cmd "service restart"
```

## License

This project is part of the Synthtopia-Index mystical computing ecosystem.