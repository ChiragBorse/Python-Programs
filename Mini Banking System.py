class BankAccount:

    def __init__(self,name,balance=0):

        self.name=name

        self.balance=balance

    def deposit(self,amount):

        self.balance+=amount

    def withdraw(self,amount):

        if amount<=self.balance:

            self.balance-=amount

        else:

            print("Insufficient Balance")

    def show(self):

        print(self.name,self.balance)

account=BankAccount("Chirag",10000)

account.deposit(5000)

account.withdraw(3000)

account.show()
