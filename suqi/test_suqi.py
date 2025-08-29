#!/usr/bin/env python3
"""
Su-Qi Test Suite
Basic functionality tests for the Su-Qi authentication system
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def run_test(description, command, expected_exit_code=0, input_text=None):
    """Run a test command and check results"""
    print(f"\n🧪 Testing: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            input=input_text,
            timeout=30
        )
        
        if result.returncode == expected_exit_code:
            print(f"✅ PASS - Exit code: {result.returncode}")
            if result.stdout:
                print(f"Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ FAIL - Expected exit code {expected_exit_code}, got {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ FAIL - Test timed out")
        return False
    except Exception as e:
        print(f"❌ FAIL - Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("🔮 SU-QI AUTHENTICATION SYSTEM TEST SUITE")
    print("=" * 60)
    
    # Change to suqi directory
    os.chdir(Path(__file__).parent)
    
    # Test results
    results = []
    
    # Test 1: Help message
    results.append(run_test(
        "Help message display",
        "python3 suqi.py --help",
        expected_exit_code=0
    ))
    
    # Test 2: Token creation with passphrase
    results.append(run_test(
        "Token creation with passphrase",
        "python3 suqi.py --create-token --passphrase --token test_passphrase.sq",
        expected_exit_code=0,
        input_text="test_passphrase\n"
    ))
    
    # Test 3: Token creation with generated key
    results.append(run_test(
        "Token creation with generated key",
        "python3 suqi.py --create-token --token test_key.sq",
        expected_exit_code=0
    ))
    
    # Test 4: Authentication success with passphrase
    results.append(run_test(
        "Authentication success with passphrase",
        "python3 suqi.py --token test_passphrase.sq --cmd 'echo Test successful'",
        expected_exit_code=0,
        input_text="test_passphrase\n"
    ))
    
    # Test 5: Authentication failure with wrong passphrase
    results.append(run_test(
        "Authentication failure with wrong passphrase",
        "python3 suqi.py --token test_passphrase.sq --cmd 'echo Should fail'",
        expected_exit_code=1,
        input_text="wrong_passphrase\n"
    ))
    
    # Test 6: Missing command error
    results.append(run_test(
        "Missing command error",
        "python3 suqi.py --token test_passphrase.sq",
        expected_exit_code=1
    ))
    
    # Test 7: File permissions check
    print(f"\n🧪 Testing: Token file permissions")
    token_file = Path("test_passphrase.sq")
    if token_file.exists():
        permissions = oct(token_file.stat().st_mode)[-3:]
        if permissions == "600":
            print("✅ PASS - Token file has correct permissions (600)")
            results.append(True)
        else:
            print(f"❌ FAIL - Token file has permissions {permissions}, expected 600")
            results.append(False)
    else:
        print("❌ FAIL - Token file not found")
        results.append(False)
    
    # Test 8: Log file creation
    print(f"\n🧪 Testing: Log file creation")
    log_file = Path("atlas_beacon.log")
    if log_file.exists() and log_file.stat().st_size > 0:
        print("✅ PASS - Log file exists and has content")
        results.append(True)
    else:
        print("❌ FAIL - Log file missing or empty")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Su-Qi is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())