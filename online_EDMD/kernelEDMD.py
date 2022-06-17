import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.spatial import distance
from d3s import observables, domain, systems


def gramian(X, sigma):
    return np.exp(-distance.squareform(distance.pdist(X.T, 'sqeuclidean'))/(2*sigma**2))
def gramian2(X, Y, sigma=np.sqrt(2)):
    return np.exp(-distance.cdist(X.T, Y.T, 'sqeuclidean')/(2*sigma**2))

if __name__=="__main__":
    #generate data
    bounds = np.array([[-20, 20], [-20, 20], [-20, 20]])
    boxes = np.array([20, 20, 20])
    Omega = domain.discretization(bounds, boxes)
    sigma = np.sqrt(2)
    f = systems.Hydrogen(1e-3, 10000)
    np.random.seed(seed=233423)
    X = Omega.rand(50)
    Y = f(X)
    
    #compute gramian, G_hat, A_hat
    G = gramian(X, sigma)
    A = gramian2(X, Y, sigma)
    #eigenvalue decomposition, G_hat = V*S^2*V(inv)
    d, Q = np.linalg.eig(G)
    S_2 = np.diag(d)
    S = sp.linalg.sqrtm(S_2)
    #compute K_hat, Koopman matrix
    S_pinv = np.linalg.pinv(S)
    K = S_pinv @ Q.T @ A @ Q @ S_pinv
    S_r = S_2 @ S_pinv
    d, V = np.linalg.eig(K)
    eigenfunctions = Q @ S_r @ V
    #plot eigenfunctions
    # parameters of the grid
    W = eigenfunctions
    Ngrid = 50
    xmin = -20 
    xmax = 20

    xvec = np.linspace(xmin,xmax,Ngrid)
    n=2
    fig, (ax1,ax2) = plt.subplots(2,1, sharex=True)
    ax1.plot(xvec,np.real(W[:,n]))
    ax1.set(title='Realteil Eigenfunktion %d'%(n),xlabel='x')
    ax2.plot(xvec,np.power(np.abs(W[:,n]),2))
    ax2.set(title='AbsQuadrat Eigenfunktion %d'%(n),xlabel='x')
    fig.tight_layout()
    fig.show()