from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
# Chave secreta necessária para usar sessões (pode ser qualquer string)
app.secret_key = 'sua-chave-secreta-muito-segura'

opcoes = ["pedra", "papel", "tesoura"]

# Rota principal: mostra a tela de início ou o jogo
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Salva o nome do jogador na sessão e inicia o placar
        session['nome_jogador'] = request.form['nome']
        session['vitorias_jogador'] = 0
        session['vitorias_computador'] = 0
        session['rodadas'] = 0
        return redirect(url_for('index'))

    # Se o jogador já inseriu o nome, mostra a tela do jogo
    if 'nome_jogador' in session:
        # CORREÇÃO APLICADA AQUI:
        # Passamos 'vencedor=None' para evitar o erro na primeira vez que a página carrega.
        return render_template('index.html', vencedor=None)
    
    # Se não, mostra a tela para inserir o nome
    return render_template('login.html')

# Rota para processar a jogada
@app.route('/play', methods=['POST'])
def play():
    escolha_jogador = request.form['choice']
    escolha_computador = random.choice(opcoes)

    vencedor = ""
    # Lógica do jogo
    if escolha_jogador == escolha_computador:
        vencedor = "Empate"
    elif (escolha_jogador == "pedra" and escolha_computador == "tesoura") or \
         (escolha_jogador == "tesoura" and escolha_computador == "papel") or \
         (escolha_jogador == "papel" and escolha_computador == "pedra"):
        vencedor = session['nome_jogador']
        session['vitorias_jogador'] += 1
    else:
        vencedor = "Computador"
        session['vitorias_computador'] += 1
    
    session['rodadas'] += 1
    
    # Renderiza a página novamente, mas agora com os resultados da jogada
    return render_template('index.html', 
                           player_choice=escolha_jogador,
                           computer_choice=escolha_computador,
                           vencedor=vencedor)

# Rota para reiniciar o jogo
@app.route('/reset')
def reset():
    # Limpa os dados da sessão para começar de novo
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)