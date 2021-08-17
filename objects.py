class Profile:
    def __init__(self, orders):
        self.orders = orders
        self.length = len(orders)
    
    def __str__(self):
        return ''.join(self.orders)


R = Profile(['abc', 'bca'])
for l in R.orders:
    print(l)