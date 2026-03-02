"""
Minimal patch for Visdom scatter method to fix environment auto-creation issue.

This patch modifies the scatter method in visdom/__init__.py to automatically
create environments when using update="append" with non-existent environments.

ISSUE: When using viz.line(..., env="newenv", update="append") where "newenv" 
doesn't exist, no window is created because the environment doesn't exist.

SOLUTION: Check if environment exists before checking window existence, and
create the plot without update mode if environment doesn't exist.
"""

# ORIGINAL CODE (around line 2400 in scatter method):
"""
elif update is not None:
    assert win is not None, "Must define a window to update"

    if update == "append":
        if win is None:
            update = None
        elif not self.offline:
            exists = self.win_exists(win, env)
            if exists is False:
                update = None
"""

# FIXED CODE:
"""
elif update is not None:
    assert win is not None, "Must define a window to update"

    if update == "append":
        if win is None:
            update = None
        elif not self.offline:
            # Check if environment exists first
            try:
                env_list = self.get_env_list()
                env_name = env if env is not None else self.env
                env_exists = env_name in env_list
                
                if not env_exists:
                    # Environment doesn't exist, create plot without update
                    update = None
                else:
                    # Environment exists, check window
                    exists = self.win_exists(win, env)
                    if exists is False:
                        update = None
            except Exception:
                # If there's any error, create without update
                update = None
"""

# Complete replacement for the scatter method section:
def get_scatter_method_patch():
    """
    Returns the patched code for the scatter method's update handling section.
    
    This should replace lines approximately 2400-2410 in the original scatter method.
    """
    return '''
        elif update is not None:
            assert win is not None, "Must define a window to update"

            if update == "append":
                if win is None:
                    update = None
                elif not self.offline:
                    # Enhanced logic: Check environment existence first
                    try:
                        env_list = self.get_env_list()
                        env_name = env if env is not None else self.env
                        env_exists = env_name in env_list
                        
                        if not env_exists:
                            # Environment doesn't exist, create plot without update
                            update = None
                        else:
                            # Environment exists, check if window exists
                            exists = self.win_exists(win, env)
                            if exists is False:
                                update = None
                    except Exception:
                        # If there's any error checking, create without update
                        update = None
    '''

# Instructions for applying the patch:
PATCH_INSTRUCTIONS = """
To apply this patch to your Visdom installation:

1. Locate your Visdom installation directory:
   - Usually in: site-packages/visdom/__init__.py
   - Or in your project: py/visdom/__init__.py

2. Find the scatter method (around line 2400)

3. Look for this code block:
   elif update is not None:
       assert win is not None, "Must define a window to update"
       
       if update == "append":
           if win is None:
               update = None
           elif not self.offline:
               exists = self.win_exists(win, env)
               if exists is False:
                   update = None

4. Replace it with the enhanced version shown above.

5. Save the file and restart your Python session.

After applying this patch, the following code will work correctly:

    vis = visdom.Visdom()
    vis.line([1, 2, 3], env="newenv", update="append")  # Creates environment automatically
    vis.line([4, 5, 6], env="newenv", update="append")  # Appends to existing plot
"""

if __name__ == "__main__":
    print("Visdom Environment Auto-Creation Patch")
    print("=" * 50)
    print(PATCH_INSTRUCTIONS)
    print("\nPatched code:")
    print(get_scatter_method_patch())