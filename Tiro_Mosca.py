import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import random

import st_state_patch

def check_senha(senha_str):
    """
    Confere se determinada senha tem a quantidade correta de dígitos (4), se só contém digitos
    e se não contém nenhum dígito repetido.
    """
    if (len(senha_str) != 4):
        return False
    if (not senha_str.isdigit()):
        return False

    d1,d2,d3,d4 = senha_str[0], senha_str[1], senha_str[2], senha_str[3]

    return (d1 != d2 and d1 != d3 and d1 != d4 and d2 != d3 and d2 != d4 and d3 != d4)

def calcula_moscas(palpite, senha):
    """
    Calcula quantas moscas um determinado palpite tem em uma determinada senha.
    """
    moscas = sum([palpite[d]==senha[d] for d in range(len(palpite))])
    return moscas              

def calcula_tiros(palpite, senha):
    """
    Calcula quantos tiros um determinado palpite tem em uma determinada senha.
    """
    tiros = [((senha[d] in palpite) and (senha[d]!=palpite[d])) for d in range(len(palpite))]
    tiros = sum(tiros)
    return tiros

def gera_senha():
    """
    Gera uma nova senha de 4 dígitos, contendo somente números distintos entre 0 e 9.
    """
    nova_senha=[]

    for i in range(4):
        novo_num = random.randint(0,9)
        while(novo_num in nova_senha):
            novo_num= random.randint(0,9)
        nova_senha.append(novo_num)

    senha_maquina = "".join([str(i) for i in nova_senha])

    return senha_maquina

def gera_possibilidades():
    """
    Gera todas as possíveis senhas de 4 dígitos e somente com números distintos entre 0 e 9.
    """
    possibilidades = []
    possibilidades.clear()
    for d1 in range(10):
        for d2 in range(10):
            for d3 in range(10):
                for d4 in range(10):
                    if (d1 != d2 and d1 != d3 and d1 != d4 and d2 != d3 and d2 != d4 and d3 != d4):
                        p = "".join([str(p) for p in [d1,d2,d3,d4]])
                        possibilidades.append(p)
    return possibilidades

def atualiza_possibilidades(palpite, tiros, moscas, possibilidades):
    """
    Dadas as possibilidades restantes para acertar uma senha, um novo palpite e suas moscas e tiros,
    determina quais serão as possibilidades restantes para a senha adversária.
    """
    atualizadas = []
    atualizadas.clear()

    for possibilidade in possibilidades:
        if ((calcula_tiros(possibilidade, palpite) == tiros) and (calcula_moscas(possibilidade, palpite) == moscas)):
            atualizadas.append(possibilidade)

    return atualizadas

