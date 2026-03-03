#!/usr/bin/env python3
"""
Comprehensive test for text window comparison feature enhancement
"""

import numpy as np
import time
from visdom import Visdom

def create_test_environments():
    """Create test environments with both plots and text windows for comparison"""
    print("Creating test environments for comparison...")
    viz = Visdom()
    
    # Check connection
    if not viz.check_connection(timeout_seconds=3):
        print("ERROR: Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        return False
    
    print("✓ Connected to Visdom server")
    
    # Create 3 experiment environments
    environments = ['experiment_run_1', 'experiment_run_2', 'experiment_run_3']
    
    for i, env in enumerate(environments):
        print(f"Creating environment: {env}")
        
        # Create plots with same titles (existing functionality)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x + i * 0.5) + np.random.normal(0, 0.1, 100)
        y2 = np.cos(x + i * 0.3) + np.random.normal(0, 0.1, 100)
        
        # Training Loss plot
        viz.line(Y=y1, X=x, env=env, win='training_loss', 
                opts={'title': 'Training Loss', 'xlabel': 'Epoch', 'ylabel': 'Loss'})
        
        # Validation Accuracy plot  
        viz.line(Y=y2, X=x, env=env, win='val_accuracy',
                opts={'title': 'Validation Accuracy', 'xlabel': 'Epoch', 'ylabel': 'Accuracy'})
        
        # Create text windows with same titles (NEW FUNCTIONALITY)
        config_text = f\"\"\"<h3>Experiment Configuration</h3>\n<ul>\n<li><b>Learning Rate:</b> {0.001 * (i + 1):.4f}</li>\n<li><b>Batch Size:</b> {32 * (2**i)}</li>\n<li><b>Optimizer:</b> {'Adam' if i == 0 else 'SGD' if i == 1 else 'RMSprop'}</li>\n<li><b>Epochs:</b> {100 - i * 20}</li>\n<li><b>Model:</b> ResNet-{18 + i * 16}</li>\n</ul>\"\"\"\n        \n        results_text = f\"\"\"<h3>Final Results</h3>\n<table border=\"1\" style=\"border-collapse: collapse;\">\n<tr><th>Metric</th><th>Value</th></tr>\n<tr><td>Test Accuracy</td><td>{90 + i * 2 + np.random.uniform(-1, 1):.2f}%</td></tr>\n<tr><td>Test Loss</td><td>{0.2 - i * 0.05 + np.random.uniform(-0.02, 0.02):.4f}</td></tr>\n<tr><td>Training Time</td><td>{45 + i * 15} minutes</td></tr>\n<tr><td>Parameters</td><td>{11.2 + i * 5.3:.1f}M</td></tr>\n</table>\"\"\"\n        \n        notes_text = f\"\"\"<h3>Experiment Notes</h3>\n<p><b>Run {i+1} Observations:</b></p>\n<ul>\n<li>{'Converged quickly' if i == 0 else 'Slow convergence' if i == 1 else 'Optimal performance'}</li>\n<li>{'No overfitting' if i % 2 == 0 else 'Some overfitting observed'}</li>\n<li>Memory usage: {2.1 + i * 0.8:.1f}GB</li>\n</ul>\n<p><i>Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}</i></p>\"\"\"\n        \n        # Create text windows that will be compared\n        viz.text(config_text, env=env, win='config', \n                opts={'title': 'Configuration'})\n        \n        viz.text(results_text, env=env, win='results',\n                opts={'title': 'Results Summary'})\n        \n        viz.text(notes_text, env=env, win='notes',\n                opts={'title': 'Experiment Notes'})\n        \n        # Create unique text window (won't be compared)\n        unique_text = f\"<h3>Environment-specific Info</h3><p>This is unique to {env}</p>\"\n        viz.text(unique_text, env=env, win=f'unique_{i}',\n                opts={'title': f'Unique Info {i+1}'})\n        \n        time.sleep(0.5)  # Small delay between environments\n    \n    print(\"✓ Created all test environments\")\n    return True

def print_instructions():
    """Print instructions for testing the comparison feature"""
    print(\"\\n\" + \"=\"*70)\n    print(\"TEXT WINDOW COMPARISON FEATURE TEST\")\n    print(\"=\"*70)\n    \n    print(\"\\n📋 WHAT WAS CREATED:\")\n    print(\"   • 3 environments: experiment_run_1, experiment_run_2, experiment_run_3\")\n    print(\"   • Each environment contains:\")\n    print(\"     - 2 plots with same titles (Training Loss, Validation Accuracy)\")\n    print(\"     - 3 text windows with same titles (Configuration, Results Summary, Experiment Notes)\")\n    print(\"     - 1 unique text window per environment\")\n    \n    print(\"\\n🧪 HOW TO TEST:\")\n    print(\"   1. Open your browser to the Visdom server\")\n    print(\"   2. In the environment selector, choose all 3 environments:\")\n    print(\"      experiment_run_1 + experiment_run_2 + experiment_run_3\")\n    print(\"   3. You should see a comparison view with:\")\n    \n    print(\"\\n✅ EXPECTED RESULTS:\")\n    print(\"   📊 PLOTS (existing feature):\")\n    print(\"      • Training Loss (0, 1, 2, ...) - combined plot with legend\")\n    print(\"      • Validation Accuracy (0, 1, 2, ...) - combined plot with legend\")\n    \n    print(\"   📝 TEXT WINDOWS (NEW feature):\")\n    print(\"      • Configuration (0, 1, 2, ...) - combined text with [0], [1], [2] prefixes\")\n    print(\"      • Results Summary (0, 1, 2, ...) - combined text with [0], [1], [2] prefixes\")\n    print(\"      • Experiment Notes (0, 1, 2, ...) - combined text with [0], [1], [2] prefixes\")\n    \n    print(\"   🚫 NOT SHOWN (as expected):\")\n    print(\"      • Unique Info windows (only appear in single environments)\")\n    \n    print(\"\\n🔍 WHAT TO VERIFY:\")\n    print(\"   ✓ Text windows with same titles are combined\")\n    print(\"   ✓ Each text section is prefixed with [0], [1], [2] indices\")\n    print(\"   ✓ Title shows '(0, 1, 2, ...)' suffix\")\n    print(\"   ✓ Content from all environments is visible\")\n    print(\"   ✓ Unique text windows are filtered out\")\n    print(\"   ✓ Plot comparison still works as before\")\n    \n    print(\"\\n\" + \"=\"*70)\n\ndef main():\n    \"\"\"Main test function\"\"\"\n    print(\"🚀 Starting Text Window Comparison Feature Test\")\n    \n    if create_test_environments():\n        print_instructions()\n        print(\"\\n✅ Test setup complete! Check your browser to verify the feature.\")\n    else:\n        print(\"\\n❌ Test setup failed. Please check your Visdom server connection.\")\n\nif __name__ == '__main__':\n    main()