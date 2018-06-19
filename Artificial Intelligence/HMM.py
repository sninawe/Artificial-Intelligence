class Solver:


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling


    Initial_Prob=[]  #Initial_State_Probability
    Trans_Prob=[]  #Transition_Probability
    Emi_Prob=[]  #Emission_Probability


    count=0
    def posterior_prob(self, sentence, tag):
        post_prob=0
        for i in range(len(sentence)):
            index="%s|%s"%(sentence[i],tag[i])
            if index not in Solver.Trans_Emi[0]:
                Solver.Trans_Emi[0][index] = - sys.maxint

        post_prob = post_prob + math.log(Solver.Initial_Prob[tag[0]]) + sum([math.log(Solver.Trans_Emi[0]["START|START"%(sentence[x],tag[x])]) for x in range(len(sentence))])

        post_prob = post_prob + sum([math.log(Solver.Trans_Prob[0]["LAST|LAST" % (tag[x],tag[x-1])]) for x in range(1,len(tag))])

        return post_prob

#Calculate Initial Probability P(S1)
def Initial_State_Probability(self,data):
    init_prob = {}
    line_count = 0

    for i in data:
        current = "START" % (i[1][0])
        if current in init_prob:
            init_prob[current] = init_prob[current] + 1
        else:
            init_prob[current] = 1
        line_count += 1

    for i in init_prob:
        init_prob[i]=init_prob[i]/float(Sentence_count)
    return init_prob

#Calculate Transition Probability P(Sn+1|Sn)
def Transition_Probability(self,data):
    Posterior={}
    Tran_prob={}
    for i in data:
        for j in range(len(i[1])-1):
            if len(i[1]) == 1:
                continue

        current = "START" % (i[1][j+1])

        if current in Posterior:
            Posterior[current] = Posterior[current] + 1
        else:
            Posterior[current] = 1

    for i in data:
        for j in range(len(i[1])-1):
            next = "LAST|LAST" % (i[1][j+1],i[1][j])
            if next in Tran_prob:
                Tran_prob[next] = (Tran_prob[next]+1)/float(Posterior[i[1][j+1]])
            else:
                Tran_prob[next] = 1/float(Posterior[i[1][j+1]])

    return [Tran_prob,Posterior]

#Calculate Emission Probability P(W|S)
def Emission_Probability(self,data):
    Word_Count={}
    Emission_Prob={}
    for i in data:
        for j in range(len(i[1])):
            current="START" % (i[0][j])
            if current in Word_Count:
                Word_Count[current] = Word_Count[current] + 1
            else:
                Word_Count[current] = 1

    for i in data:
        for j in range(len(i[1])):
            next="LAST|LAST" % (i[0][j],i[1][j])
        if next in Emission_Prob:
            Emission_Prob[next] = (Emission_Prob[next]+1)/float(Word_Count[i[0][j]])
        else:
            Emission_Prob[next] = 1/float(Word_Count[i[0][j]])

    return [Emission_Prob,Word_Count]


def train(self, data):
    Solver.Initial_Prob=self.Initial_State_Probability(data)
    Solver.Trans_Prob=self.Transition_Probability(data)
    Solver.Emi_Prob=self.Emission_Probability(data)

# Functions for each algorithm.
#
def Simplified(self, sentence):
     POS_Pridictions_1=[]
     Word_Probability=[]
     Types=['adv','noun','adp','prt','det','num','x','pron','verb','.','conj','adj']


     for i in sentence:
         maximum=0.01e-3
         temp_POS=''
         for j in Types:
                 if i not in Solver.Traind_GAW[1]:
                     Solver.Traind_GAW[0]["%s|%s" % (i,'x')]=0.1e-6
                     temp_POS='x'
                 temp="%s|%s" % (i,j)
                 if temp in Solver.Traind_GAW[0]:
                     if Solver.Traind_GAW[0][temp]>maximum:
                         maximum=Solver.Traind_GAW[0][temp]
                     temp_POS=j
         if i==0:
                 Word_Probability.append(maximum*Solver.Traind_IWP[temp_POS])
         else:
             Word_Probability.append(maximum)
         POS_Pridictions_1.append(temp_POS)


     return [ [POS_Pridictions_1], [Word_Probability] ]



