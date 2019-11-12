import numpy as np
def mtt(image):                    
 ans=image.sum(axis=(0,1)).argmax()      # using sum() and argmax() get the desired index
 return(ans)

def sd(image):
 std=np.std(image, axis=2)
 ind = np.unravel_index(np.argmax(std, axis=None), std.shape)   # using argmax() function to get the (x,y) index
 return(ind)

def threshold(image, th):
 condlist = [image>th]
 choicelist = [image]
 x= np.select(condlist,choicelist)    # using select function to place condtion of required threshold
 print(x)
 print()
 sum1=x.sum() 
 return(sum1)   

def main() :
 image = np.random.randint(0, 10, size=(2,2,5)) 
 print("My 3D array is:\n",image)
 print()
 print("Total intensity corresponding to the third dimension:",mtt(image))
 print()
 print("(x,y) indices of a point that has the largest variability:",sd(image))
 print()
 print("sum of intensities over all measurement:", threshold(image,5))

if __name__ == '__main__':
    main()
 