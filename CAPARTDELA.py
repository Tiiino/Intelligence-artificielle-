import numpy as np
from random import randint
import random
import time

plateau = [0,0,0,0,0,0,0,0,0]
tour = 0



class Player:
	def __init__(self,robot,trainable,nom):
		self.robot = robot
		self.nom = nom
		self.trainable = trainable
		self.role = 0
		self.value = {}
		self.s = []
		self.reward = 0
		self.nb_win = 0
		self.nb_lose = 0
		self.nb_egalite = 0
		self.element = 0
		self.epsilon = 0.05
		self.possibleactions = []

def action(j,plateau):
	actions = j.possibleactions
	defval = -9999
	defaction = -1
	tempval = 0
	futurplateau = list(plateau)
	if random.randrange(0,101) > j.epsilon*100:
		for i in actions:
			futurplateau = list(plateau)
			futurplateau[i] = j.role
			if not(futurplateau in j.value.values()):#on ajoute un slot pour chaque nouvel état découvert
				j.value[0.000000001*j.element] = list(futurplateau)
				j.element += 1
			tempval = get_key(futurplateau,j)
			if tempval >= defval:
				defval = tempval
				defaction = i
	else:
		defaction = random.randrange(0,9)
	return defaction
def reset_stats(j):
	j.nb_win = 0
	j.nb_lose = 0
	j.nb_egalite = 0

def verification(plateau,joueur,afficher):
	temp = plateau

	if joueur.role == 1:
		j = 1
	else:
		j = 2

	for i in [0,3,6]:
		if (temp[i] == temp[i+1] & temp[i] == temp[i+2] & temp[i] == j): 
			if afficher == True:
				print('ligne')
			return True

	for i in [0,1,2]:
		if (temp[i] == temp[i+3] & temp[i] == temp[i+6] & temp[i] == j): 
			if afficher == True:
				print('colonne') 
			return True

	if (temp[0] == temp[4] & temp[0] == temp[8] & temp[0] == j) | (temp[2] == temp[4] & temp[2] == temp[6] & temp[2] == j):
		if afficher == True:
			print('diagonale') 
		return True 
	return False


def afficher(plateau):
	for i in [0,3,6]:
		print(plateau[i],plateau[i+1],plateau[i+2])
	print('')
				
def possible_actions(plateau):
	actions = []
	for i in range(0,9):
		if plateau[i] == 0:
			actions.append(i)
	return actions

def joue(plateau,j1,j2,state,tour,qui_commence):
	state = False
	affichage = False
	a_commence = qui_commence
	if j2.robot == False:
		affichage = True
		afficher(plateau)
	while 1 == 1:
		has_played = False
		#j1 joue
		if qui_commence != 2:
			
			if (plateau in j1.value.values()) == False:#on ajoute un slot pour chaque nouvel état découvert
				j1.value[0.000000001*j1.element] = list(plateau)
				j1.element = j1.element + 1
			
			j1.s.append(list(plateau)) #on enregistre l'état actuel
			j1.possibleactions = possible_actions(plateau)

			while 1 == 1:
				if affichage == True:
					print('A',j1.nom,' : ')
				if j1.robot == False:
					a1 = int(input())

				elif j1.robot == True:
					if j1.trainable == False:
						
						a1 = random.choice(j1.possibleactions)
					elif j1.trainable == True:

						a1 = action(j1,plateau)
				
				if plateau[a1] == 0:
					break
			plateau[a1] = j1.role
	
			if affichage == True:
				afficher(plateau)
			
			
			state = verification(plateau,j1,afficher)
			
			if state == True:
				if affichage == True:	
					print(j1.nom, "a gagné")
				j1.nb_win += 1
				j1.reward = 1
				j2.nb_lose += 1
				j2.reward = -2
				break
			
			if tour == 4:
				if affichage == True:	
					print("Egalité !")
				j1.reward = 0
				j2.reward = 0
				j1.nb_egalite = j1.nb_egalite + 1
				j2.nb_egalite = j2.nb_egalite + 1
				break
			qui_commence = 3
			if a_commence == 2:
				tour = tour + 1
			#j2 joue
	
		if qui_commence != 1:	
			if (plateau in j2.value.values()) == False:#on ajoute un slot pour chaque nouvel état découvert
				j2.value[0.000000001*j2.element] = list(plateau)

				
				j2.element = j2.element + 1
			

			j2.s.append(list(plateau)) #on enregistre l'état actuel
			j2.possibleactions = possible_actions(plateau)	

			while 1 == 1:
				if affichage == True:
					print('A',j2.nom,' : ') 

				if j2.robot == False:
					a2 = int(input())

				elif j2.robot == True:
					if j2.trainable == False:
						
						a2 = random.choice(j2.possibleactions)
					elif j2.trainable == True:

						a2 = action(j2,plateau)
				
				if plateau[a2] == 0:
					break
			plateau[a2] = j2.role
			afficher(plateau)
			
			if affichage == True:
				afficher(plateau) 
			
			
			state = verification(plateau,j2,afficher)
			
			if state == True:
				if affichage == True:
					print(j2.nom, "a gagné") 
				j2.nb_win += 1
				j2.reward = 1
				j1.nb_lose += 1
				j1.reward = -2
				break
		
			if tour == 4:
				if affichage == True:	
					print("Egalité !") 
				j1.reward = 0
				j2.reward = 0
				j2.nb_egalite = j2.nb_egalite + 1
				j2.nb_egalite = j2.nb_egalite + 1
				break
		if a_commence == 1:
				tour = tour + 1
		qui_commence = 3
		
		