def hmm(self, sentence):
     POS_Pridictions_2=[]
     v={}
     Types=['adv','noun','adp','prt','det','num','x','pron','verb','.','conj','adj']
     for i in Types:
             v[i]=[1 for j in range(len(sentence))]


     #Smoothening
     for i in Types:
             for j in Types:
                 temp="%s|%s" % (i,j)
             if temp not in Solver.Traind_GAP[0]:
                 Solver.Traind_GAP[0][temp]=0.01e-6


     for i in range(len(sentence)):
            if i==0:
                for j in Types:
                    index="%s|%s"%(sentence[i],j)
                if index in Solver.Traind_GAW[0]:
                        v[j][i]=((Solver.Traind_IWP[j])*(Solver.Traind_GAW[0][index]))
                else:
                    Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]=0.1e-6
                    v[j][i]=((Solver.Traind_IWP[j])*(Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]))
        else:
            for j in Types:
                index="%s|%s"%(sentence[i],j)
                if index in Solver.Traind_GAW[0]:
                        v[j][i]=max([v[x][i-1]*Solver.Traind_GAP[0]["%s|%s"%(j,x)] for x in Types])*Solver.Traind_GAW[0][index]
                else:
                    Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]=0.1e-6
                    v[j][i]=max([v[x][i-1]*Solver.Traind_GAP[0]["%s|%s"%(j,x)] for x in Types])*Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]




     for i in range(len(sentence)):
        temp=[[v[x][i],x] for x in Types]
        maximum=max([v[x][i] for x in Types])
        for j in temp:
                if j[0]==maximum:
                    POS_Pridictions_2.append(j[1])


     return [[POS_Pridictions_2[0:len(sentence)]],[]]






def complex(self, sentence):
    POS_Pridictions_3=[]
    Word_Probability=[]
    t={}


    Types=['adv','noun','adp','prt','det','num','x','pron','verb','.','conj','adj']
    for i in Types:
            t[i]=[1 for j in range(len(sentence))]


    for i in range(len(sentence)):
            if i==0:
                for j in Types:
                    index="%s|%s" % (sentence[i],j)
                if index in Solver.Traind_GAW[0]:
                        t[j][i]=Solver.Traind_IWP[j]*Solver.Traind_GAW[0][index]
                else:
                    Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]=0.1e-6
                    t[j][i]=Solver.Traind_IWP[j]*Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]
            elif i==1:
                for j in Types:
                    index="%s|%s" % (sentence[i],j)
                if index in Solver.Traind_GAW[0]:
                        t[j][i]=sum([Solver.Traind_GAP[0]["%s|%s" % (j,x)]*t[x][i-1] for x in Types])*Solver.Traind_GAW[0][index]
                else:
                    Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]=0.1e-6
                    t[j][i]=sum([Solver.Traind_GAP[0]["%s|%s" % (j,x)]*t[x][i-1] for x in Types])*Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]
            else:
                 for j in Types:
                    index="%s|%s" % (sentence[i],j)
                 if index in Solver.Traind_GAW[0]:
                        t[j][i]=sum([ Solver.Traind_GAP[0]["%s|%s" % (j,Types[x])]*t[Types[x]][i-1]+[Solver.Traind_GAP[0]["%s|%s" % (j,Types[y])]*t[Types[y]][i-2] for y in range(len(Types))][x] for x in range(len(Types))])*Solver.Traind_GAW[0][index]
                 else:
                    Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]=0.1e-6
                    t[j][i]=sum([ Solver.Traind_GAP[0]["%s|%s" % (j,Types[x])]*t[Types[x]][i-1]+[Solver.Traind_GAP[0]["%s|%s" % (j,Types[y])]*t[Types[y]][i-2] for y in range(len(Types))][x] for x in range(len(Types))])*Solver.Traind_GAW[0]["%s|%s" % (sentence[i],'x')]


    for i in range(len(sentence)):
        temp=[[t[x][i],x] for x in Types]
        maximum=max([t[x][i] for x in Types])
        for j in temp:
                if j[0]==maximum:
                    Word_Probability.append(j[0])
                POS_Pridictions_3.append(j[1])


    return [ [POS_Pridictions_3[0:len(sentence)] ], [Word_Probability[0:len(sentence)]] ]




# This solve() method is called by label.py, so you should keep the interface the
#  same, but you can change the code itself.
# It's supposed to return a list with two elements:
#
#  - The first element is a list of part-of-speech labelings of the sentence.
#    Each of these is a list, one part of speech per word of the sentence.
#
#  - The second element is a list of probabilities, one per word. This is
#    only needed for simplified() and complex() and is the marginal probability for each word.
#
def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"
