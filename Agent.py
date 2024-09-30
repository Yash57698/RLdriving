import tensorflow as tf
import numpy as np
import random

tf.config.run_functions_eagerly(False)
class Agent:
    #Hyperparameters
    neurons = 32
    discount = 0
    update_epochs = 256
    updatesbeforetrainupdate = 10 
    actionsB4update = 32
    batchsize = 256
    maxbuffer = 2048

    def __init__(self,car,load = False):
        self.car = car
        self.state_size = 8 #relative position of target, velocity of car,heading of car,carpos
        self.action_size = 7 #up, down, upleft, upright,dwnleft, dwnright,nothing
        self.model = self.build_model()
        self.trainmodel = self.build_model("Train")
        self.count = 0 
        self.episode = 0
        self.actioncount =0
        self.data = -1
        self.load = load
        if self.load:
            self.model.load_weights("model.weights.h5")
            self.trainmodel.set_weights(self.model.get_weights())
        self.lastloss = 0

    def build_model(self,name = 'Agent'):
        model = tf.keras.models.Sequential(name=name)
        model.add(tf.keras.layers.Input(shape=(self.state_size,)))
        model.add(tf.keras.layers.Dense(8, activation='relu'))
        # model.add(tf.keras.layers.LSTM(24))
        model.add(tf.keras.layers.Dense(4, activation='relu'))
        # model.add(tf.keras.layers.Dense(64, activation='relu'))
        # model.add(tf.keras.layers.Dense(32, activation='relu'))
        # model.add(tf.keras.layers.Dense(16, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(0.01))
        model.summary()
        return model
    
    def getaction(self, state):
        return self.model.predict(state,verbose=0)
    
    def gettrainaction(self, state):
        return self.trainmodel.predict(state,verbose=0)
    
    def storeexp(self, state, action, reward, next_state):
        self.actioncount+=1
        if self.data == -1:
            self.data = 1
            self.statebuffer = state
            self.actionbuffer = action
            self.rewardbuffer = np.array([reward])
            self.nextstatebuffer = next_state        
        else:
            if self.statebuffer.shape[0] >= self.maxbuffer:
                p = random.randint(0,self.maxbuffer-1)
                self.statebuffer[p] = state
                self.actionbuffer[p] = action
                self.rewardbuffer[p] = reward
                self.nextstatebuffer[p] = next_state
            else:
                self.statebuffer = np.vstack((self.statebuffer,state))
                self.actionbuffer = np.vstack((self.actionbuffer,action))
                self.rewardbuffer = np.vstack((self.rewardbuffer,np.array([reward])))
                self.nextstatebuffer = np.vstack((self.nextstatebuffer,next_state))

        if(self.actioncount%self.actionsB4update == 0):
            self.update()
        self.actioncount = self.actioncount%self.actionsB4update
        

    def update(self):
        if(self.statebuffer.shape[0]>self.batchsize):
            d = np.random.randint(0,self.statebuffer.shape[0],self.batchsize)
            if(self.count%self.updatesbeforetrainupdate == 0):
                self.episode+=1
                print("Updating train model after episode:",self.episode)
                self.trainmodel.set_weights(self.model.get_weights())
                self.model.save_weights("model.weights.h5")

            trainaction = self.gettrainaction(self.nextstatebuffer[d])
            trainaction = trainaction[np.arange(trainaction.shape[0]),np.argmax(self.actionbuffer[d],axis=1)].reshape(-1,1)
            target = self.rewardbuffer[d] + self.discount * trainaction
            
            t = np.array(self.actionbuffer[d])
            t[np.arange(t.shape[0]),np.argmax(self.actionbuffer[d],axis=1)] = target.reshape((-1))
            
            
            
            # print("t")
            # print(t[0])

            print("Training model: episode ",self.episode," iteration: ",self.count,end = ' ')
            
            callbacks = [tf.keras.callbacks.EarlyStopping(min_delta=0.01, patience=64,monitor='loss')]
            verb = 0
            if(self.episode>50): verb = 2
            history = self.model.fit(self.statebuffer[d], t, epochs=self.update_epochs,callbacks=callbacks,verbose = 0)
            self.lastloss = history.history['loss'][-1]
            print("Loss:",history.history['loss'][-1],end = '\r')
            if(self.count == self.updatesbeforetrainupdate-1):
                print(" ")
            # print(np.mean(np.power(np.abs(self.trainmodel.predict(self.statebuffer[d]) - t),2)))
            self.count+=1
            self.count = self.count%self.updatesbeforetrainupdate

    def decodeaction(action):
        action = np.argmax(action[0])
        wpressed = False
        apressed = False
        spressed = False
        dpressed = False
        if action == 0:
            wpressed = True
        elif action == 1:
            spressed = True
        elif action == 2:
            wpressed = True
            apressed = True
        elif action == 3:
            wpressed = True
            dpressed = True
        elif action == 4:
            spressed = True
            apressed = True
        elif action == 5:
            spressed = True
            dpressed = True
        return wpressed,spressed,dpressed,apressed

# target
# [[-0.59688819 -0.57093825 -0.63637327 -0.46150278 -0.7688636  -0.65296948]
 
#  trainaction
# [[ 0.02553365  0.05436693 -0.01833865  0.1759619  -0.16555013 -0.03677889]
#  action
# [[ 0.02519402  0.05056667 -0.01937537  0.17501199 -0.16376476 -0.03711161]

# reward
# [[-0.61986848]
 

 
#  t
# [[ 0.02519402  0.05056667 -0.01937537  0.17501199 -0.16376476 -0.03711161]