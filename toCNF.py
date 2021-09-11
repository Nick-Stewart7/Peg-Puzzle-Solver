#Nicholas Stewart nss67
import sys
import os

def getPreconditions(atomDict, jumpSS, holeSS, outFile):
	f = open(outFile, 'a')
	for jump in jumpSS:
		axiom = [(),(),()]
		jumpV = atomDict[jump]
		H1 = jump[0]
		H2 = jump[1]
		H3 = jump[2]
		I = jump[3]
		for hole in holeSS:
			if hole[0] == H1 and hole[1] == I:
				axiom[0] = atomDict[hole]
			if hole[0] == H2 and hole[1] == I:
				axiom[1] = atomDict[hole]
			if hole[0] == H3 and hole[1] == I:
				axiom[2] = -atomDict[hole]
		for value in axiom:
			fullStr = str(-jumpV) + " " + str(value) + "\n"
			f.write(fullStr)
	f.close()
	
def getCasual(atomDict, jumpSS, holeSS, outFile):
	f = open(outFile, 'a')
	for jump in jumpSS:
		axiom = [(),(),()]
		jumpV = atomDict[jump]
		H1 = jump[0]
		H2 = jump[1]
		H3 = jump[2]
		I = jump[3]
		I += 1
		for hole in holeSS:
			if hole[0] == H1 and hole[1] == I:
				axiom[0] = -atomDict[hole]
			if hole[0] == H2 and hole[1] == I:
				axiom[1] = -atomDict[hole]
			if hole[0] == H3 and hole[1] == I:
				axiom[2] = atomDict[hole]
		for value in axiom:
			fullStr = str(-jumpV) + " " + str(value) + "\n"
			f.write(fullStr)
	f.close()
	
def getFrame(atomDict, jumpSS, holeSS, outFile, N):
	f = open(outFile, 'a')
	#a
	for pegSlot in holeSS:
		axiom = []
		pegV = atomDict[pegSlot]
		H = pegSlot[0]
		I = pegSlot[1]
		if I != N - 1:
			for nextpegSlot in holeSS:
				if nextpegSlot[0] == H and nextpegSlot[1] == (I+1):
					axiom.append(atomDict[nextpegSlot])
			for jump in jumpSS:
				if (jump[0] == H or jump[1] == H) and jump[3] == I:
					axiom.append(atomDict[jump])
			if axiom != []:
				fullStr = str(-pegV)
				for value in axiom:
					fullStr += " " + str(value)
			fullStr += "\n"
			f.write(fullStr)
	#b
	for pegSlot in holeSS:
		axiom = []
		pegV = atomDict[pegSlot]
		H = pegSlot[0]
		I = pegSlot[1]
		if I != N - 1:
			for nextpegSlot in holeSS:
				if nextpegSlot[0] == H and nextpegSlot[1] == (I+1):
					axiom.append(-atomDict[nextpegSlot])
			for jump in jumpSS:
				if (jump[2] == H and jump[3] == I):
					axiom.append(atomDict[jump])
			if axiom != []:
				fullStr = str(pegV)
				for value in axiom:
					fullStr += " " + str(value)
			fullStr += "\n"
			f.write(fullStr)
	f.close()

def getSingleAction(atomDict, jumpSS, holeSS, outFile, N):
	f = open(outFile, 'a')
	upperTriangle = []
	for jump in jumpSS:
		I = jump[3]
		jumpV = atomDict[jump]
		for sameTimeJump in jumpSS:
			if sameTimeJump[3] == I and jumpV != atomDict[sameTimeJump]:
				if (jumpV, atomDict[sameTimeJump]) not in upperTriangle and (atomDict[sameTimeJump], jumpV) not in upperTriangle:
					upperTriangle.append((jumpV, atomDict[sameTimeJump]))
	for value in upperTriangle:
		fullStr = str(-value[0]) + " " + str(-value[1]) + "\n"
		f.write(fullStr)
	f.close()
	
