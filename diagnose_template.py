"""
Diagnostic script to find what variables your template expects
Run this to see what's missing
"""

import re
import os

def find_template_variables(template_path):
    """Extract all Jinja2 variables from a template"""
    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        return set()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all {{ variable }} patterns
    variables = set(re.findall(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_\.]*)', content))
    
    # Find all {% if variable %} patterns
    if_vars = set(re.findall(r'\{%\s*if\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', content))
    variables.update(if_vars)
    
    # Find all {% for item in variable %} patterns
    for_vars = set(re.findall(r'\{%\s*for\s+\w+\s+in\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', content))
    variables.update(for_vars)
    
    return variables

# Check if running in the actual project directory
template_file = 'templates/admin/reports.html'

if os.path.exists(template_file):
    print("=" * 70)
    print("ANALYZING: templates/admin/reports.html")
    print("=" * 70)
    
    variables = find_template_variables(template_file)
    
    # Filter out common Jinja2 functions/filters
    exclude = {'range', 'loop', 'super', 'self', 'url_for', 'now', 'format', 
               'strftime', 'length', 'items', 'safe', 'tojson'}
    
    variables = {v.split('.')[0] for v in variables if v.split('.')[0] not in exclude}
    
    print("\nVariables expected by template:")
    print("-" * 70)
    for var in sorted(variables):
        print(f"  - {var}")
    
    print("\n" + "=" * 70)
    print(f"Total: {len(variables)} variables")
    print("=" * 70)
else:
    print("ERROR: Template not found!")
    print(f"Looking for: {template_file}")
    print("\nPlease run this script from your project root directory where")
    print("the 'templates' folder exists.")
    print("\nOr provide the path to your reports.html template.")

print("\n")