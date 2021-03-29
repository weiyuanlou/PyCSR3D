import numpy as np
import scipy.special as ss

from scipy.optimize import root_scalar

from csr3d.core import psi_calc, psi_x, psi_x0, psi_y0, psi_y, psi_s


def symmetric_vec(n, d):
    """
    Returns a symmetric vector about 0 of length 2*n with spacing d.
    The center = 0 is at [n-1]
    """
    return np.arange(-n+1,n+1,1)*d

def green_mesh(density_shape, deltas, rho=None, gamma=None, offset=(0,0,0), component='s'):
    """
    Computes Green funcion meshes for psi_s and psi_x simultaneously.
    These meshes are in real space (not scaled space).
    
    Parameters
    ----------
    shape : tuple(int, int, int)
        Shape of the charge mesh
    
    deltas : tuple(float, float, float)
        mesh spacing corresonding to dx, dy, dz
        
    gamma : float
        relativistic gamma
    
    
    
    Returns:
    tuple of:
        psi_s_grid : np.array
            Double-sized array for the psi_s Green function
        
        psi_x_grid : 
            Double-sized array for the psi_x Green function
        
        zvec2 : array-like
            Coordinate vector in z (real space) [m]

        xvec2 : array-like
            Coordinate vector in x (real space) [m]
    
    """
    
    # handle negative rho
    rho_sign = np.sign(rho)
    rho = abs(rho)
    
    nx, ny, nz = tuple(density_shape)
    dx, dy, dz = tuple(deltas) # Convenience
    
    # Change to internal coordinates
    dx = dx/rho
    dy = dy/rho
    dz = dz/(2*rho)
    
    # Make an offset grid
    vecs = [symmetric_vec(n, delta) for n, delta, o in zip(density_shape, [dx,dy,dz], offset)] 
    vecs[0] = rho_sign*vecs[0] # Flip sign of x
    meshes = np.meshgrid(*vecs, indexing='ij')

    
    
    if component == 'x':
     #   green = psi_x(*meshes, gamma)
        green = rho_sign*psi_x0(*meshes, gamma, dx, dy, dz)        
    elif component == 'y':
        green = psi_y0(*meshes, gamma, dx, dy, dz)        
    elif component == 's':
        green = psi_s(*meshes, gamma)
    else:
        raise ValueError(f'Unknown component: {component}')


    
    return green
    
