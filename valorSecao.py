import tkinter as tk
from tkinter import messagebox
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def dividir_em_sessoes(valor, sessao_maxima, sessoes_por_dia):
    data_atual = datetime.date.today()
    primeiro_dia_mes = datetime.date(data_atual.year, data_atual.month, 1)
    ultimo_dia_mes = datetime.date(data_atual.year, data_atual.month + 1, 1) - datetime.timedelta(days=1)
    dias_mes = (ultimo_dia_mes - primeiro_dia_mes).days + 1

    valor_restante = valor
    sessoes_restantes = valor // sessao_maxima
    dia = 1
    soma_sessoes = 0
    valor_total_sessoes = 0
    result = ""

    while sessoes_restantes > 0 and dia <= dias_mes:
        data_atual = primeiro_dia_mes + datetime.timedelta(days=dia-1)

        if data_atual.weekday() != 6:  # Verifica se não é domingo
            sessoes_no_dia = min(sessoes_restantes, sessoes_por_dia)
            result += f"{data_atual.strftime('%d/%m')}: {sessoes_no_dia} sessões\n"

            soma_sessoes += sessoes_no_dia  # Adiciona o número de sessões à soma total
            valor_total_sessoes += sessoes_no_dia * sessao_maxima  # Calcula o valor total das sessões

            valor_restante -= sessoes_no_dia * sessao_maxima
            sessoes_restantes = valor_restante // sessao_maxima

        dia += 1

    result += f"\nResultado final: Total de {soma_sessoes} sessões\n"
    result += f"Valor total das sessões: R${valor_total_sessoes}"

    return result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    valor_input = int(request.json["valor"])
    sessao_maxima_input = int(request.json["sessao_maxima"])
    sessoes_por_dia_input = int(request.json["sessoes_por_dia"])

    resultado = dividir_em_sessoes(valor_input, sessao_maxima_input, sessoes_por_dia_input)

    return jsonify(resultado)

def run_gui():
    # Criar a janela principal
    window = tk.Tk()
    window.title("Dividir em Sessões")

    # Criar os rótulos e campos de entrada
    valor_label = tk.Label(window, text="Digite um valor:")
    valor_label.pack()
    valor_entry = tk.Entry(window)
    valor_entry.pack()

    sessao_maxima_label = tk.Label(window, text="Digite o valor máximo da sessão:")
    sessao_maxima_label.pack()
    sessao_maxima_entry = tk.Entry(window)
    sessao_maxima_entry.pack()

    sessoes_por_dia_label = tk.Label(window, text="Digite o máximo de sessões por dia:")
    sessoes_por_dia_label.pack()
    sessoes_por_dia_entry = tk.Entry(window)
    sessoes_por_dia_entry.pack()

    def calcular():
        valor_input = int(valor_entry.get())
        sessao_maxima_input = int(sessao_maxima_entry.get())
        sessoes_por_dia_input = int(sessoes_por_dia_entry.get())

        resultado = dividir_em_sessoes(valor_input, sessao_maxima_input, sessoes_por_dia_input)
        messagebox.showinfo("Resultado", resultado)

    calcular_button = tk.Button(window, text="Calcular", command=calcular)
    calcular_button.pack()

    # Iniciar a execução da janela
    window.mainloop()

if __name__ == "__main__":
    app.run()
