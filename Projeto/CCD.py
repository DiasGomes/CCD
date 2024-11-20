from tkinter import *
from CD_REV1 import calcula_curva_descarga
from pandastable import Table
from tkinter import ttk

"""
Created on Fri Nov 18 12:02:07 2024

@author: joao.gomes
"""

#################################################################
#                           FUNCOES
#################################################################

# gera o valor de saida
def generates_response():
    global cd, El_Max, El_Soleira, Discretizacao, tipo_secao, tipo, dimensoes_secao, exibe_msg
    fields = []
    dimensoes_secao = {}
    form_incomplete = False
    msg = ""
    cor = "black"
    # pega o valor dos campos do formulario de secao
    for widget in form_frame.winfo_children():
        if isinstance(widget, Entry):
            fields.append(widget.get())
    # pega informacoes do formulario geral
    try:
        _El_Soleira = float(El_Soleira.get())
        _El_Max = float(El_Max.get())
        _Discretizacao = float(Discretizacao.get())
    except:
        form_incomplete = True
    _tipo_secao = str(tipo_secao.get())
    # dimensoes_secao
    if _tipo_secao == "circular":
        try:
            dimensoes_secao["diametro"] = float(fields[0])
            dimensoes_secao["linhas"] = float(fields[1])
            dimensoes_secao["H2"] = dimensoes_secao["diametro"]
        except:
            form_incomplete = True    
    elif _tipo_secao == "retangular":
        try:
            dimensoes_secao["base"] = float(fields[0])
            dimensoes_secao["altura"] = float(fields[1])
            dimensoes_secao["H2"] = dimensoes_secao["altura"]
        except:
            form_incomplete = True
    elif _tipo_secao == "soleira":
        try:
            dimensoes_secao["Cd"] = float(fields[0])
            dimensoes_secao["Comprimento"] = float(fields[1])
            dimensoes_secao["N_pilar"] = float(fields[2])
            dimensoes_secao["Ka"] = float(fields[3])
            dimensoes_secao["Kp"] = float(fields[4])
            dimensoes_secao["H2"] = float(fields[5])
            dimensoes_secao["z"] = float(fields[6])
        except:
            form_incomplete = True
    elif _tipo_secao == "trapezoidal":   
        try: 
            dimensoes_secao["inclinacao_talude"] = float(fields[0])
            dimensoes_secao["base_menor"] = float(fields[1])
            dimensoes_secao["altura"] = float(fields[2])
            dimensoes_secao["H2"] = dimensoes_secao["altura"] 
        except:
            form_incomplete = True
    else:
        form_incomplete = True
    # verifica se o formulario foi prenchido e calcula o valor de saida
    if  form_incomplete == False:
        try:
            cd = calcula_curva_descarga(_tipo_secao, dimensoes_secao, _El_Soleira, _El_Max, _Discretizacao, tipo)
            msg = "Calculado a curva de descarga"
            cor = "green"
            # gera uma nova tela com a tabela gerada
            tela_cd = Toplevel()
            tela_cd.title(f"Curva de Descarga - {_tipo_secao}")
            tabela = Table(tela_cd, dataframe=cd, showtoolbar=True, showstatusbar=True)
            tabela.show()
        except Exception as e:
            msg = f"ERRO: {e}"
            cor = "red"
    else:
        msg = "Campo(s) não prenchido(s)"
        cor = "red"
    # mostra a resposta
    exibe_msg.config(text = msg, foreground=cor)

# Permite valores vazios ou valores que podem ser convertidos para float
def validate_float(new_value):
    if new_value == "":
        return True
    try:
        float(new_value)
        return True
    except ValueError:
        return False

