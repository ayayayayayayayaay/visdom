#!/usr/bin/env python3
"""
Comprehensive demo of text window comparison feature
"""

import time
from visdom import Visdom

def demo_text_comparison():
    """Enhanced demo of text window comparison with multiple scenarios"""
    viz = Visdom()
    
    if not viz.check_connection():
        print("Please start Visdom server: python -m visdom.server")
        return
    
    print("Creating comprehensive text comparison demo...")
    
    # Scenario 1: Model Configurations
    configs = [
        {"model": "ResNet18", "lr": 0.001, "acc": 92.1, "epochs": 50},
        {"model": "ResNet34", "lr": 0.01, "acc": 94.5, "epochs": 45},
        {"model": "ResNet50", "lr": 0.005, "acc": 96.2, "epochs": 60}
    ]
    
    for i, config in enumerate(configs, 1):
        text = f"""<h3>Experiment {i}</h3>
        <b>Model:</b> {config['model']}<br>
        <b>Learning Rate:</b> {config['lr']}<br>
        <b>Accuracy:</b> {config['acc']}%<br>
        <b>Epochs:</b> {config['epochs']}<br>
        <b>Status:</b> <span style='color:green'>✓ Completed</span>
        """
        viz.text(text, env=f'exp_{i}', opts={'title': 'Experiment Config'})
    
    # Scenario 2: Training Logs
    logs = [
        "Epoch 1/50: Loss=2.45, Acc=45.2%\nEpoch 2/50: Loss=1.89, Acc=62.1%\nEpoch 3/50: Loss=1.34, Acc=78.9%",
        "Epoch 1/45: Loss=2.12, Acc=52.3%\nEpoch 2/45: Loss=1.67, Acc=69.4%\nEpoch 3/45: Loss=1.23, Acc=82.1%",
        "Epoch 1/60: Loss=1.98, Acc=58.7%\nEpoch 2/60: Loss=1.45, Acc=74.2%\nEpoch 3/60: Loss=1.12, Acc=85.6%"
    ]
    
    for i, log in enumerate(logs, 1):
        viz.text(f"<pre>{log}</pre>", env=f'exp_{i}', opts={'title': 'Training Log'})
    
    print("✅ Demo environments created!")
    print("\n📊 Available comparisons:")
    print("🔗 All experiments: http://localhost:8097/env/exp_1+exp_2+exp_3")
    print("🔗 Exp 1 vs 2: http://localhost:8097/env/exp_1+exp_2")
    print("🔗 Exp 2 vs 3: http://localhost:8097/env/exp_2+exp_3")
    print("\n📝 Features to observe:")
    print("  • Side-by-side text comparison")
    print("  • Multiple windows per environment")
    print("  • HTML formatting support")
    
    # Add dynamic updates demo
    print("\n⏳ Adding dynamic updates in 3 seconds...")
    time.sleep(3)
    
    for i in range(1, 4):
        update_text = f"""<h4>🔄 Updated Results</h4>
        <b>Final Accuracy:</b> {95.0 + i}%<br>
        <b>Best Epoch:</b> {40 + i*5}<br>
        <b>Updated:</b> {time.strftime('%H:%M:%S')}
        """
        viz.text(update_text, env=f'exp_{i}', opts={'title': 'Live Updates'})
    
    print("✅ Dynamic updates added!")
    print("🔄 Refresh the comparison page to see updates")

if __name__ == '__main__':
    demo_text_comparison()