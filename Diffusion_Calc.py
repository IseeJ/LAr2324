import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

file_path = '/home/wjaidee/Qpix/Programs/PyBoltz/results/'+str(sys.argv[1])
df = pd.read_csv(file_path, header=None, names=['E', 'P', 'Vdrift', 'Vdrift_err', 'DT', 'DT_err'])
df = df.sort_values(by='P')
df['µ'] = (df['Vdrift']*(1e5))/df['E'] #Vdrift/E                                                                    
df['µ_err'] = df['Vdrift_err']/df['E']
df['DT/µ'] = df['DT']/df['µ']
df['DT/µ_err'] = df['DT/µ']*np.sqrt((df['DT_err']/df['DT'])**2+(df['µ_err']/df['µ'])**2)
df['Diffusion'] = (np.sqrt((2*df['DT/µ']/df['E'])))*10
df['Diffusion_err'] = 10*df['Diffusion']*1/2*(df['DT/µ_err']/df['DT/µ'])


print(df)

"""                                                                                                                 
if str(sys.argv[2]) == 'err':                                                                                       
    y_err = df['DT/µ_err']                                                                                          
else:                                                                                                               
    y_err = 0                                                                                                       
                                                                                                                    
plt.figure(figsize=(12, 5))                                                                                         
plt.subplot(1, 2, 1)                                                                                                
plt.errorbar(df['P'], df['DT/µ'], yerr=y_err, fmt='o', color='b', capsize=5)                                        
plt.xlabel('P')                                                                                                     
plt.ylabel('DT/µ')                                                                                                  
plt.title('DT/µ against P')                                                                                         
                                                                                                                    
                                                                                                                    
plt.subplot(1, 2, 2)                                                                                                
plt.errorbar(df['P'], df['Diffusion'], yerr=y_err, fmt='o', color='r', capsize=5)                                   
plt.xlabel('P')                                                                                                     
plt.ylabel('Diffusion')                                                                                             
plt.title('Diffusion against P')                                                                                    
                                                                                                                    
plt.tight_layout()                                                                                                  
plt.show()                                                                                                          
"""

new_file_path = '/home/wjaidee/Qpix/Programs/PyBoltz/Calc/'+'calc'+str(sys.argv[1])[3:-4]+'.txt'
df.to_csv(new_file_path, sep=',', index=False)
print(f"Modified DataFrame saved to {new_file_path}")
