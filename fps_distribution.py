#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math
import statistics
import csv
import matplotlib.pyplot as plt
import os, tkinter, tkinter.filedialog,tkinter.messagebox

plt.rcParams['font.family']='sans-serif'#使用するフォント
plt.rcParams['xtick.direction']='in'#メモリ内向き('in')外向き('out')双方向('inout')
plt.rcParams['ytick.direction']='in'
plt.rcParams['xtick.major.width'] = 1.0#メモリ線の線幅
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['font.size'] = 20#フォントの太さ
plt.rcParams['axes.linewidth'] = 1.0#囲みの太さ

def filename():
    root = tkinter.Tk()
    root.withdraw()
    ftyp = [("","*.csv")]
    idir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo("FPS DEVIATION", "SELECT FILE TO ANAYZE")
    filenames = tkinter.filedialog.askopenfilenames(filetypes = ftyp, initialdir = idir)#chosing some files simultaneously
    filelist = list(filenames)
    return filelist

def cutfilename(filelist):
    returnlist=[]
    for i in filelist:
        for j in range(len(i)):
            if i[j]=="/":
                regi=j
        returnlist.append(i[regi+1:])
    return returnlist

def gaussian(x,mean,std):
    return 1/np.sqrt(2*np.pi*std**2)*np.exp(-(x-mean)**2/(2*std**2))

def log_normal_distribution(x,mean,std):
    return 1/(np.sqrt(2*np.pi)*std*x)*np.exp(-(np.log(x)-mean)**2/(2*std**2))

def figname(filelist):
    savename = str()
    for i in filelist:
        savename = savename+"_"+i[:-4]
    return savename

class fps_deviation():
    def __init__(self):
        self.MAX_OF_FPS = 300
        self.BINS = 600 #width of the stick on hist
        self.INFI = 999
        self.PSEUDO_ZERO = 0.000001
        self.dfname = filename()
        self.filename = cutfilename(self.dfname)
        self.df = pd.read_csv(self.dfname[0])
        self.df = self.df.rename(columns={"MsBetweenDisplayChange":self.filename[0]})
        self.df1 = self.df[self.filename[0]]#df1 contains frame time of each files
        if len(self.filename)>=2:
            for i in range(len(self.filename)-1):
                self.df = pd.read_csv(self.dfname[i+1])
                self.df = self.df.rename(columns={"MsBetweenDisplayChange":self.filename[i+1]})
                self.df1 = pd.concat([self.df1,self.df[self.filename[i+1]]], axis = 1)
        print(self.df1)
        
    def define_axis(self):
        f = lambda x:round(1/x*1000,1)
        g = lambda x:np.log(x)
        self.df1 = self.df1.replace(0,self.PSEUDO_ZERO)
        self.df2 = self.df1.apply(f)#df2 contains FPS
        self.df2 = self.df2.replace(np.inf,self.INFI)
        self.df2 = self.df2.replace(0,self.PSEUDO_ZERO)
        self.df3 = self.df2.apply(g)#df3 contains log(FPS)
    def plot_deviation(self):
        fig = plt.figure()
        x = np.linspace(0.1,300,3000)
        if len(self.filename)>=2:
            for i in range(len(self.filename)):
                bufdf=self.df2[self.df2[self.filename[i]] < self.MAX_OF_FPS]
                plt.hist(bufdf[self.filename[i]], range=(0,self.MAX_OF_FPS), bins=self.BINS, density=True, alpha=0.45, label=self.filename[i])
                plt.plot(x, gaussian(x,bufdf[self.filename[i]].mean(), bufdf[self.filename[i]].std()))
                plt.annotate(round(bufdf[self.filename[i]].mean(),2), xy = (round(bufdf[self.filename[i]].mean()), 0), xytext = (round(bufdf[self.filename[i]].mean()), -0.004-0.002*i),size = 18, color = plt.rcParams["axes.prop_cycle"].by_key()["color"][i*2], arrowprops = dict(color = plt.rcParams["axes.prop_cycle"].by_key()["color"][i*2]))
                #bufdf3=self.df3[self.df3[self.filename[i]] < np.log(self.MAX_OF_FPS)]
                #plt.plot(x, log_normal_distribution(x,bufdf3[self.filename[i]].mean(), bufdf3[self.filename[i]].std()))              
        else:
            bufdf=self.df2[self.df2< self.MAX_OF_FPS]
            plt.hist(bufdf, range=(0,self.MAX_OF_FPS), bins=self.BINS, density=True, alpha=0.5, label=self.filename)
            plt.plot(x, gaussian(x,bufdf.mean(), bufdf.std()))
            plt.annotate(round(bufdf.mean(),2), xy = (round(bufdf.mean()), 0), xytext = (round(bufdf.mean()), -0.004),size = 18, color = plt.rcParams["axes.prop_cycle"].by_key()["color"][0], arrowprops = dict(color = plt.rcParams["axes.prop_cycle"].by_key()["color"][0]))
            #bufdf3=self.df3[self.df3< np.log(self.MAX_OF_FPS)]
            #plt.plot(x, log_normal_distribution(x,bufdf3.mean(), bufdf3.std()))
        plt.xlabel("FPS", labelpad = 40)
        plt.ylabel("Probability")
        plt.legend(fontsize=14)
        savename = figname(self.filename)
        fig.savefig(savename+".png", dpi = 256, facecolor = "white", bbox_inches = "tight")
        plt.show()

    def data_print(self):
        if len(self.filename)>=2:
            for i in range(len(self.filename)):
                bufdf=self.df2[self.df2[self.filename[i]] < self.MAX_OF_FPS]
                buf_result=[bufdf[self.filename[i]].mean(),bufdf[self.filename[i]].std()]
                del bufdf
                print(buf_result)
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