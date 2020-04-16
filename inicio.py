from tkinter import *

def bt_click():
    if(str(ent.get()).isnumeric() and str(ent2.get()).isnumeric()):
        num1 = int(ent.get())
        num2 = int(ent2.get())
        result["text"]=num1+num2
    else:
        result["text"]="Valores não são numéricos"

janela = Tk()

lb = Label(janela, text="Insira os nomes a serem sumidos")
lb.place(x=100, y=50)
result = Label(janela, text="Soma")
result.place(x=100, y=350)

janela.title("Interface")
janela.geometry("500x400+200+200")

ent = Entry(janela)
ent.place(x=100, y=100)
ent2 = Entry(janela)
ent2.place(x=100,y=150)

bt = Button(janela, width=20, text = "faz1", command=bt_click)
bt.place(x=100, y=200)



janela.mainloop()