def get_key(val,joueur): 
	for key, v in joueur.value.items(): 
		 if val == v: 
			 return key 

def game(j1,j2):
	stategame = False #True = finie 
	plateau = [0,0,0,0,0,0,0,0,0]
	#r1 fait une game contre r2
	qui_commence = 1#nnormalement random
	j1.role = qui_commence
	
	if j1.role == 1:
		#print(j1.nom,'commence')
		j2.role = 2
	if j1.role == 2:
		#print(j2.nom,'commence')
		j2.role = 1


	if j1.robot == False | j2.robot == False:
		
		affichage = True
		afficher(plateau)
	tour = 0
	joue(plateau,j1,j2,stategame,tour,qui_commence)
	#fin de la game

	#j1 train
	if not(plateau in j1.value.values()):#on ajoute un slot pour chaque nouvel état découvert
		j1.value[0.000000001*j1.element] = list(plateau)
		j1.element += 1
		
	if j1.reward == 1:
		temp_value = get_key(plateau,j1)
		temp_value = float(temp_value)
		temp_value = temp_value + 0.01*(1-temp_value)
		j1.value[temp_value] = j1.value.pop(get_key(plateau,j1))
	
	elif j1.reward == -2:
		temp_value = get_key(plateau,j1)
		temp_value = float(temp_value)
		temp_value = temp_value - 0.02*temp_value - 0.02
		j1.value[temp_value] = j1.value.pop(get_key(plateau,j1))
	
	elif j1.reward == 0:
		temp_value = get_key(plateau,j1)
		temp_value = float(temp_value)
		temp_value = temp_value - 0.02*temp_value
		j1.value[temp_value] = j1.value.pop(get_key(plateau,j1))
	
	for i in range(tour-1,-1,-1):
		temp_value = get_key(j1.s[tour],j1) 
		temp_value = temp_value + 0.02*(get_key(j1.s[tour+1]-temp_value))
		j1.value[temp_value] = j1.value.pop(get_key(j1.s[tour],j1))

	#j2 train
	if not(plateau in j2.value.values()):#on ajoute un slot pour chaque nouvel état découvert
		j2.value[0.000000001*j2.element] = list(plateau)
		j2.element += 1
		
	if j2.reward == 1:
		temp_value = get_key(plateau,j2)
		temp_value = float(temp_value)
		temp_value = temp_value + 0.02*(1-temp_value)
		j2.value[temp_value] = j2.value.pop(get_key(plateau,j2))
	
	elif j2.reward == -1:
		temp_value = get_key(plateau,j2)
		temp_value = float(temp_value)
		temp_value = temp_value - 0.02*temp_value - 0.02
		j2.value[temp_value] = j2.value.pop(get_key(plateau,j2))
	
	elif j2.reward == 0:
		temp_value = get_key(plateau,j2)
		temp_value = float(temp_value)
		temp_value = temp_value - 0.02*temp_value
		j2.value[temp_value] = j2.value.pop(get_key(plateau,j2))
	
	for i in range(tour-1,-1,-1):
		temp_value = get_key(j2.s[tour],j2) 
		temp_value = temp_value + 0.02*(get_key(j2.s[tour+1]-temp_value))
		j2.value[temp_value] = j2.value.pop(get_key(j2.s[tour],j2))
	j1.s.clear()
	j2.s.clear()
	j2.reward = 0
	j1.reward = 0

	
 

if __name__ == "__main__":
	r1 = Player(robot=True,trainable=False,nom='r1')
	r2 = Player(robot=True,trainable=False,nom='r2')
	moi = Player(robot=False,trainable=False,nom='moi')
	random_player = Player(robot=True,trainable=False,nom='random_player')
	r1.epsilon = 0.05
	r2.epsilon = 0.05
	for i in range(0,0):#games de découvertes
		game(r1,r2)
		#game(r2,r1)
		#print('Game ',i+1,' de découverte','Winrate r1: ',r1.nb_win,r1.nb_lose,'Winrate r2: ',r2.nb_win,r2.nb_lose,r2.nb_egalite)
	
	
	#winrate1 = r1.nb_win/(r1.nb_win + r1.nb_lose)
	#winrate2 = r2.nb_win/(r2.nb_win + r2.nb_lose)
	#print(winrate1*100,winrate2*100)	

	reset_stats(r1)
	reset_stats(r2)
	time.sleep(2)
	r1.trainable = True
	r2.trainable = True
	for i in range(0,25000):
		game(r1,r2)
		#game(r2,r1)
		print('r1 VS r2 :','Game ',i+1,'Winrate r1: ',r1.nb_win,r1.nb_lose,'Winrate r2: ',r2.nb_win,r2.nb_lose,r2.nb_egalite)
	
	
	winrate1 = r1.nb_win/(r1.nb_win + r1.nb_lose)
	winrate2 = r2.nb_win/(r2.nb_win + r2.nb_lose)
	print(winrate1*100,winrate2*100)	
	reset_stats(r1)
	reset_stats(r2)
	time.sleep(2)

	r1.epsilon = 0
	r2.epsilon = 0
	for i in range(0,1000):
		game(r1,random_player)
		print('r1 VS random_player :',' Game ',i+1,'Winrate r1: ',r1.nb_win,r1.nb_lose,r1.nb_egalite)
	
	
	winrate1 = r1.nb_win/(r1.nb_win + r1.nb_lose)
	
	print(winrate1*100)	

	time.sleep(2)

	
	print('GAME FINALE : r1 VS Moi')
	for i in range (0,6):
		print('AYMERICK TU ES NUL')
		game(r1,moi)	