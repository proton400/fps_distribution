#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math
import statistics
import csv
import matplotlib.pyplot as plt
import os, tkinter, tkinter.filedialog,tkinter.messagebox

def filename():
    root = tkinter.Tk()
    root.withdraw()
    ftyp = [("","*.csv")]
    idir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo("FPS DEVIATION", "SELECT FILE TO ANAYZE")
    filenames = tkinter.filedialog.askopenfilenames(filetypes = ftyp, initialdir = idir)#chosing some files simultaneously
    filelist = list(filenames)
    return filelist

def gaussian(x,mean,std):
    return 1/np.sqrt(2*np.pi*std**2)*np.exp(-(x-mean)**2/(2*std**2))

def log_normal_distribution(x,mean,std):
    return 1/(np.sqrt(2*np.pi)*std*x)*np.exp(-(np.log(x)-mean)**2/(2*std**2))

class fps_deviation():
    def __init__(self):
        self.MAX_OF_FPS = 300
        self.BINS = 300 #width of the stick on hist
        self.INFI = 999
        self.filename = filename()
        self.df = pd.read_csv(self.filename[0])
        self.df1 = self.df["MsBetweenDisplayChange"]#df1 contains frame time of each files
        if len(self.filename)>=2:
            for i in range(len(self.filename)-1):
                self.df = pd.read_csv(self.filename[i+1])
                self.df = self.df.rename(columns={"MsBetweenDisplayChange":str(i)})
                self.df1 = pd.concat([self.df1,self.df[str(i)]], axis = 1)
    def define_axis(self):
        f = lambda x:round(1/x*1000,1)
        g = lambda x:np.log(x)
        self.df1 = self.df1.replace(0,0.000000001)
        self.df2 = self.df1.apply(f)#df2 contains FPS
        self.df2 = self.df2.replace(np.inf,self.INFI)
        self.df3 = self.df2.apply(g)#df3 contains log(FPS)
    def plot_deviation(self):
        x = np.linspace(0.1,300,3000)
        if len(self.filename)>=2:
            bufdf=self.df2[self.df2["MsBetweenDisplayChange"] < self.MAX_OF_FPS]
            bufdf3=self.df3[self.df3["MsBetweenDisplayChange"] < np.log(self.MAX_OF_FPS)]
            plt.hist(bufdf["MsBetweenDisplayChange"], range=(0,self.MAX_OF_FPS), bins=self.BINS, density=True)
            #plt.plot(x, gaussian(x,bufdf["MsBetweenDisplayChange"].mean(), bufdf["MsBetweenDisplayChange"].std()))
            plt.plot(x, log_normal_distribution(x,bufdf3["MsBetweenDisplayChange"].mean(), bufdf3["MsBetweenDisplayChange"].std()))
            plt.show()
            for i in range(len(self.filename)-1):
                bufdf=self.df2[self.df2[str(i)] < self.MAX_OF_FPS]
                bufdf3=self.df3[self.df3[str(i)] < np.log(self.MAX_OF_FPS)]
                plt.hist(bufdf[str(i)], range=(0,self.MAX_OF_FPS), bins=self.BINS, density=True)
                #plt.plot(x, gaussian(x,bufdf[str(i)].mean(), bufdf[str(i)].std()))
                plt.plot(x, log_normal_distribution(x,bufdf3[str(i)].mean(), bufdf3[str(i)].std()))              
                plt.show()
        else:
            bufdf=self.df2[self.df2< self.MAX_OF_FPS]
            bufdf3=self.df3[self.df3< np.log(self.MAX_OF_FPS)]
            plt.hist(bufdf, range=(0,self.MAX_OF_FPS), bins=self.BINS, density=True)
            #plt.plot(x, gaussian(x,bufdf.mean(), bufdf.std()))
            plt.plot(x, log_normal_distribution(x,bufdf3.mean(), bufdf3.std()))  
            plt.show()
    def data_print(self):
        if len(self.filename)>=2:
            bufdf=self.df2[self.df2["MsBetweenDisplayChange"] < self.MAX_OF_FPS]
            result=[bufdf["MsBetweenDisplayChange"].mean(),bufdf["MsBetweenDisplayChange"].std()]
            del bufdf
            for i in range(len(self.filename)-1):
                bufdf=self.df2[self.df2[str(i)] < self.MAX_OF_FPS]
                buf_result=[bufdf[str(i)].mean(),bufdf[str(i)].std()]
                del bufdf
                result.extend(buf_result)
        else:
            bufdf=self.df2[self.df2< self.MAX_OF_FPS]
            result=[bufdf.mean(),bufdf.std()]
        print(result)


def main():
    fps = fps_deviation()
    fps.define_axis()
    fps.data_print()
    fps.plot_deviation()
if __name__ == "__main__":
    main()
    #calculate mean and standard deviation after applay log to fps for fitting with log-normal-distribution
