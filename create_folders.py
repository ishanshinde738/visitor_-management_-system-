import os

# Create necessary directories
directories = [
    'uploads',
    'static/faces',
    'static/epasses',
    'static/images',
    'models',
    'routes',
    'utils',
    'templates/admin',
    'templates/analytics',
    'templates/errors'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    # Create .gitkeep to preserve empty folders in git
    gitkeep_path = os.path.join(directory, '.gitkeep')
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            pass
    print(f"Created: {directory}")

print("\nAll directories created successfully!")