def getStarting(atomDict, holeSS, missingPeg, outFile, N):
	f = open(outFile, 'a')
	missing = tuple(missingPeg)
	for hole in holeSS:
		if hole == missing:
			value = -atomDict[hole]
			fullStr = str(value) + "\n"
			f.write(fullStr)
		elif hole[1] == missing[1]:
			value = atomDict[hole]	
			fullStr = str(value) + "\n"
			f.write(fullStr)
	f.close()
	
def getEnding(atomDict, jumpSS, holeSS, outFile, N):
	f = open(outFile, 'a')
	endingJumps = []
	combos = []
	for hole in holeSS:
		if hole[1] == (N-1):
			fullStr = str(atomDict[hole]) + " "
			f.write(fullStr)
			endingJumps.append(atomDict[hole])
	f.write("\n")
	for jump in endingJumps:
		for nextJump in endingJumps:
			if jump != nextJump:
				if ((-jump, -nextJump) not in combos) and ((-nextJump, -jump) not in combos):
					entry = (-jump, -nextJump)
					combos.append(entry)
	for combo in combos:
		jump1 = combo[0]
		jump2 = combo[1]
		fullStr = str(jump1) + " " + str(jump2) + "\n"
		f.write(fullStr)
	f.close()
				
def createPropositions(lineData):
	Holes = []
	Jumps = []
	filetoWrite = 'propositions.txt'
	missingPeg = lineData[0]
	for K in range(1,len(lineData)):
		line = lineData[K]
		for element in line:
			if element not in Holes:
				Holes.append(element)
		if line not in Jumps:
			Jumps.append(line)
		reverseLine = line[::-1]
		if reverseLine not in Jumps:
			Jumps.append(reverseLine)
	N = len(Holes)
	JumpI = N - 2
	PegI = N - 1
	jumpSS = []
	holeSS = []
	for i in range(len(Jumps)):
		jump = Jumps[i]
		for j in range(JumpI):
			entry = jump.copy()
			entry.append(j+1)
			entry = tuple(entry)
			jumpSS.append(entry)		
	for i in range(len(Holes)):
		hole = Holes[i]
		for j in range(PegI):
			entry = [hole]
			entry.append(j+1)
			entry = tuple(entry)
			holeSS.append(entry)
	f = open(filetoWrite, 'w')
	atomDict = {}
	atomCount = 1
	for jump in jumpSS:
		jumpStr = str(jump)
		countStr = str(atomCount)
		fullStr = countStr + " Jump" + jumpStr + "\n"
		f.write(fullStr)
		dictEntry = tuple(jump)
		atomDict[dictEntry] = atomCount
		atomCount += 1
	for hole in holeSS:
		holeStr = str(hole)
		countStr = str(atomCount)
		fullStr = countStr + " Peg" + holeStr +"\n"
		f.write(fullStr)
		dictEntry = tuple(hole)
		atomDict[dictEntry] = atomCount
		atomCount += 1
	f.close()
	return (atomDict, jumpSS, holeSS, N, missingPeg)
			
def main():
	outFile = 'output.txt'
	f = open(outFile, 'w')
	f.close()
	fileName = sys.argv[1]
	data = open(fileName, 'r')
	lines = data.readlines()
	lineData = []
	for line in lines:
		line = line.strip('\n')
		line = line.split()
		for i in range(len(line)):
			num = line[i]
			num = int(num)
			line[i] = num
		lineData.append(line)
	lineData.remove([])
	result = createPropositions(lineData)
	atomDict = result[0]
	jumpSS = result[1]
	holeSS = result[2]
	N = result[3]
	missingPeg = result[4]
	getPreconditions(atomDict, jumpSS, holeSS, outFile)
	getCasual(atomDict, jumpSS, holeSS, outFile)
	getFrame(atomDict, jumpSS, holeSS, outFile, N)
	getSingleAction(atomDict, jumpSS, holeSS, outFile, N)
	getStarting(atomDict, holeSS, missingPeg, outFile, N)
	getEnding(atomDict, jumpSS, holeSS, outFile, N)
	
if __name__ == "__main__":
	main()
