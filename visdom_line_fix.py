#!/usr/bin/env python3

"""
Optimized Visdom line plotting with automatic environment creation.

This module provides a wrapper function that automatically handles environment
creation when using update="append" with non-existent environments.
"""

import visdom
import numpy as np


def line_with_auto_env(viz, Y, X=None, win=None, env=None, opts=None, update=None, name=None):
    """
    Enhanced line plotting function that automatically creates environments.
    
    This function wraps the standard visdom.line() method to handle the case where
    update="append" is used with a non-existent environment. It automatically
    creates the environment and window on the first call, then uses append for
    subsequent calls.
    
    Args:
        viz: Visdom instance
        Y: Data for Y-axis (same as visdom.line)
        X: Data for X-axis (same as visdom.line) 
        win: Window name (same as visdom.line)
        env: Environment name (same as visdom.line)
        opts: Options dict (same as visdom.line)
        update: Update mode - 'append', 'replace', etc. (same as visdom.line)
        name: Trace name (same as visdom.line)
        
    Returns:
        Window ID from the visdom call
    """
    
    # If not using append mode, use standard behavior
    if update != "append":
        return viz.line(Y, X=X, win=win, env=env, opts=opts, update=update, name=name)
    
    # For append mode, check if environment and window exist
    env_exists = env in viz.get_env_list() if env else True
    win_exists = viz.win_exists(win, env) if win and env_exists else False
    
    # If environment or window doesn't exist, create it first without update
    if not env_exists or not win_exists:
        return viz.line(Y, X=X, win=win, env=env, opts=opts, update=None, name=name)
    
    # If both exist, use append mode
    return viz.line(Y, X=X, win=win, env=env, opts=opts, update="append", name=name)


# Example usage
if __name__ == "__main__":
    # Create Visdom instance
    vis = visdom.Visdom()
    
    # Test data
    x_data = np.array([1, 2, 3, 4, 5])
    y_data = np.array([2, 4, 6, 8, 10])
    
    # This will work even if "newenv" doesn't exist
    win = line_with_auto_env(vis, y_data, X=x_data, env="newenv", update="append", 
                            opts={"title": "Auto Environment Creation"})
    
    # Subsequent calls will append correctly
    x_data2 = np.array([6, 7, 8])
    y_data2 = np.array([12, 14, 16])
    line_with_auto_env(vis, y_data2, X=x_data2, win=win, env="newenv", update="append")
    
    print(f"Plot created in window: {win}")
    print("Environment 'newenv' created automatically!")