#!/usr/bin/env python3
"""
Dead Code Detector for Python codebase
Finds potentially unused Python modules and functions
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def find_python_files(root_dir: str, exclude_patterns: List[str] = None) -> List[Path]:
    """Find all Python files in the directory tree."""
    if exclude_patterns is None:
        exclude_patterns = [
            'venv', '.venv', '__pycache__', '.pytest_cache',
            'node_modules', 'dist', 'build', 'obsolete', '.git'
        ]
    
    python_files = []
    root_path = Path(root_dir)
    
    for py_file in root_path.rglob('*.py'):
        # Check if file is in excluded directory
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue
        python_files.append(py_file)
    
    return python_files


def extract_definitions(file_path: Path) -> Dict[str, Set[str]]:
    """Extract function and class definitions from a Python file."""
    definitions = {
        'functions': set(),
        'classes': set(),
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find function definitions
        func_pattern = r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        definitions['functions'] = set(re.findall(func_pattern, content, re.MULTILINE))
        
        # Find class definitions
        class_pattern = r'^class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]'
        definitions['classes'] = set(re.findall(class_pattern, content, re.MULTILINE))
        
    except Exception as e:
        print(f"{Colors.RED}Error reading {file_path}: {e}{Colors.NC}")
    
    return definitions


def find_references(file_path: Path, target: str) -> int:
    """Count references to a target identifier in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple pattern: word boundaries around target
        pattern = rf'\b{re.escape(target)}\b'
        matches = re.findall(pattern, content)
        return len(matches)
    except Exception:
        return 0


def analyze_dead_code(root_dir: str) -> Dict[str, List[Dict]]:
    """Analyze Python files for potentially dead code."""
    print(f"{Colors.BLUE}🔍 Analyzing Python code for dead code...{Colors.NC}\n")
    
    python_files = find_python_files(root_dir)
    print(f"Found {len(python_files)} Python files to analyze\n")
    
    # Extract all definitions
    all_definitions = {}
    for py_file in python_files:
        defs = extract_definitions(py_file)
        if defs['functions'] or defs['classes']:
            all_definitions[py_file] = defs
    
    # Check for unused definitions
    results = {
        'unused_functions': [],
        'unused_classes': [],
        'unused_files': []
    }
    
    # Analyze each file
    for file_path, definitions in all_definitions.items():
        module_name = file_path.stem
        
        # Check each function
        for func_name in definitions['functions']:
            # Skip special methods and common patterns
            if func_name.startswith('_') or func_name in ['main', 'test_']:
                continue
            
            # Count references across all files
            total_refs = 0
            for search_file in python_files:
                if search_file == file_path:
                    # In the same file, need at least 2 references (definition + usage)
                    refs = find_references(search_file, func_name)
                    if refs > 1:
                        total_refs += refs - 1  # Subtract the definition
                else:
                    total_refs += find_references(search_file, func_name)
            
            if total_refs == 0:
                results['unused_functions'].append({
                    'file': str(file_path),
                    'name': func_name,
                    'type': 'function'
                })
        
        # Check each class
        for class_name in definitions['classes']:
            total_refs = 0
            for search_file in python_files:
                if search_file == file_path:
                    refs = find_references(search_file, class_name)
                    if refs > 1:
                        total_refs += refs - 1
                else:
                    total_refs += find_references(search_file, class_name)
            
            if total_refs == 0:
                results['unused_classes'].append({
                    'file': str(file_path),
                    'name': class_name,
                    'type': 'class'
                })
    
    return results


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = '.'
    
    print(f"{Colors.GREEN}🧹 Dead Code Detector{Colors.NC}")
    print(f"{'=' * 50}\n")
    print(f"Analyzing directory: {os.path.abspath(root_dir)}\n")
    
    results = analyze_dead_code(root_dir)
    
    # Display results
    print(f"\n{Colors.YELLOW}📊 Results:{Colors.NC}\n")
    
    if results['unused_functions']:
        print(f"{Colors.RED}❌ Potentially unused functions ({len(results['unused_functions'])}):${Colors.NC}")
        for item in results['unused_functions'][:20]:  # Limit output
            print(f"   • {item['name']} in {item['file']}")
        if len(results['unused_functions']) > 20:
            print(f"   ... and {len(results['unused_functions']) - 20} more")
        print()
    
    if results['unused_classes']:
        print(f"{Colors.RED}❌ Potentially unused classes ({len(results['unused_classes'])}):${Colors.NC}")
        for item in results['unused_classes'][:20]:
            print(f"   • {item['name']} in {item['file']}")
        if len(results['unused_classes']) > 20:
            print(f"   ... and {len(results['unused_classes']) - 20} more")
        print()
    
    if not results['unused_functions'] and not results['unused_classes']:
        print(f"{Colors.GREEN}✅ No obvious dead code found!{Colors.NC}\n")
    else:
        print(f"{Colors.YELLOW}⚠️  Warning: This is a simple heuristic analysis.{Colors.NC}")
        print(f"   • Dynamic imports may not be detected")
        print(f"   • Entry points may appear unused")
        print(f"   • String-based references are not detected")
        print(f"   • Always verify manually before deleting!\n")
        
        # Save results to file
        output_file = '/tmp/dead-code-report.txt'
        with open(output_file, 'w') as f:
            f.write("Dead Code Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Unused Functions ({len(results['unused_functions'])}):\n")
            for item in results['unused_functions']:
                f.write(f"  {item['name']} in {item['file']}\n")
            f.write(f"\nUnused Classes ({len(results['unused_classes'])}):\n")
            for item in results['unused_classes']:
                f.write(f"  {item['name']} in {item['file']}\n")
        
        print(f"📄 Full report saved to: {output_file}\n")


if __name__ == '__main__':
    main()
