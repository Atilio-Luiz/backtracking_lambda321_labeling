## -----------------------------------------------------
## L(3,2,1)-labeler program
## Author: Atilio Gomes Luiz
## Date: October 2020
## ---------------------------
## Program that reads the list of adjacency of a given 
## graph and prints all of its L(3,2,1)-labellings for a given lambda.
## It is assumed that the vertex set of the graph is 
## V(G) = {0,1,...,|V(G)|-1}
## ---------------------------
## Input: a file called edges.txt with the list of edges
## Output: a file called labelings.txt containg a list of 
## the vertex labels for each of the L(3,2,1)-labelings 
## found, if any.
## -----------------------------------------------------
import sys
import ast

def is_safe(G,vertex,labelling,l,mDist2,mDist3):
	""" A label is safe if it respects the lambda-labelling restrictions """
	for i in range(len(G)):
		if mDist3[vertex][i] > 0:
			if labelling[i] != -1:
				if l == labelling[i]:
					return False
					
					
	for i in range(len(G)):
		if mDist2[vertex][i] > 0:
			if labelling[i] != -1:
				if abs(l - labelling[i]) < 2:
					return False
	
	
	for neighbour in G[vertex]:
		if labelling[neighbour] != -1:
			if abs(l - labelling[neighbour]) < 3:
				return False	
			
	return True

		
def generate_labelling(G, edges, labelling, index, mAdj, mDist3, mLambda):
	""" A recursive function that searches for a graceful labelling."""
	if labelling.count(-1) == 0:
		print labelling
		return True
		
	for l in xrange(0,mLambda+1):
		if is_safe(G, index, labelling, l, mAdj, mDist3):
			labelling[index] = l
			
			generate_labelling(G,edges,labelling,index+1,mAdj,mDist3,mLambda)
			
			## backtrack
			labelling[index] = -1 
				
	return False

def inicializa_matriz(matriz, n):
	for i in range(n):
		linha = [];
		for i in range(n):
			linha.append(0)
		matriz.append(linha)
	

def multiplica_matriz(A,B,C):
	for i in range(len(A)):
		for j in range(len(B[0])):
			for k in range(len(B)):
				C[i][j] += A[i][k] * B[k][j]
	
		
if __name__ == "__main__":
	# 0-indexed labelling 
	
	## Open file with read only permit
    file_in = open('edges.txt')
    ## Open file with write permit
    file_out  = open("labellings.txt",'w')
    sys.stdout = file_out
    
    ## Read the first line of input file
    edges = file_in.readline().rstrip('\n')
    edges = ast.literal_eval(edges)
    
    ## Create graph G
    G = dict()
    for e in edges:
		if e[0] not in G:
			G[e[0]] = []
		if e[1] not in G:
			G[e[1]] = []
		G[e[0]].append(e[1])
		G[e[1]].append(e[0])
	
	## Create adjacency matrix M	
    order = len(G)
    M = []
    inicializa_matriz(M, order)
    for e in edges:
		M[e[0]][e[1]] = 1
		M[e[1]][e[0]] = 1
    
    Mdistance2 = []
    inicializa_matriz(Mdistance2, order)
    multiplica_matriz(M,M,Mdistance2)
    
    Mdistance3 = []
    inicializa_matriz(Mdistance3, order)
    multiplica_matriz(Mdistance2, M, Mdistance3)
	
		
	## list with the final labelling
    labelling = [-1]*len(G) 
    
    maxLabel = 8   
    
    generate_labelling(G, edges, labelling, 0, Mdistance2, Mdistance3, maxLabel)
    
    file_out.close()
    file_in.close()
