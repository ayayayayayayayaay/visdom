#!/usr/bin/env python3
"""
Test script to verify text window comparison feature
"""

import time
from visdom import Visdom

def test_text_comparison():
    """Test text window comparison across environments"""
    print("Testing text window comparison feature...")
    
    # Create multiple environments with text windows having same titles
    viz = Visdom()
    
    # Check connection
    if not viz.check_connection(timeout_seconds=3):
        print("ERROR: Cannot connect to Visdom server!")
        print("Please start the server with: python -m visdom.server")
        return
    
    print("✓ Connected to Visdom server")
    
    # Environment 1 - Experiment Run 1
    viz.text("Config for Run 1:<br>Learning Rate: 0.001<br>Batch Size: 32<br>Epochs: 100", 
             env='exp_run_1', win='config', opts={'title': 'Experiment Config'})
    
    viz.text("Results for Run 1:<br>Accuracy: 92.5%<br>Loss: 0.15<br>Time: 45 min", 
             env='exp_run_1', win='results', opts={'title': 'Results'})
    
    # Environment 2 - Experiment Run 2  
    viz.text("Config for Run 2:<br>Learning Rate: 0.01<br>Batch Size: 64<br>Epochs: 50", 
             env='exp_run_2', win='config', opts={'title': 'Experiment Config'})
    
    viz.text("Results for Run 2:<br>Accuracy: 89.2%<br>Loss: 0.22<br>Time: 30 min", 
             env='exp_run_2', win='results', opts={'title': 'Results'})
    
    # Environment 3 - Experiment Run 3
    viz.text("Config for Run 3:<br>Learning Rate: 0.005<br>Batch Size: 128<br>Epochs: 75", 
             env='exp_run_3', win='config', opts={'title': 'Experiment Config'})
    
    viz.text("Results for Run 3:<br>Accuracy: 94.1%<br>Loss: 0.12<br>Time: 60 min", 
             env='exp_run_3', win='results', opts={'title': 'Results'})
    
    print("✓ Created test environments with text windows")
    print("✓ Text windows with same titles: 'Experiment Config' and 'Results'")
    print("\nTo test the comparison feature:")
    print("1. Open your browser to the Visdom server")
    print("2. Compare environments: exp_run_1+exp_run_2+exp_run_3")
    print("3. You should see text windows grouped by title with indices (0, 1, 2)")
    print("4. Each text window should show content from all environments")

if __name__ == '__main__':
    test_text_comparison()