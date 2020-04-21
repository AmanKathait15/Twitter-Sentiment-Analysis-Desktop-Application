from tkinter import *
from tkinter import ttk

root = Tk()

root.title("Twitter Sentiment Analysis Desktop Application")

root.geometry("800x600")
root.resizable(width = False , height = False)
root.configure(background = "lightblue")

label1 = Label(root,text="Twitter Sentiment Analysis",fg="blue",bg="skyblue",font=("",15,"bold"))
label1.pack(side=TOP,pady=20)

twitter_img = PhotoImage(file="/home/aman/Documents/my_projects/Sentiment Analysis in python/twitter.png")
label2 = Label(root,image = twitter_img).pack()

label3 = Label(root,text="Enter Twitter #tag to search",fg="red",bg="yellow",font=("",12,"bold"))
label3.pack(side=TOP,pady=10)

tag = Entry(root,justify=CENTER,font = ("verdana","15","bold"))
tag.pack(side = TOP)

frame = Frame(root,background="lightblue")
frame.pack()

search_button = Button(frame,text="Search",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"))
search_button.pack(side = LEFT,padx=5,pady=5)

clear_button = Button(frame,text="Clear",fg="white",bg="black",height=1,width=10,font=("verdana",10,"bold"))
clear_button.pack(side = LEFT,padx=5,pady=5)

label4 = Label(root,text="Select number of tweets to fetch from twitter",fg="red",bg="yellow",font=("",12,"bold"))
label4.pack(side=TOP,pady=10)

Values = (50,75,100,150,200,250,500,750,1000)

choices = ttk.Combobox(root,values=Values,height=10)
choices.pack()

label5 = Label(root,text="Select appropriate diagram to dislpay ",fg="red",bg="yellow",font=("",12,"bold"))
label5.pack(side=TOP,pady=10)

bottomFrame = Frame(root,background="lightblue",width=700,height=150)
bottomFrame.pack(side = TOP,pady = 20)

piechart_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/piechart.png")
scatterplot_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/scatter.png")
histogram_image = PhotoImage(file = "/home/aman/Documents/my_projects/Sentiment Analysis in python/histogram.png")

piechart_image = piechart_image.subsample(2,2)
scatterplot_image = scatterplot_image.subsample(2,2)
histogram_image = histogram_image.subsample(2,2)

piechart_button = Button(bottomFrame,image = piechart_image)
piechart_button.pack(side = LEFT,padx=20)

scatterplot_button = Button(bottomFrame, image = scatterplot_image)
scatterplot_button.pack(side = LEFT,padx=20)

histogram_button = Button(bottomFrame,image = histogram_image)
histogram_button.pack(side = LEFT,padx=20)

root.mainloop()
