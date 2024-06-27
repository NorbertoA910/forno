from tkinter import * 

placas = []
placapresa = []
contador = 0
defaulttempo = 5

root = Tk()
root.title("Forno de Placas")
root.resizable(width=False, height=False)

def adicionar_placas():
    global contador
    contador += 1
    placas.append(contador)
    print(placas)
    entrada(placas[-1])
    
def entrada(placa):
    listavalores.insert(END, f"Placa {placa} entrou\n")
    root.after(int(tempoentradasaida.get())*1000, lambda: saida(placa))

def saida(placa):
    listavalores.insert(END, f"Placa {placa} saiu\n")
    placas.remove(placa)
    root.after(2000, reset)
    
def reset():
    global contador
    if not placas:
        contador = 0
        listavalores.delete('1.0', END)

controles = Frame(root)
controles.grid(row=0, column=0)

addplacas = Button(controles, text="Adicionar Placa", command=adicionar_placas)
addplacas.grid(row=0, column=0)

tempoentradasaida = Entry(controles)
tempoentradasaida.grid(row=0, column=1)
tempoentradasaida.insert(END, str(defaulttempo))
Label(controles, text="Tempo de saida(s)").grid(row=1, column=1)

lista = Frame(root)
lista.grid(row=1, column=0)

Label(lista, text="Registro de Movimentos:").pack()

scrolllista = Scrollbar(lista)
scrolllista.pack(side=RIGHT, fill=Y)

listavalores = Text(lista, height=10, width=60, yscrollcommand=scrolllista)
listavalores.pack() 

scrolllista.config(command=listavalores.yview)

root.mainloop()