# ATUALIZA OS FORMULARIOS CONFORME O TIPO DE SACAO
def update_form(*args):
    # Remove os widgets existentes
    for widget in form_frame.winfo_children():
        widget.destroy()  

    _tipo_secao = tipo_secao.get()
    
    #############
    # CIRCULAR
    #############
    if _tipo_secao == "circular":
        # Diâmetro da seção circular
        diametro_Label = ttk.Label(form_frame, text="Diâmetro da seção circular (metros)", style="TLabel")
        diametro_Label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="w")
        diametro = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        diametro.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky="e")
        # Linhas operando"
        linha_Label = ttk.Label(form_frame, text="Linhas operando", style="TLabel")
        linha_Label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="w")
        linha = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        linha.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky="e")
    #############
    # RETANGULAR
    #############
    elif _tipo_secao == "retangular":
        # base da seção retangular
        base_Label = ttk.Label(form_frame, text="Base da seção retangular (metros)", style="TLabel")
        base_Label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="w")
        base = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        base.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky="e")
        # altura da seção retangular
        altura_Label = ttk.Label(form_frame, text="Altura da seção retangular (metros)", style="TLabel")
        altura_Label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="w")
        altura = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        altura.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky="e")
    #############
    # SOLEIRA
    #############
    elif _tipo_secao == "soleira":
        # coeficiente de descarga da soleira
        coeficiente_Label = ttk.Label(form_frame, text="Coeficiente de descarga da soleira", style="TLabel")
        coeficiente_Label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="w")
        coeficiente = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        coeficiente.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky="e")
        # comprimento da soleira
        comprimento_Label = ttk.Label(form_frame, text="Comprimento da soleira", style="TLabel")
        comprimento_Label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="w")
        comprimento = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        comprimento.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky="e")
        # numero de pilares na soleira
        pilares_Label = ttk.Label(form_frame, text="Pilares na soleira", style="TLabel")
        pilares_Label.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="w")
        pilares = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        pilares.grid(column=1, row=2, padx=PAD_X, pady=PAD_Y, sticky="e")
        # ka
        ka_Label = ttk.Label(form_frame, text="Ka", style="TLabel")
        ka_Label.grid(column=0, row=3, padx=PAD_X, pady=PAD_Y, sticky="w")
        ka = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        ka.grid(column=1, row=3, padx=PAD_X, pady=PAD_Y, sticky="e")
        # kp
        kp_Label = ttk.Label(form_frame, text="Kp", style="TLabel")
        kp_Label.grid(column=0, row=4, padx=PAD_X, pady=PAD_Y, sticky="w")
        kp = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        kp.grid(column=1, row=4, padx=PAD_X, pady=PAD_Y, sticky="e")
        # Altura maxima do NA
        altura_Label = ttk.Label(form_frame, text="Altura maxima do NA", style="TLabel")
        altura_Label.grid(column=0, row=5, padx=PAD_X, pady=PAD_Y, sticky="w")
        altura = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        altura.grid(column=1, row=5, padx=PAD_X, pady=PAD_Y, sticky="e")
        # inclinacao da parede
        inclincao_Label = ttk.Label(form_frame, text="Inclinção da parede", style="TLabel")
        inclincao_Label.grid(column=0, row=7, padx=PAD_X, pady=PAD_Y, sticky="w")
        inclinacao = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        inclinacao.grid(column=1, row=7, padx=PAD_X, pady=PAD_Y, sticky="e")
        # tipo de soleira
        def toggle_entry(*args):
            global tipo
            tipo = str(tipo_opt.get())
            if tipo_opt.get() == "retangular":
                inclinacao.delete(0, END) 
                inclinacao.insert(0, 0)
                inclinacao.config(state="disabled")  
            else: 
                inclinacao.config(state="normal")
        
        tipo_Label = ttk.Label(form_frame, text="Tipo de soleira", style="TLabel")
        tipo_Label.grid(column=0, row=6, padx=PAD_X, pady=PAD_Y, sticky="w")
        tipo_opt = StringVar(form_frame, value="Select an Option") 
        menu = ttk.OptionMenu(form_frame, tipo_opt, *LST_TIPOS, style="TMenubutton") 
        menu.grid(column=1, row=6, padx=PAD_X, pady=PAD_Y, sticky="e")
        tipo_opt.trace_add("write", toggle_entry) 
    #############
    # TRAPEZOIDAL
    #############
    elif _tipo_secao == "trapezoidal":
        # inclinação da parede do dispositivo
        inclinacao_Label = ttk.Label(form_frame, text="Inclinação da parede do dispositivo (m/m)", style="TLabel")
        inclinacao_Label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky="w")
        inclincao = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        inclincao.grid(column=1, row=0, padx=PAD_X, pady=PAD_Y, sticky="e")
        # base menor da seção trapezoidal
        base_Label = ttk.Label(form_frame, text="Base menor da seção trapezoidal (metros)", style="TLabel")
        base_Label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="w")
        base = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        base.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky="e")
        # altura da seção trapezoidal
        altura_Label = ttk.Label(form_frame, text="Altura da seção trapezoidal (metros)", style="TLabel")
        altura_Label.grid(column=0, row=2, padx=PAD_X, pady=PAD_Y, sticky="w")
        altura = ttk.Entry(form_frame, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
        altura.grid(column=1, row=2, padx=PAD_X, pady=PAD_Y, sticky="e")

#################################################################
#                          PARAMETROS
#################################################################
TITULO = "CCD v1.0.0"
LST_TIPOS_SECOES = ["Escolha uma opção", "circular", "retangular", "soleira", "trapezoidal"] 
LST_TIPOS = ["Escolha uma opção", "retangular", "side_flow", "trapezoidal", "triangular"]
PAD_X = 25
PAD_Y = 7
tipo = None
cd = None
fonte = ("Helvetica", 10)

#################################################################
#                         CONFIGURACOES
#################################################################
tela = Tk()
tela.title(TITULO)
# Registra a função para uso no validatecommand
vcmd = tela.register(validate_float) 
# configurações de estilo de tela 
tela.configure(bg="#f5f5f5")  # Cor de fundo da janela

# Configurar estilos
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=fonte, background="#f5f5f5")
style.configure("TEntry", font=fonte, padding=3)
style.configure("TButton", font=fonte+("bold",), foreground="white", background="#2c6e49")
style.configure("TMenubutton", font=fonte, background="#f0f0f0", foreground="#333")
# Cor ao pressionar
style.map("TButton", background=[("active", "#2d9f79")])  
style.map("TMenubutton", background=[("active", "#d9d9d9")])

