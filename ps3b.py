# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

from ps3b_precompiled_38 import *

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb=maxBirthProb
        self.clearProb=clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        p=random.random()
        #random.random trabaja en [0.0, 1.0)
        if p<self.getClearProb():
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        p=random.random()
        if p<(self.maxBirthProb*(1-popDensity)):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException
            



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses=viruses
        self.maxPop=maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        viruses=self.getViruses()
        copy=viruses.copy()
        #Creamos una copia para iterar sobre ella y que no haya saltos en las listas por añadir o eliminar elementos mientras se itera directamente sobre ellas
        for v in copy:
            #Comprobamos si el individuo virus (uno a uno) va a desaparecer del paciente
            if v.doesClear():
                viruses.remove(v)
        #Actualizamos el paciente
        self.__init__(viruses, self.getMaxPop())
        popDensity=self.getTotalPop()/self.getMaxPop()
        viruses=self.getViruses()
        copy=viruses.copy()
        for v in copy:
            #Comprobamos uno a uno si los virus van a tener descendencia y si ocurre, los guardamos en viruses
            try:
                a=v.reproduce(popDensity)
                viruses.append(a)
            except NoChildException:
                continue
        #Actualizamos de nuevo el paciente
        self.__init__(viruses, self.getMaxPop())
        
        return self.getTotalPop()
        
        #También puede hacerse modificando self directamente
        '''
        for v in self.viruses[:]:
            if v.doesClear():
                self.viruses.remove(v)

        self.popDensity = len(self.getViruses()) / self.getMaxPop()

        for vs in self.viruses[:]:
            try:
                self.viruses.append(vs.reproduce(self.popDensity))
            except NoChildException:
                continue

        return self.getTotalPop()
        '''


#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    mean=[]
    population=[]
    for i in range(300):
        #300 time-steps
        #Crear una lista que contenga primero todos los time-steps y dentro los diferentes trials
        #population=[[ts1_trial1, ts1_trial2, ...], [ts2_trial1, ts2_trial2, ...], ...]
        population.append([])
    
    for t in range(numTrials):
        time=[]
        viruses=[]
        #Como los virus se van actualizando, hay que inicializarlos cada vez
        for v in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        #Inicializamos en cada trial el paciente
        p=Patient(viruses, maxPop)
        for i in range(300):
            time.append(i)
            population[i].append(p.update())
    
    for i in range(300):
        #Sacamos la media de los trials en cada time-step
        mean.append(sum(population[i])/numTrials)
    
    pylab.plot(mean, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()


simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)



#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances=resistances
        self.mutProb=mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.getResistances():
            return self.resistances[drug]
        else:
            return False
        '''
        try:
            return self.resistances[drug]
        except KeyError:
            return False
        '''


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        #Creamos una copia que nos servirá para las características de la herencia
        resistances=self.getResistances()
        #Ya que vamos a recorrer el diccionario original entero, podemos crear uno nuevo
        new={}
        for d in activeDrugs:
            if not self.isResistantTo(d):
                #El virus no deja descendencia si no es resistente a alguno de los medicamentos
                #Además, se muere
                raise NoChildException
        #El virus sobrevive y a lo mejor se reproduce
        p1=random.random()
        if p1<(self.maxBirthProb*(1-popDensity)):
            #Si logra reproducirse falta por ver si hereda las características o no
            #Mayor porcentaje de quedarse como está y menor de cambiar(que podrá ser para bien, ganar resistencia, o para mal, perderla)
            #Ver ejemplo más arriba para más información
            for d in resistances.keys():
                p2=random.random()
                if resistances[d]==True and p2<(1-self.getMutProb()):
                    new[d]=True
                elif resistances[d]==True and p2>=(1-self.getMutProb()):
                    new[d]=False
                elif resistances[d]==False and p2<(1-self.getMutProb()):
                    new[d]=False
                elif resistances[d]==False and p2>=(1-self.getMutProb()):
                    new[d]=True
            #Una vez visto los rasgos que hereda o no, se inicializa el hijo con el diccionario que hemos ido modificando
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), new, self.getMutProb())
        else:
            raise NoChildException
        '''
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            newRes = {}
            for k in self.resistances.keys():
                if random.random() <= self.mutProb:
                    newRes[k] = not self.resistances[k]
                else:
                    newRes[k] = self.resistances[k]
            return ResistantVirus(self.maxBirthProb, self.clearProb, newRes, self.mutProb)
        raise NoChildException
        '''
            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.prescription=[]


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        #What happens when a drug is introduced? The drugs we consider do not directly kill virus particles lacking resistance to the drug,
        #but prevent those virus particles from reproducing (much like actual drugs used to treat HIV).
        #Virus particles with resistance to the drug continue to reproduce normally.
        if newDrug not in self.getPrescriptions():
            self.getPrescriptions().append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.prescription


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count=0
        for v in self.getViruses():
            #Comprobamos todos los virus
            i=0
            for d in drugResist:
                #Ese virus tiene que ser resistente a todos los fármacos
                if v.isResistantTo(d):
                    i+=1
                    if i==len(drugResist):
                        count+=1
        return count


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        #Es idéntico al de más arriba, con algunos cambios en los inputs
        #No hace falta actualizar Patient todo el rato
        viruses=self.getViruses()
        copy=viruses.copy()
        for v in copy:
            if v.doesClear():
                viruses.remove(v)
        popDensity=self.getTotalPop()/self.getMaxPop()
        viruses=self.getViruses()
        copy=viruses.copy()
        for v in copy:
            try:
                #Hay que añadir la lista de medicamentos
                a=v.reproduce(popDensity, self.getPrescriptions())
                viruses.append(a)
            except NoChildException:
                continue
        return self.getTotalPop()


#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    #Queremos 150 time-steps sin administrar medicamentos, añadir guttagonol y después otros 150 
    #Dibujamos la población y los resistentes
    mean=[]
    mean_resis=[]
    population=[]
    population_resis=[]
    time=[]
    for i in range(300):
        population.append([])
        population_resis.append([])
        time.append(i)
    
    for t in range(numTrials):
        viruses=[]
        for v in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        p=TreatedPatient(viruses, maxPop)
        for i in range(300):
            if i==150:
                #Añadimos el medicamento en el time-sep 150
                p.addPrescription('guttagonol')
            population[i].append(p.update())
            population_resis[i].append(p.getResistPop(['guttagonol']))
    
    for i in range(300):
        mean.append(sum(population[i])/numTrials)
        mean_resis.append((sum(population_resis[i])/numTrials))
    
    pylab.plot(mean, label = "Virus")
    pylab.plot(mean_resis, label = "Virus resistant to drugs")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()

simulationWithDrug(100, 10000, 0.1, 0.05, {'guttagonol':False}, 0.005, 100)
