import tkinter as tk
from datetime import datetime

placas = []
contador = 0
tempo_saida = 5

def adicionar_placa():
    global contador
    contador += 1
    agora = datetime.now()
    nova_placa = {
        "numero": contador,
        "stuck": False,
        "entrada": agora,
        "tempo_espera": 0,
        "aviso_emperrado": False,
        "botao_emperramento": None,
        "botao_desemperramento": None
    }
    
    if len(placas) > 0:
        tempo_entrada_anterior = placas[-1]["entrada"]
        diferenca_tempo = (agora - tempo_entrada_anterior).total_seconds()
        nova_placa["tempo_espera"] = diferenca_tempo
    else:
        nova_placa["tempo_espera"] = int(entrada_temposaida.get())
    
    placas.append(nova_placa)
    entrada(nova_placa)
    
    nova_placa["botao_emperramento"] = tk.Button(frame_registro, text=f"Placa {contador} Emperrada", command=lambda p=nova_placa: simular_emperramento(p)) 
    nova_placa["botao_emperramento"].pack(pady=2)

def entrada(placa_info):
    placa_num = placa_info["numero"]
    texto_registro.insert(tk.END, f"Placa {placa_num} entrou\n")
    texto_registro.see(tk.END)

def saida():
    agora = datetime.now()
    
    for i, placa_info in enumerate(placas):
        placa_num = placa_info["numero"]
        tempo_desde_entrada = (agora - placa_info["entrada"]).total_seconds()
        
        if i == 0:
            tempo_esperado_saida = int(entrada_temposaida.get())
        else:
            placa_anterior = placas[i-1]
            if placa_anterior["stuck"]:
                break
            tempo_esperado_saida = placa_anterior["tempo_espera"] + int(entrada_temposaida.get())

        if tempo_desde_entrada >= tempo_esperado_saida:
            if not placa_info["stuck"]:
                texto_registro.insert(tk.END, f"Placa {placa_num} saiu\n")
                texto_registro.see(tk.END)
                if placa_info["botao_emperramento"]:
                    placa_info["botao_emperramento"].pack_forget()
                if placa_info["botao_desemperramento"]:
                    placa_info["botao_desemperramento"].pack_forget()
                placas.remove(placa_info)
                break
            else:
                if not placa_info["aviso_emperrado"]:
                    texto_registro.insert(tk.END, f"Placa {placa_num} não foi detectada como saída após o tempo de espera!\n")
                    texto_registro.see(tk.END)
                    placa_info["aviso_emperrado"] = True

    root.after(1000, saida)

def simular_emperramento(placa_info):
    placa_info["stuck"] = True
    placa_num = placa_info["numero"]
    texto_registro.insert(tk.END, f"Placa {placa_num} está emperrada!\n")
    texto_registro.see(tk.END)
    
    if placa_info["botao_emperramento"]:
        placa_info["botao_emperramento"].pack_forget()
    
    placa_info["botao_desemperramento"] = tk.Button(frame_registro, text=f"Placa {placa_num} Desemperrar", command=lambda p=placa_info: desemperrar_placa(p)) 
    placa_info["botao_desemperramento"].pack(pady=2)

def desemperrar_placa(placa_info):
    placa_info["stuck"] = False
    placa_num = placa_info["numero"]
    texto_registro.insert(tk.END, f"Placa {placa_num} foi desemperrada!\n")
    texto_registro.see(tk.END)
    
    if placa_info["botao_desemperramento"]:
        placa_info["botao_desemperramento"].pack_forget()

def limpar_tudo():
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
tk.Button(frame_controles, text="Limpar", command=limpar_tudo).grid(row=0, column=1, padx=5, pady=5)

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

root.after(1000, saida)
root.mainloop()
