#!/usr/bin/env python3
"""
Command-line interface for Microstep Validation.

Usage:
    python scripts/microstep_validate.py list
    python scripts/microstep_validate.py check <step> [<gender> <age>]
    python scripts/microstep_validate.py progress <step> <status> [<gender> <age>] [--details "..."]
    python scripts/microstep_validate.py config <step> [<gender> <age>]
"""

import sys
import argparse
from pathlib import Path

# Add src/Python to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "Python"))

from Tools.MicrostepValidator import (
    MicrostepValidator,
    copilot_check_microstep,
    update_microstep_progress,
    log_microstep_config
)


def cmd_list():
    """List all microsteps."""
    validator = MicrostepValidator()
    validator.list_microsteps()


def cmd_check(step: int, gender: str = None, age: str = None):
    """Perform @copilot check on a microstep."""
    copilot_check_microstep(step, gender, age)


def cmd_progress(step: int, status: str, gender: str = None, age: str = None, details: str = ""):
    """Update progress for a microstep."""
    update_microstep_progress(step, status, details, gender, age)
    print(f"✅ Progress updated: Step {step} - {status}")


def cmd_config(step: int, gender: str = None, age: str = None):
    """Log configuration for a microstep."""
    log_microstep_config(step, gender=gender, age=age)
    print(f"✅ Config logged: Step {step}")


def main():
    parser = argparse.ArgumentParser(
        description="Microstep Validation CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all microsteps
  %(prog)s list
  
  # Check a microstep
  %(prog)s check 2
  %(prog)s check 2 women 18-23
  
  # Update progress
  %(prog)s progress 2 started
  %(prog)s progress 2 completed women 18-23 --details "Generated 20 ideas"
  
  # Log config
  %(prog)s config 2
  %(prog)s config 2 women 18-23
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List command
    subparsers.add_parser('list', help='List all microsteps')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Perform validation check')
    check_parser.add_argument('step', type=int, help='Step number (1-19)')
    check_parser.add_argument('gender', nargs='?', help='Target gender (optional)')
    check_parser.add_argument('age', nargs='?', help='Target age group (optional)')
    
    # Progress command
    progress_parser = subparsers.add_parser('progress', help='Update progress')
    progress_parser.add_argument('step', type=int, help='Step number (1-19)')
    progress_parser.add_argument('status', help='Status (started, in_progress, completed, failed)')
    progress_parser.add_argument('gender', nargs='?', help='Target gender (optional)')
    progress_parser.add_argument('age', nargs='?', help='Target age group (optional)')
    progress_parser.add_argument('--details', default='', help='Additional details')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Log configuration')
    config_parser.add_argument('step', type=int, help='Step number (1-19)')
    config_parser.add_argument('gender', nargs='?', help='Target gender (optional)')
    config_parser.add_argument('age', nargs='?', help='Target age group (optional)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'list':
            cmd_list()
        elif args.command == 'check':
            cmd_check(args.step, args.gender, args.age)
        elif args.command == 'progress':
            cmd_progress(args.step, args.status, args.gender, args.age, args.details)
        elif args.command == 'config':
            cmd_config(args.step, args.gender, args.age)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
