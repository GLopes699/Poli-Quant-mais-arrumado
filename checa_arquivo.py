import pandas as pd
import copy


def checa_arquivo(arquivo):
   
    df_ibov = pd.read_csv("ibov_2010_2024.csv")

    if arquivo == "N":
        #Lê o CSV das ações e exclui todas as que não estavam durante o período completo e cria um novo CSV formatado, para evitar esse processo no futuro
        csv_dos_precos = input("Por favor, escreva o nome do arquivo csv com os preços das ações: ")
        df_acoes = pd.read_csv(csv_dos_precos)
        print("Exlcuindo as ações que não estavam presentes na Bolsa durante o período completo, por favor aguarde...")
        df_acoes=df_acoes.fillna("0")
        index=list(df_acoes.index)
        nome_acoes=list(df_acoes.columns)
        nome_acoes=nome_acoes[1:]
        nome_acoes_atualizado=copy.deepcopy(nome_acoes)
        for x in nome_acoes:
            df_acoes_temp=df_acoes.filter(items=[x],axis=1)
            excluido = False
            for t in index:
                if df_acoes_temp.loc[t].values[0] == "0" and excluido == False:
                    df_acoes=df_acoes.drop(columns=[x])
                    nome_acoes_atualizado.remove(x)
                    excluido = True
        df_acoes.loc[5, "BBAS3.SA"] = 5.591660976409912
        print("Processo concluído, obrigado por aguardar!")
        df_acoes.to_csv("precos_acoes_b3_2010_2024_formatado.csv", index = False)
        print("CSV já formatado possui o nome 'precos_acoes_b3_2010_2024_formatado.csv'")

    else:
        #Lê os CSVs das ações já formatados
        df_acoes = pd.read_csv("precos_acoes_b3_2010_2024_formatado.csv")
        index=list(df_acoes.index)
        nome_acoes_atualizado=list(df_acoes.columns)

    return df_acoes, df_ibov, nome_acoes_atualizado
