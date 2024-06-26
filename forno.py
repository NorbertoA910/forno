import tkinter as tk
from datetime import datetime, timedelta

placas = []
contador = 0
tempo_saida = 5

def adicionar_placa():
    global contador
    contador += 1
    agora = datetime.now()
    placa = {"numero": contador, "stuck": False, "entrada": agora, "botao_emperramento": None}
    
    if len(placas) > 0: #len() é uma função que returna o numero de items num objeto(placas)
        tempo_entrada_anterior = placas[-1]["entrada"]
        diferenca_tempo = (agora - tempo_entrada_anterior).total_seconds()
        placa["tempo_espera"] = max(int(entrada_temposaida.get()), diferenca_tempo) #max() é uma função que returna o items com o valor mais alto
    else:
        placa["tempo_espera"] = int(entrada_temposaida.get())
    
    placas.append(placa)
    entrada(placa)
    placa["botao_emperramento"] = tk.Button(frame_registro, text=f"Placa {contador} Emperrada", command=lambda p=placa: simular_emperramento(p)) 
    placa["botao_emperramento"].pack(pady=2)

def entrada(placa_info):
    placa_num = placa_info["numero"]
    texto_registro.insert(tk.END, f"Placa {placa_num} entrou\n")
    texto_registro.see(tk.END)
    if not placa_info["stuck"]:
        root.after(int(placa_info["tempo_espera"]) * 1000, lambda: saida(placa_info))

def saida(placa_info):
    placa_num = placa_info["numero"]
    
    if placa_info["stuck"]:
        texto_registro.insert(tk.END, f"Placa {placa_num} não pode sair porque está emperrada!\n")
        texto_registro.see(tk.END)
        return
    
    placa_index = placas.index(placa_info)
    for anterior in placas[:placa_index]:
        if anterior["stuck"]:
            texto_registro.insert(tk.END, f"Placa {placa_num} não pode sair porque a Placa {anterior['numero']} está emperrada!\n")
            texto_registro.see(tk.END)
            return
    
    texto_registro.insert(tk.END, f"Placa {placa_num} saiu\n")
    texto_registro.see(tk.END)
    placas.remove(placa_info)

def simular_emperramento(placa_info):
    placa_info["stuck"] = True
    placa_num = placa_info["numero"]
    texto_registro.insert(tk.END, f"Placa {placa_num} está emperrada!\n")
    texto_registro.see(tk.END)
    if placa_info["botao_emperramento"]:
        placa_info["botao_emperramento"].pack_forget()

def limpar_lista():
    global placas, contador
    placas.clear()
    contador = 0
    texto_registro.delete(1.0, tk.END)
    for widget in frame_registro.winfo_children():
        widget.pack_forget()

root = tk.Tk()
root.title("Sensores Forno de placas")
root.resizable(width=False, height=False)

frame_controles = tk.Frame(root)
frame_controles.pack(padx=10, pady=10)

tk.Button(frame_controles, text="Adicionar Placa", command=adicionar_placa).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_controles, text="Limpar Lista", command=limpar_lista).grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_controles, text="Tempo de saída (s):").grid(row=0, column=2, padx=5, pady=5)

entrada_temposaida = tk.Entry(frame_controles)
entrada_temposaida.grid(row=0, column=3, padx=5, pady=5)
entrada_temposaida.insert(tk.END, str(tempo_saida))

frame_registro = tk.Frame(root)
frame_registro.pack(padx=10, pady=10)

frame_list = tk.Frame(root)
frame_list.pack(padx=10, pady=10)

tk.Label(frame_list, text="Registro de Movimentos:").pack()

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

texto_registro = tk.Text(frame_list, height=10, width=60, yscrollcommand=scrollbar.set)
texto_registro.pack()

scrollbar.config(command=texto_registro.yview)

root.mainloop()