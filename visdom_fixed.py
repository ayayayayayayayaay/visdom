#!/usr/bin/env python3

"""
Visdom Environment Auto-Creation Patch

This module provides a patched version of the Visdom class that automatically
handles environment creation when using update="append" with non-existent 
environments. This fixes the issue where no window is created when the 
environment doesn't exist.
"""

import visdom
from visdom import Visdom as OriginalVisdom


class VisdomFixed(OriginalVisdom):
    """
    Enhanced Visdom class with automatic environment creation.
    
    This class extends the original Visdom class to automatically handle
    environment creation when using update="append" with environments
    that don't exist yet.
    """
    
    def scatter(self, X, Y=None, win=None, env=None, opts=None, update=None, name=None):
        """
        Enhanced scatter method with automatic environment creation.
        
        This method wraps the original scatter method to handle the case where
        update="append" is used with a non-existent environment.
        """
        
        # If not using append mode, use original behavior
        if update != "append":
            return super().scatter(X, Y=Y, win=win, env=env, opts=opts, update=update, name=name)
        
        # For append mode, check if we need to create environment/window first
        try:
            # Check if environment exists
            env_list = self.get_env_list()
            env_name = env if env is not None else self.env
            env_exists = env_name in env_list
            
            # Check if window exists (only if environment exists)
            win_exists = False
            if env_exists and win is not None:
                win_exists = self.win_exists(win, env)
                # Handle the case where win_exists returns None (connection error)
                if win_exists is None:
                    win_exists = False
            
            # If environment or window doesn't exist, create it first
            if not env_exists or (win is not None and not win_exists):
                # Create the plot without update mode first
                return super().scatter(X, Y=Y, win=win, env=env, opts=opts, update=None, name=name)
            
            # If both exist, proceed with append
            return super().scatter(X, Y=Y, win=win, env=env, opts=opts, update="append", name=name)
            
        except Exception:
            # If there's any error checking existence, create without update
            return super().scatter(X, Y=Y, win=win, env=env, opts=opts, update=None, name=name)


def create_visdom_fixed(*args, **kwargs):
    """
    Factory function to create a VisdomFixed instance.
    
    This function provides the same interface as creating a regular Visdom
    instance but returns the enhanced version.
    
    Returns:
        VisdomFixed instance
    """
    return VisdomFixed(*args, **kwargs)


# Monkey patch the original Visdom class (optional)
def patch_visdom():
    """
    Monkey patch the original Visdom class with the fixed version.
    
    After calling this function, all new Visdom() instances will use
    the enhanced version with automatic environment creation.
    """
    visdom.Visdom = VisdomFixed


# Example usage and test
if __name__ == "__main__":
    import numpy as np
    
    # Test the fixed version
    print("Testing VisdomFixed with automatic environment creation...")
    
    # Create enhanced Visdom instance
    vis = VisdomFixed()
    
    # Test data
    x_data = np.array([1, 2, 3, 4, 5])
    y_data = np.array([2, 4, 6, 8, 10])
    
    # This should work even if "testenv" doesn't exist
    print("Creating plot with update='append' in non-existent environment...")
    try:
        win = vis.line(y_data, X=x_data, env="testenv", update="append", 
                      opts={"title": "Auto Environment Test"})
        print(f"✓ Success! Plot created in window: {win}")
        
        # Test appending more data
        x_data2 = np.array([6, 7, 8])
        y_data2 = np.array([12, 14, 16])
        vis.line(y_data2, X=x_data2, win=win, env="testenv", update="append")
        print("✓ Successfully appended additional data!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test with scatter plot directly
    print("\nTesting scatter plot with update='append'...")
    try:
        scatter_data = np.random.rand(10, 2)
        win2 = vis.scatter(scatter_data, env="scatterenv", update="append",
                          opts={"title": "Auto Scatter Test"})
        print(f"✓ Success! Scatter plot created in window: {win2}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\nAll tests completed!")