k = 10
img = 153
klusters = dict(zip(range(k),[i*(255//k) for i in range(k)]))
print(klusters.values())
print([0]*5)
a = [abs(img-value) for value in klusters.values()]
