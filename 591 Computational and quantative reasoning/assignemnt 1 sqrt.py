def main():
  n=int(input("Enter any number"))
  prime(n)
def prime(n):
 c=0;
 for i in range (1,n+1):
  if n%i==0:
   c=c +1;
 if c==2:
   print(" The given number is a prime number")  
 else:
   print(" The given number is not a prime number")

if __name__ == '__main__':
  main()



