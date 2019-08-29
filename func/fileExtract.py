import os
import numpy as np
import math
import csv

class dataExtract():

    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.lines = ""
        self.fileasList = []
        self.floatList = []
        self.columnData = 0
        self.ext = ""

    def num_there(self, string):
        try:
            float(string)
            allDigit = True
        except:
            allDigit = False
        return allDigit
    
    def f1(self, x):
        return np.sin(x)
    def f2(self, x):
        return np.cos(x)
    def f3(self, x):
        return np.log(x)

    def f4(self, x):
        return np.sqrt(x)
    
    def f5(self, x, y):
        return np.sin(np.sqrt(x ** 2 + y ** 2))
    def f6(self, x, y):
        return (np.cos(x) + np.sin(y))
    
    def getDataFromList(self, inlist):
        deffloatList = []
        for it in inlist:
                tempList = []
                for its in it:
                    if self.num_there(its):
                        tempList.append(float(its))
                if tempList != []:
                    deffloatList.append(tempList)
        return deffloatList

    def getData2d(self, file, func):
        self.ext = os.path.splitext(file)[-1].lower()
        if self.ext == ".csv":
            with open(file, 'rb') as f:
                reader = csv.reader(f)
                self.fileasList = list(reader)
            self.floatList = self.getDataFromList(self.fileasList)
            self.columnData = len(self.floatList[0])
            for el in self.floatList:
                if len(self.floatList[0]) == 1:
                    self.x.append(el[0])
                    if func == "Sin":
                        self.y = self.f1(self.x)
                    if func == "Cos":
                        self.y = self.f2(self.x)
                    if func == "log":
                        self.y = self.f3(self.x)
                    if func == "e":
                        self.y = self.f4(self.x)
                if len(self.floatList[0]) == 2:
                    self.x.append(el[0])
                    self.y.append(el[1])
        if self.ext == ".txt":
            f = open(file, "r")
            self.lines = f.readlines()
            for line in self.lines:
                self.fileasList.append(line.split())
            self.floatList = self.getDataFromList(self.fileasList)
            self.columnData = len(self.floatList[0])
            for el in self.floatList:
                if len(self.floatList[0]) == 1:
                    self.x.append(el[0])
                    if func == "Sin":
                        self.y = self.f1(self.x)
                    if func == "Cos":
                        self.y = self.f2(self.x)
                    if func == "log":
                        self.y = self.f3(self.x)
                    if func == "e":
                        self.y = self.f4(self.x)
                if len(self.floatList[0]) == 2:
                    self.x.append(el[0])
                    self.y.append(el[1])
        if self.ext == ".np":
            A = np.loadtxt(file)
            self.columnData = len(np.size(A, 1))
            if self.columnData == 2:
                self.x = A[:, 0]
                self.y = A[:, 1]
            if self.columnData == 1:
                self.x = A[:, 0]
                if func == "Sin":
                    self.y = self.f1(self.x)
                if func == "Cos":
                    self.y = self.f2(self.x)
                if func == "log":
                    self.y = self.f3(self.x)
                if func == "e":
                    self.y = self.f4(self.x)

    def getData3d(self, file, func, typeP):
        self.ext = os.path.splitext(file)[-1].lower()
        if self.ext == ".txt":
            f = open(file, "r")
            self.lines = f.readlines()
            for line in self.lines:    
                self.fileasList.append(line.split())
            self.floatList = self.getDataFromList(self.fileasList)
            self.columnData = len(self.floatList[0])
            for el in self.floatList:
                if len(self.floatList[0]) == 3:
                    self.x.append(el[0])
                    self.y.append(el[1])
                    self.z.append(el[2])
                if len(self.floatList[0]) == 2:
                    self.x.append(el[0])
                    self.y.append(el[1])
        if self.ext == ".csv":
            with open(file, 'rb') as f:
                reader = csv.reader(f)
                self.fileasList = list(reader)
            self.columnData = len(self.floatList[0])
            for el in self.floatList:
                if len(self.floatList[0]) == 3:
                    self.x.append(el[0])
                    self.y.append(el[1])
                    self.z.append(el[2])
        if self.ext == ".np":
            X = []
            Y = []
            Z = []
            A = np.loadtxt(file)
            self.columnData = len(np.size(A, 1))
            if self.columnData == 3:
                X = A[:, 0]
                Y = A[:, 1]
                Z = A[:, 2]
                self.x = X
                self.y = Y
                self.z = Z
            if self.columnData == 2:
                X = A[:, 0]
                Y = A[:, 1]
                self.x = X
                self.y = Y
        if typeP == "Surface" or typeP == "Simple Contour" \
            or typeP == "Fill Contour" or typeP == "WireFrame" \
            or typeP == "Contour3D":
            if self.columnData == 3:       
                X = self.x
                Y = self.y
                Z = self.z
                zindex = 0
                lengf = math.sqrt(len(X))
                leng = int(lengf)
                self.x = np.zeros(shape=(leng, leng), dtype=float)
                self.y = np.zeros(shape=(leng, leng), dtype=float)
                self.z = np.zeros(shape=(leng, leng), dtype=float)
                for a in range(leng):
                    for b in range(leng):
                        self.x[a, b] = X[zindex]
                        self.y[a, b] = Y[zindex]
                        self.z[a, b] = Z[zindex]
                        zindex = zindex + 1 
        if typeP == "Surface" or typeP == "Simple Contour" or typeP == "Fill Contour" \
            or typeP == "WireFrame" or typeP == "Contour3D":
            if self.columnData == 2:
                X = self.x
                Y = self.y
                [self.x, self.y] = np.meshgrid(X, Y)
                if func == "Sin Cos":
                    self.z = self.f5(self.x, self.y)
                if func == "Sqrt":
                    self.z = self.f6(self.x, self.y)
        if typeP == "Line" or typeP == "Scatter":
                if self.columnData == 2:
                    if func == "Sin Cos":
                        self.z = self.f5(self.x, self.y)
                    if func == "Sqrt":
                        self.z = self.f6(self.x, self.y)