def main():

    page = st.sidebar.selectbox("Escolha uma opção:", ['Início', 'Regras', 'Como jogar', 'Jogar contra a máquina', 'Jogar contra outra pessoa', 'Como a máquina pensa?'])
    #language = st.sidebar.selectbox("Língua/Language: ", ['Português', 'English'])
    st.sidebar.markdown('Desenvolvido por **Gustavo Domingues**.')
    st.sidebar.markdown('gustavomdom@gmail.com')


    if page == 'Início':
        image = Image.open('senha.jpg')
        st.title('Bem-vindo ao Tiro & Mosca!')
        st.subheader('Você já jogou Senha ou Mastermind? Tiro & Mosca é uma versão adaptada com números.')
        st.write('Navegue no menu ao seu lado esquerdo para escolher o modo de jogo ou aprender como jogar! .')
        st.image(image, use_column_width=True)

    elif page == '1 Jogador':

        s = st.State() # recurso para guardar informações entre execuções do Streamlit, que rodam todo código após cada evento na página

        if not s:
        #    s.senha_jogador = []
        #    s.palpites_jogador = []
        #    s.palpites_maquina = []
        #    s.palpites = []
             s.inicio = False
        #    s.history_df = pd.DataFrame(None, columns=['Vazio', 'Você', 'Acertos', 'Máquina', 'Acertos'])
        #    #s.history_df.set_index("Você")
        #    s.senha_maquina = gera_senha()
        #    s.possibilidades = gera_possibilidades()

        # print("\n\nPossibilidades: ",len(s.possibilidades), "\n\n")
     
        st.title('Tiro & Mosca - Você contra a máquina')        

        header = ['Vazio', 'Você', 'Acertos', 'Máquina', 'Acertos'] # como não tem jeito de tirar o índice, deixei ele vazio

        if not s.inicio:

            s.senha_jogador = []
            s.palpites_jogador = []
            s.palpites_maquina = []
            s.palpites = []
            s.inicio = False
            s.history_df = pd.DataFrame(None, columns= ['Vazio', 'Você', 'Acertos', 'Máquina', 'Acertos'])
            #s.history_df.set_index("Você")
            s.senha_maquina = gera_senha()
            s.possibilidades = gera_possibilidades()

            s.senha_jogador = st.text_input('Qual sua senha?', type="password") 
            if (check_senha(s.senha_jogador)):
                st.success("A sua senha foi computada.")  
                s.inicio = True  
            elif len(s.senha_jogador)>0:
                st.warning("A sua senha não é válida. Ele deve conter exatamente 4 números distintos entre 0 e 9.")

        if s.inicio:

            print("\n\nSenha maquina: " + s.senha_maquina + "\n\n")

            st.markdown(':lock: ' + s.senha_jogador) # deixa anotado a senha que a pessoa escolheu

            palpite_jogador = st.text_input('QUAL SEU PALPITE?') 

            if (check_senha(palpite_jogador)):

                mensagem_jogador = "O seu palpite " + palpite_jogador + " foi computado."
                moscas_jogador = calcula_moscas(palpite_jogador, s.senha_maquina)
                tiros_jogador = calcula_tiros(palpite_jogador, s.senha_maquina) 
                s.palpites_jogador.insert(0, [palpite_jogador, moscas_jogador, tiros_jogador])
                st.warning(mensagem_jogador)
                

                posicao_aleatoria = random.randint(0,len(s.possibilidades)-1)
                palpite_maquina = s.possibilidades[posicao_aleatoria]
                #print("\n\nPalpite maquina: " + palpite_maquina + "\n\n")
                #print("Senha jogador: ", s.senha_jogador)
                moscas_maquina = calcula_moscas(palpite_maquina, s.senha_jogador)
                #print("\nMoscas: ", moscas_maquina)
                tiros_maquina = calcula_tiros(palpite_maquina, s.senha_jogador)
                #print("\nTiros: ", tiros_maquina)
                s.palpites_maquina.insert(0, [palpite_maquina, moscas_maquina, tiros_maquina])
                mensagem_maquina = "O palpite da máquina foi: " + palpite_maquina + "."
                st.error(mensagem_maquina)

                s.palpites.insert(0, ['', palpite_jogador, str(moscas_jogador)+'M '+str(tiros_jogador)+'T', palpite_maquina, str(moscas_maquina) + 'M ' + str(tiros_maquina) + 'T'])
                s.history_df = pd.DataFrame(s.palpites, columns=header)

                s.possibilidades = atualiza_possibilidades(palpite_maquina, tiros_maquina, moscas_maquina, s.possibilidades)
                
                (s.history_df).set_index('Vazio', inplace=True)
                #(s.history_df).index.name = 'Você'

                if (palpite_maquina == s.senha_jogador) and (palpite_jogador == s.senha_maquina):
                    st.balloons()
                    st.success("VOCÊ E A MÁQUINA EMPATARAM!")
                    #st.table(s.history_df)
                    s.inicio = False    

                elif (palpite_jogador == s.senha_maquina):
                    st.balloons()
                    st.success("PARABÉNS! VOCÊ VENCEU!")
                    #st.table(s.history_df)
                    s.inicio = False 

                elif (palpite_maquina == s.senha_jogador):
                    st.balloons()
                    st.success("QUE PENA... A MÁQUINA VENCEU! A SENHA DELA ERA: " + s.senha_maquina)
                    #st.table(s.history_df)
                    s.inicio = False 

            elif len(palpite_jogador)>0:
                st.warning("O seu palpite não é válido. Ele deve conter exatamente 4 números entre 0 e 9 distintos.")

                
            st.table(s.history_df)
            st.markdown('**T** = Tiros, **M** = Moscas.')
                
    elif page == '2 Jogadores':
        st.title('Em breve.')

    elif page == 'Regras':
        st.title('Regras')
        st.header('Qual o objetivo?')
        st.markdown('Descobrir a senha do adversário antes que ele descubra a sua.')
        st.header('Mas como?')
        st.markdown('Através de palpites! Cada rodada os jogadores darão seus palpites e receberão o feedback de quantos tiros e quantas moscas acertaram.')
        st.header('Tiros??')
        st.markdown('Cada tiro (T) é um dígito existente no palpite e na senha adversária, mas em **posições diferentes**.')
        st.markdown('**Exemplo:**')
        st.markdown('Palpite: 1234')
        st.markdown('Senha do adversário: 6543')
        st.markdown('Tiros: 2 (o 3 e o 4)')
        st.header('Moscas??')
        st.markdown('Cada mosca (M) é um dígito existente no palpite e na senha adversária em **posições idênticas**.')
        st.markdown('**Exemplo:**')
        st.markdown('Palpite: 1234')
        st.markdown('Senha do adversário: 1289')
        st.markdown('Moscas: 2 (o 1 e o 2)')
        st.header('Como são as senhas?')
        st.markdown('As senhas contém quatro dígitos numéricos **distintos**, sendo cada um dos dígitos um número entre 0 e 9.')
        st.markdown('Exemplos **corretos**: 1234, 6789, 1857, 0172.')
        st.markdown('Exemplos **incorretos**: 123456, 6689, A857, @#12.')
        
     
    elif page == 'Como jogar':
        st.title('Como jogar') 
        st.header('Modo 1 Jogador')
        st.subheader('Você contra a máquina')
        st.markdown('1. Selecione a opção __1 Jogador__ no menu do seu lado esquerdo.')
        image_11 = Image.open('ComoJogar_J1_1.png')
        st.image(image_11, use_column_width=True)
        st.markdown('2. Preencha o campo de senha com um valor válido e aperte ENTER (ou correspondente).')
        image_12 = Image.open('ComoJogar_J1_2.png')
        st.image(image_12, use_column_width=True)
        st.markdown('3. Neste momento a máquina já criou a senha dela e o resultado de Moscas (M) e Tiros (T) de ambos serão computados automaticamente ao mesmo tempo.')
        st.markdown('4. Digite seu palpite no campo apresentado e aperte ENTER (ou correspondete).')
        image_14= Image.open('ComoJogar_J1_4.png')
        st.image(image_14 , use_column_width=True)
        st.markdown('5. Acompanhe os resultados dos seus palpites e da máquina na tabela apresentada.')
        image_15 = Image.open('ComoJogar_J1_5.png')
        st.image(image_15, use_column_width=True)
        st.markdown('6. Quando alguém acertar a senha adversária o jogo se encerra (com possibildade de empate).')
        image_16 = Image.open('ComoJogar_J1_6.png')
        st.image(image_16 , use_column_width=True)
        st.markdown('7. Para começar uma nova partida você pode recarregar a página ou inserir qualquer outro palpite e apertar ENTER.')
        st.header('Modo 2 Jogadores')
        st.subheader('Você contra outra pessoa utilizando o mesmo dispositivo.')
        st.markdown('Em breve.')   

    elif page == "Sobre o algoritmo":
        st.title('Em breve')



if __name__ == '__main__':
    main()