#################################################################
#                             TELA
#################################################################
texto = ttk.Label(
    tela, text="Calculador de Curva de Descarga", 
    font=("Helvetica", 16, "bold"), 
    background="#2c6e49", foreground="white",
    anchor="center", padding=10
)
texto.grid(column=0, row=0, sticky="ew", pady=(0, 2*PAD_Y), columnspan = 2)

# Frame para os formulários
form_frame = Frame(tela)
form_frame.grid(column=0, row=2, padx=0, pady=PAD_Y, columnspan = 2)

# Option box - TIPO DE SECAO 
tipo_secao_Label = ttk.Label(tela, text="Tipo de Seção", style="TLabel")
tipo_secao_Label.grid(column=0, row=1, padx=PAD_X, pady=PAD_Y, sticky="w")
tipo_secao = StringVar(tela, value="Select an Option") 
# Chama update_form quando o valor muda
tipo_secao.trace_add("write", update_form)  
question_menu = ttk.OptionMenu(tela, tipo_secao, *LST_TIPOS_SECOES, style="TMenubutton") 
question_menu.grid(column=1, row=1, padx=PAD_X, pady=PAD_Y, sticky="e")

# formulario indenpedente do tipo de secao
El_Max_Label = ttk.Label(tela, text="Elevação máxima da estrutura", style="TLabel")
El_Max_Label.grid(column=0, row=3, padx=PAD_X, pady=PAD_Y, sticky="w")
El_Max = ttk.Entry(tela, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
El_Max.grid(column=1, row=3, padx=PAD_X, pady=PAD_Y, sticky="e")

El_Soleira_Label = ttk.Label(tela, text="Elevação da soleira do dispositivo", style="TLabel")
El_Soleira_Label.grid(column=0, row=4, padx=PAD_X, pady=PAD_Y, sticky="w")
El_Soleira = ttk.Entry(tela, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
El_Soleira.grid(column=1, row=4, padx=PAD_X, pady=PAD_Y, sticky="e")

Discretizacao_Label = ttk.Label(tela, text="Intervalo de discretização da CD", style="TLabel")
Discretizacao_Label.grid(column=0, row=5, padx=PAD_X, pady=PAD_Y, sticky="w")
Discretizacao = ttk.Entry(tela, validate="key", validatecommand=(vcmd, "%P"), style="TEntry")
Discretizacao.grid(column=1, row=5, padx=PAD_X, pady=PAD_Y, sticky="e")

# botao de calcular
button = ttk.Button(tela, text="Calcular", command=generates_response, style="TButton")
button.grid(column=0, row=6, padx=PAD_X, pady=(2*PAD_Y, 2), columnspan = 2)

# texto de feedback
exibe_msg = Label(tela)
exibe_msg.grid(column=0, row=7, padx=PAD_X, pady=PAD_Y, columnspan = 2)

# contato do desenvolvedor
autor = Label(tela, text="@github/DiasGomes", foreground="darkgray")
autor.grid(column=0, row=8, padx=5, pady=2, columnspan = 2)

tela.mainloop()