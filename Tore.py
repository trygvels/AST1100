from scitools.std import*
import urllib 
from urllib2 import urlopen

t = 'spectrum_day'+raw_input('File number-->')+'.txt'
url = 'http://folk.uio.no/frodekh/AST1100/lecture6/'+t
urllib.urlretrieve(url,filename=t)
infile = urlopen(url)
number_of_observations = sum(array([1 for _ in infile]))
infile = urlopen(url)

observation = zeros((number_of_observations, 2))

i = 0
for line in infile:
	wavelength, flux_relative = line.split()
	observation[i][0] = float(wavelength)
	observation[i][1] = float(flux_relative)
	i += 1

plt.plot(observation[:,0], observation[:,1])
plt.xlim([656.3,656.5])

Fmax = 1.
Fmin_approx=float(raw_input('Flux at the center of spectrum, made from by-eye estimate --> '))
sigma_approx=float(raw_input('Width of spectrum, made from by-eye estimate --> '))
lambdacenter_approx=float(raw_input('Central wavelength in spectral line, made from by-eye estimate --> '))

Fmin_candidates = linspace(0.90*Fmin_approx, 1.1*Fmin_approx, 40)
sigma_candidates = linspace(0.90*sigma_approx, 1.1*sigma_approx, 40)
lambdacenter_candidates = linspace(lambdacenter_approx-0.1, lambdacenter_approx+0.1, 40)

#print Fmin_candidates,sigma_candidates,lambdacenter_candidates

delta=zeros((40**3, 4))
i=0
for Fmin in Fmin_candidates:
	for sigma in sigma_candidates:
		for lambdacenter in lambdacenter_candidates:
			F_model = Fmax+(Fmin-Fmax)*e**(-((observation[:,0]-lambdacenter)**2)/(2*sigma**2))
			s = sum((observation[:,1]- F_model)**2) # testing what gives the most accurate using least square method(LSM)
			delta[i] = [s, Fmin, sigma, lambdacenter]
			i+=1


minimum_delta=argmin(delta[:,0]) #finding best values which we found using LSM

Fmin = delta[minimum_delta][1]
sigma=delta[minimum_delta][2]
lambdacenter=delta[minimum_delta][3]

F_mod = Fmax+(Fmin-Fmax)*e**(-((observation[:,0]-lambdacenter)**2)/(2*sigma**2))
print Fmax,Fmin,lambdacenter,sigma


plt.plot(observation[:,0], observation[:,1],observation[:,0], F_mod)
