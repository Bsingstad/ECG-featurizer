import numpy as np

class OLS_clf:

    def __init__(self,polynomial):
        #elf.X_matrix = None
        self.predict_ = None
        self.beta = None
        self.poly = polynomial

    def fit(self, x,y,z):
        x = x.ravel()
        y = y.ravel()
        z = z.ravel()
        X = 0
        X_temp = 0
        if len(x) != len(y):
            print("x and y needs to have the same length!")
            
        X = np.ones(len(x)).reshape(len(x),1)
        for i in range(self.poly):
            if i == 0:
                X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1)))
                X = np.concatenate((X,X_temp),axis=1)
            else:
                X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1),((x**i) * (y**i)).reshape(len(y),1) ))
                X = np.concatenate((X,X_temp),axis=1)
        
        self.beta=np.linalg.inv(X.T.dot(X)).dot(X.T).dot(z)
        return self.beta

    def predict(self, x,y):
        x = x.ravel()
        y = y.ravel()
        self.predict_ = self.beta[0]

        for i in range(self.poly):
            if i == 0:
                self.predict_ = self.predict_ + self.beta[1] * x + self.beta[2] * y
            else:
                self.predict_ = self.predict_ + self.beta[i*3] *(x**(i+1)) + self.beta[(i*3)+1]*(y**(i+1)) + self.beta[(i*3)+2]*((x**i) * (y**i))

        return self.predict_



class Ridge_clf:

    def __init__(self,polynomial,lmbda):
        #elf.X_matrix = None
        self.lambda_ = lmbda
        self.predict_ = None
        self.beta = None
        self.poly = polynomial

    def fit(self, x,y,z):
        x = x.ravel()
        y = y.ravel()
        z = z.ravel()
        X = 0
        X_temp = 0
        if len(x) != len(y):
            print("x and y needs to have the same length!")
            
        X = np.ones(len(x)).reshape(len(x),1)
        for i in range(self.poly):
            if i == 0:
                X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1)))
                X = np.concatenate((X,X_temp),axis=1)
            else:
                X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1),((x**i) * (y**i)).reshape(len(y),1) ))
                X = np.concatenate((X,X_temp),axis=1)
        
        #self.beta=np.linalg.inv(X.T.dot(X)).dot(X.T).dot(z)
        self.beta=np.linalg.inv(X.T.dot(X)+self.lambda_ * np.identity(X.shape[1])).dot(X.T).dot(z)
        return self.beta

    def predict(self, x,y):
        x = x.ravel()
        y = y.ravel()
        self.predict_ = self.beta[0]

        for i in range(self.poly):
            if i == 0:
                self.predict_ = self.predict_ + self.beta[1] * x + self.beta[2] * y
            else:
                self.predict_ = self.predict_ + self.beta[i*3] *(x**(i+1)) + self.beta[(i*3)+1]*(y**(i+1)) + self.beta[(i*3)+2]*((x**i) * (y**i))

        return self.predict_


class sdg_clf:

    def __init__(self,polynomial,epochs,iterations,m=1,method="OLS",lambda_=0.01):
        self.X_matrix = None
        self.predict_ = None
        self.theta = None
        self.m = m
        self.poly = polynomial
        self.epochs = epochs
        self.iterations = iterations
        self.method = method
        self.lambda_ = lambda_

    def fit(self, x,y,z):

        def _learning_schedule(t):
            t0, t1 = 5, 50
            return t0/(t+t1)

        def _make_design_matrix(x,y):
            X = np.ones(len(x)).reshape(len(x),1)
            for i in range(self.poly):
                if i == 0:
                    X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1)))
                    X = np.concatenate((X,X_temp),axis=1)
                else:
                    X_temp = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1),((x**i) * (y**i)).reshape(len(y),1) ))
                    X = np.concatenate((X,X_temp),axis=1)
            return X
        
        def _SDG_OLS(z):
            self.theta=np.random.randn(self.X_matrix.shape[1],1)
            for epoch in range(self.epochs):
                for i in range(self.iterations):
                    random_index = np.random.randint(len(z.ravel()))
                    xi = self.X_matrix[random_index:random_index+1]
                    zi = z.ravel()[random_index:random_index+1]
                    gradients = (2.0/self.m )* xi.T @ ((xi @ self.theta)-zi)
                    eta = _learning_schedule(epoch*self.iterations+i)
                    self.theta = self.theta - eta*gradients
            return self.theta

        def _SDG_Ridge(z):
            self.theta=np.random.randn(self.X_matrix.shape[1],1)
            for epoch in range(self.epochs):
                for i in range(self.iterations):
                    random_index = np.random.randint(len(z.ravel()))
                    xi = self.X_matrix[random_index:random_index+1]
                    zi = z.ravel()[random_index:random_index+1]
                    gradients = (2.0/self.m ) * xi.T @ ((xi @ self.theta)-zi)+2*self.lambda_*self.theta
                    eta = _learning_schedule(epoch*self.iterations+i)
                    self.theta = self.theta - eta*gradients
            return self.theta



        x = x.ravel()
        y = y.ravel()
        z = z.ravel()

        if len(x) != len(y):
            print("x and y needs to have the same length!")
        
        self.X_matrix = _make_design_matrix(x,y)
        
        if self.method == "OLS":
            _SDG_OLS(z)
        elif self.method == "Ridge":
            _SDG_Ridge(z)

        return self.theta

    def predict(self, x,y):
        x = x.ravel()
        y = y.ravel()
        if len(x) != len(y):
            print("x and y needs to have the same length!")

        X_pred = np.ones(len(x)).reshape(len(x),1)
        for i in range(self.poly):
            if i == 0:
                X_temp_pred = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1)))
                X_pred = np.concatenate((X_pred,X_temp_pred),axis=1)
            else:
                X_temp_pred = np.hstack(((x**(i+1)).reshape(len(x),1) , (y**(i+1)).reshape(len(y),1),((x**i) * (y**i)).reshape(len(y),1) ))
                X_pred = np.concatenate((X_pred,X_temp_pred),axis=1)

        self.predict_ = X_pred.dot(self.theta)
        return self.predict_  