import numpy as np
import matplotlib.pyplot as plt

try:
    from ipywidgets import interactive, IntSlider, widget, FloatText, FloatSlider, Checkbox, ToggleButtons
    pass
except Exception, e:    
    from IPython.html.widgets import  interactive, IntSlider, widget, FloatText, FloatSlider, Checkbox, ToggleButtons


sigmin = 0.1
sigmax = 2.

sig0 = 0 # conductivity of the air
h = 1.
h_boom = 0. 
h_boom_max = 2. 

zmax = 4. 

z = np.linspace(0.,zmax,1000)


phi_v = lambda z: (4.*z) / (4.*z**2 + 1.)**(3./2.)
phi_h = lambda z: 2 - (4.*z) / (4.*z**2 + 1.)**(1./2.) 

R_v = lambda z: 1./(4.*z**2. + 1.)**(1./2.)
R_h = lambda z: (4.*z**2 + 1.)**(1./2.) - 2.*z

sigma_av = lambda h_boom, h, sig1, sig2: sig0*(1.-R_v(h_boom)) + sig1*(R_v(h_boom) - R_v(h+h_boom)) + sig2*R_v(h+h_boom)
sigma_ah = lambda h_boom, h, sig1, sig2: sig0*(1.-R_h(h_boom)) + sig1*(R_h(h_boom) - R_h(h+h_boom)) + sig2*R_h(h+h_boom) 


def plot_ResponseFct(h_boom,h,sig1,sig2,orientation='vertical'):
    
    sigvec = sig1*np.ones(z.shape)
    sigvec[z > h] = sig2

    if orientation is 'vertical':
        phi = phi_v(z + h_boom)
        sig_a = sigma_av(h_boom,h,sig1,sig2)
        phi_title = '$\phi_V$'
    elif orientation is 'horizontal':
        phi = phi_h(z + h_boom)
        sig_a = sigma_ah(h_boom,h,sig1,sig2)
        phi_title = '$\phi_H$'

    phisig = phi*sigvec
    

    fig, ax = plt.subplots(1,3,figsize=(11,6))

    fs = 13

    ax[0].plot(sigvec,z,'r',linewidth=1.5)
    ax[0].set_xlim([0.,sigmax*1.1])
    ax[0].invert_yaxis()
    ax[0].set_ylabel('z/s',fontsize = fs)
    ax[0].set_title('$\sigma$', fontsize = fs+4, position=[.5, 1.02])
    ax[0].set_xlabel('Conductivity (S/m)', fontsize=fs)
    ax[0].grid(which='both',linewidth=0.6,color=[0.5,0.5,0.5])

    ax[1].plot(phi,z,linewidth=1.5)
    ax[1].set_xlim([0.,2.])
    ax[1].invert_yaxis()
    ax[1].set_title('%s'%(phi_title), fontsize = fs+4, position=[.5, 1.02])
    ax[1].set_xlabel('Response Function', fontsize=fs)
    ax[1].grid(which='both',linewidth=0.6,color=[0.5,0.5,0.5])

    ax[2].plot(phisig,z,color='k',linewidth=1.5)
    ax[2].fill_betweenx(z,phisig,color='k',alpha=0.5)
    ax[2].invert_yaxis()
    ax[2].set_title('$\sigma \cdot$ %s'%(phi_title), fontsize = fs+4, position=[.5, 1.02])
    ax[2].set_xlabel('Weighted Conductivity (S/m)', fontsize=fs)
    ax[2].set_xlim([0.,4.])
    ax[2].grid(which='both',linewidth=0.6,color=[0.5,0.5,0.5])

    props = dict(boxstyle='round', facecolor='grey', alpha=0.3)

    # place a text box in upper left in axes coords
    textstr = '$\sigma_a=%.2f$ S/m'%(sig_a)
    ax[2].text(2.0, 3.75, textstr, fontsize=fs+2,
            verticalalignment='bottom', bbox=props)

    plt.tight_layout()
    plt.show()
    
    return None

def interactive_responseFct():
	app = interactive(plot_ResponseFct,h_boom = FloatSlider(min=h_boom, max = h_boom_max, step = 0.1, value = h_boom),
                  h = FloatSlider(min=0., max=zmax,value=1.0, step = 0.1),
                  sig1 = FloatSlider(min=sigmin,max = sigmax,value=1., step = 0.1),
                  sig2 = FloatSlider(min=sigmin,max = sigmax,value=0.5, step = 0.1),
                  orientation=ToggleButtons(options=['vertical','horizontal']))
	return app

if __name__ == '__main__':
	plot_ResponseFct(1., sigmin, sigmax)