"""
Authentication module for Google Earth Engine

Handles GEE authentication and initialization with standard methods.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
import os
import sys
from typing import Optional


def authenticate(auth_mode: str = "notebook") -> None:
    """
    Authenticate with Google Earth Engine.
    
    This function handles the authentication process for GEE. It supports
    multiple authentication modes for different environments.
    
    Parameters
    ----------
    auth_mode : str, optional
        Authentication mode. Options:
        - 'notebook': For Jupyter notebooks (default)
        - 'colab': For Google Colab
        - 'gcloud': For gcloud authentication
        - 'service_account': For service account authentication
    
    Examples
    --------
    >>> import geeadvance
    >>> geeadvance.authenticate()
    Successfully authenticated with Google Earth Engine!
    
    >>> geeadvance.authenticate(auth_mode='colab')
    Authenticated for Google Colab environment!
    """
    try:
        if auth_mode == "colab":
            # Google Colab authentication
            ee.Authenticate()
            print("✓ Authenticated for Google Colab environment!")
            
        elif auth_mode == "gcloud":
            # Use gcloud credentials
            ee.Authenticate(auth_mode='gcloud')
            print("✓ Authenticated using gcloud credentials!")
            
        elif auth_mode == "service_account":
            # Service account authentication
            # Users should set EE_SERVICE_ACCOUNT and EE_PRIVATE_KEY_FILE
            service_account = os.environ.get('EE_SERVICE_ACCOUNT')
            key_file = os.environ.get('EE_PRIVATE_KEY_FILE')
            
            if not service_account or not key_file:
                raise ValueError(
                    "For service account authentication, set environment variables:\n"
                    "EE_SERVICE_ACCOUNT and EE_PRIVATE_KEY_FILE"
                )
            
            credentials = ee.ServiceAccountCredentials(service_account, key_file)
            ee.Initialize(credentials)
            print("✓ Authenticated using service account!")
            
        else:
            # Default notebook/local authentication
            ee.Authenticate()
            print("✓ Successfully authenticated with Google Earth Engine!")
            
    except Exception as e:
        print(f"✗ Authentication failed: {str(e)}", file=sys.stderr)
        print("\nTroubleshooting tips:", file=sys.stderr)
        print("1. Make sure you have a Google account", file=sys.stderr)
        print("2. Visit https://earthengine.google.com/ to sign up", file=sys.stderr)
        print("3. Run 'earthengine authenticate' in terminal", file=sys.stderr)
        raise


def initialize(project: Optional[str] = None, opt_url: Optional[str] = None) -> None:
    """
    Initialize Google Earth Engine.
    
    This must be called after authentication and before using any GEE functions.
    
    Parameters
    ----------
    project : str, optional
        GEE project ID. If not provided, uses default project.
    opt_url : str, optional
        Optional URL for GEE API endpoint.
    
    Examples
    --------
    >>> import geeadvance
    >>> geeadvance.initialize()
    ✓ Google Earth Engine initialized successfully!
    
    >>> geeadvance.initialize(project='my-gee-project')
    ✓ Google Earth Engine initialized with project: my-gee-project
    """
    try:
        if project:
            ee.Initialize(project=project, opt_url=opt_url)
            print(f"✓ Google Earth Engine initialized with project: {project}")
        else:
            ee.Initialize(opt_url=opt_url)
            print("✓ Google Earth Engine initialized successfully!")
            
    except Exception as e:
        print(f"✗ Initialization failed: {str(e)}", file=sys.stderr)
        print("\nMake sure you have authenticated first using geeadvance.authenticate()", file=sys.stderr)
        raise


def is_authenticated() -> bool:
    """
    Check if Google Earth Engine is authenticated and initialized.
    
    Returns
    -------
    bool
        True if authenticated and initialized, False otherwise.
    
    Examples
    --------
    >>> import geeadvance
    >>> geeadvance.is_authenticated()
    False
    >>> geeadvance.authenticate()
    >>> geeadvance.initialize()
    >>> geeadvance.is_authenticated()
    True
    """
    try:
        # Try to access a simple GEE object
        ee.Number(1).getInfo()
        return True
    except Exception:
        return False


def get_auth_status() -> dict:
    """
    Get detailed authentication status information.
    
    Returns
    -------
    dict
        Dictionary containing authentication status details.
    
    Examples
    --------
    >>> import geeadvance
    >>> status = geeadvance.get_auth_status()
    >>> print(status)
    {'authenticated': True, 'project': 'my-project', 'user': 'user@example.com'}
    """
    status = {
        'authenticated': False,
        'initialized': False,
        'project': None,
        'error': None
    }
    
    try:
        # Check if initialized
        ee.Number(1).getInfo()
        status['authenticated'] = True
        status['initialized'] = True
        
        # Try to get project info
        try:
            # This is a workaround as ee doesn't expose project directly
            status['project'] = 'Connected'
        except:
            pass
            
    except Exception as e:
        status['error'] = str(e)
    
    return status


# Convenience function for quick setup
def quick_setup(project: Optional[str] = None) -> None:
    """
    Quick setup: authenticate and initialize using standard Earth Engine methods.
    
    Parameters
    ----------
    project : str, optional
        GEE project ID. Required if you have multiple projects or a specific billing project.
    
    Examples
    --------
    >>> import geeadvance
    >>> geeadvance.quick_setup(project='your-project-id')
    ✓ Successfully authenticated with Google Earth Engine!
    ✓ Google Earth Engine initialized with project: your-project-id
    """
    if not is_authenticated():
        # Standard GEE calls
        ee.Authenticate()
        ee.Initialize(project=project)
    else:
        print("✓ Already authenticated and initialized!")
