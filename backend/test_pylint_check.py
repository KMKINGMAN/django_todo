#!/usr/bin/env python3
"""
Simple script to check if Python files can be imported without syntax errors.
This helps verify that our pylint fixes didn't break anything.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Test imports from the main app
    from app.models import Task, Todo
    from app.serializers import TaskSerializer, TodoSerializer
    from app.views import TaskViewSet, TodoViewSet
    print("✓ All main app imports successful")
    
    # Test test file imports (basic syntax check)
    import ast
    
    test_files = [
        'tests/test_task_api.py',
        'tests/test_todo_api.py', 
        'tests/test_models.py',
        'tests/test_auth_api.py',
        'tests/test_integration.py',
        'tests/factories.py',
    ]
    
    for test_file in test_files:
        try:
            with open(test_file, 'r') as f:
                ast.parse(f.read())
            print(f"✓ {test_file} syntax OK")
        except SyntaxError as e:
            print(f"✗ {test_file} syntax error: {e}")
        except FileNotFoundError:
            print(f"? {test_file} not found")
            
    print("\nPylint fixes validation complete!")
    
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)