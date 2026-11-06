n=[1,2,3,4,5,6,7,8,9]
def square(i):
    return i*i

new_n=list(map(square,n))
print(new_n)