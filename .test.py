
def func(var1,**kwargs):
    print(var1)
    print(kwargs)

my_dict =  {'test': 2}
my_dict2 = {'test2':3}

my_dict2.update(my_dict)
print(my_dict2)
func(1,**my_dict2)
