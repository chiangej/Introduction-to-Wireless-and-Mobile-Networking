# Description
Use the file to plot figures of 
* path loss only radio propagation, Two-ray-ground model 
* path loss and shadowing (without fading), log-normal shadowing to
model
## Requirement
Python 3.8.10

## Main Function 
```python
    def received_power_two_ray( d ):
    return Pt*Gr*Gt*(h_device*h_base) **2/ (d ** 4)
    
    def apply_shadowing(Pr, sigma, size):
    shadowing = np.random.normal(0, sigma, size)
    Pr_shadowed = Pr * 10**(shadowing / 10)
    return Pr_shadowed
   ```
## Compile
```bash
  python main.py
```

## Support
* Contact：ESOE b10505005 蔣依倢 

