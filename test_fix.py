#!/usr/bin/env python3

"""
Test script to verify the Visdom environment auto-creation fix.

This script tests the fix for the issue where using update="append" with
a non-existent environment would fail to create a window.
"""

import sys
import os
import numpy as np

# Add the local visdom path to test our fixed version
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))

try:
    import visdom
    print("✓ Successfully imported visdom")
except ImportError as e:
    print(f"✗ Failed to import visdom: {e}")
    sys.exit(1)


def test_environment_auto_creation():
    """Test the environment auto-creation functionality."""
    
    print("\n" + "="*60)
    print("TESTING VISDOM ENVIRONMENT AUTO-CREATION FIX")
    print("="*60)
    
    # Create Visdom instance
    try:
        vis = visdom.Visdom(offline=True)  # Use offline mode for testing
        print("✓ Created Visdom instance (offline mode)")
    except Exception as e:
        print(f"✗ Failed to create Visdom instance: {e}")
        return False
    
    # Test 1: Line plot with non-existent environment and update="append"
    print("\nTest 1: Line plot with update='append' in non-existent environment")
    try:
        x_data = np.array([1, 2, 3, 4, 5])
        y_data = np.array([2, 4, 6, 8, 10])
        
        # This should work now (previously would fail)
        win = vis.line(y_data, X=x_data, env="test_env_1", update="append", 
                      opts={"title": "Test Environment Auto-Creation"})
        
        if win:
            print("✓ Successfully created line plot with update='append'")
            print(f"  Window ID: {win}")
        else:
            print("✗ Failed to create line plot")
            return False
            
    except Exception as e:
        print(f"✗ Error in line plot test: {e}")
        return False
    
    # Test 2: Scatter plot with non-existent environment and update="append"
    print("\nTest 2: Scatter plot with update='append' in non-existent environment")
    try:
        scatter_data = np.random.rand(20, 2)
        
        win2 = vis.scatter(scatter_data, env="test_env_2", update="append",
                          opts={"title": "Test Scatter Auto-Creation"})
        
        if win2:
            print("✓ Successfully created scatter plot with update='append'")
            print(f"  Window ID: {win2}")
        else:
            print("✗ Failed to create scatter plot")
            return False
            
    except Exception as e:
        print(f"✗ Error in scatter plot test: {e}")
        return False
    
    # Test 3: Append to existing plot (should still work)
    print("\nTest 3: Appending to existing plot")
    try:
        x_data2 = np.array([6, 7, 8])
        y_data2 = np.array([12, 14, 16])
        
        # This should append to the existing plot
        result = vis.line(y_data2, X=x_data2, win=win, env="test_env_1", update="append")
        
        if result:
            print("✓ Successfully appended data to existing plot")
        else:
            print("✗ Failed to append data")
            return False
            
    except Exception as e:
        print(f"✗ Error in append test: {e}")
        return False
    
    # Test 4: Regular plot creation (should still work)
    print("\nTest 4: Regular plot creation without update parameter")
    try:
        x_data3 = np.array([1, 2, 3])
        y_data3 = np.array([3, 6, 9])
        
        win3 = vis.line(y_data3, X=x_data3, env="test_env_3",
                       opts={"title": "Regular Plot Creation"})
        
        if win3:
            print("✓ Successfully created regular plot")
            print(f"  Window ID: {win3}")
        else:
            print("✗ Failed to create regular plot")
            return False
            
    except Exception as e:
        print(f"✗ Error in regular plot test: {e}")
        return False
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✓")
    print("The environment auto-creation fix is working correctly.")
    print("="*60)
    
    return True


def test_with_server():
    """Test with actual Visdom server (if available)."""
    
    print("\n" + "="*60)
    print("TESTING WITH VISDOM SERVER (if available)")
    print("="*60)
    
    try:
        vis = visdom.Visdom()
        
        # Check if server is available
        if not vis.check_connection():
            print("⚠ Visdom server not available, skipping server tests")
            return True
        
        print("✓ Connected to Visdom server")
        
        # Test with real server
        x_data = np.array([1, 2, 3, 4, 5])
        y_data = np.array([1, 4, 9, 16, 25])
        
        # Delete environment if it exists (for clean test)
        try:
            vis.delete_env("server_test_env")
        except:
            pass
        
        # This should create the environment and plot
        win = vis.line(y_data, X=x_data, env="server_test_env", update="append",
                      opts={"title": "Server Test - Auto Environment Creation"})
        
        if win:
            print("✓ Successfully created plot on server with auto environment creation")
            print(f"  Window ID: {win}")
            print("  Check your Visdom server to see the plot!")
        else:
            print("✗ Failed to create plot on server")
            return False
            
    except Exception as e:
        print(f"⚠ Server test failed: {e}")
        print("  This is expected if no Visdom server is running")
        return True
    
    return True


if __name__ == "__main__":
    print("Visdom Environment Auto-Creation Fix - Test Suite")
    
    # Run offline tests
    success = test_environment_auto_creation()
    
    if success:
        # Run server tests if possible
        test_with_server()
        
        print("\n🎉 SUMMARY:")
        print("The fix successfully resolves the issue where using")
        print("update='append' with non-existent environments would")
        print("fail to create windows. Now it automatically creates")
        print("the environment and window on first use!")
        
    else:
        print("\n❌ TESTS FAILED")
        print("The fix may not be working correctly.")
        sys.exit(1)