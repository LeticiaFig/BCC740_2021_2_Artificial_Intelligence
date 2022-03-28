from cmath import sqrt


class ToilletPaperAgent():

    def __init__(self,env) -> None:
        self.env = env
        self.lats_percepts = env.initial_percepts()
        self.current_percepts = env.initial_percepts()
        self.age = 0

        self.usage = self.current_percepts['tpnumber']
        self.usage_average = self.current_percepts['tpnumber']
        self.usage_std = 0
        self.sum_to_calculate_usage_std = 0
        
        self.price_average = 0
        self.sum_to_calculate_price_std = 0
        self.spendings = 0 
        self.price_std = 0
        self.total_spending = 0
        
        self.to_buy = 0


    def act(self):         
        self.age += 1
        self.last_percepts = self.current_percepts        

        self.getQuantityToBuy()
        self.getSpendings()

        action = {'to_buy':self.to_buy}
        
        self.current_percepts = self.env.change_state(action)
        
        self.getUsage()
        self.getUsageAverage()
        self.getPriceAverage()        

    
    def getQuantityToBuy(self): #Calcular aqui uma porcentagem em cima do valor baseado na média?? mesma porcentagem em relação a média de uso é a porcentagem em relação ao preço 
        self.getUsageStd()
        self.getPriceStd()
        self.to_buy = (max(self.usage_average + self.usage_std*4 - self.current_percepts['tpnumber'],0))
        if(self.price_std != 0): 
            if(self.price_average - self.current_percepts['price'] >= 0) :
                self.to_buy -= 100*self.to_buy*(self.price_average - self.current_percepts['price'])/(self.price_std)
                self.to_buy = max(self.to_buy, 0)
            else:
                self.to_buy -= self.to_buy*(self.price_average - self.current_percepts['price'])/(10*self.price_std)
        

    def getUsageStd(self):
        self.sum_to_calculate_usage_std = self.sum_to_calculate_usage_std + (self.usage - self.usage_average)**2 
        self.usage_std = pow(self.sum_to_calculate_usage_std/self.age, 1/2)
        

    def getSpendings(self):
        self.spendings = self.to_buy * self.current_percepts['price']
        self.total_spending = self.total_spending + self.spendings
        if(self.age == 1000) : print(self.total_spending)


    def getUsage(self):
        self.usage = self.last_percepts['tpnumber'] + self.to_buy - self.current_percepts['tpnumber']

    
    def getUsageAverage(self):
        self.usage_average = (self.usage_average * (self.age - 1) + self.usage)/self.age


    def getPriceAverage(self):
        self.price_average = (self.price_average * (self.age - 1) + self.current_percepts['price'])/self.age

    
    def getPriceStd(self):
        self.sum_to_calculate_price_std = self.sum_to_calculate_price_std + (self.current_percepts['price'] - self.price_average)**2 
        self.price_std = pow(self.sum_to_calculate_price_std/self.age, 1/2)
    