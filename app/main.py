from app import pipeline
from storage import init_db, aplicar_decay

def main():
    init_db()

    perguntas = [
        "Se o tempo é uma dimensão aparentemente irreversível e a memória, uma construção falível, em que sentido o 'eu' que promete hoje é o mesmo que deve cumprir amanhã, e o que obriga essa entidade fugidia à fidelidade?",
        "Como justificar a exigência de perdoar o imperdoável — o ato que viola toda medida humana de reparação — sem transformar o perdão em cumplicidade ou em esquecimento covarde?",
        "Se toda escolha elimina infinitas possibilidades, o luto pelo não vivido é um mero capricho ou um testemunho de que a finitude, embora real, não é desejada pela própria estrutura da vontade?",
        "Por que a contemplação da natureza — um céu estrelado, uma flor silvestre — evoca, em certos momentos, uma paz que independe da resolução de qualquer problema humano, como se a existência pudesse ser justificada apenas por sua beleza?",
        "Se minha consciência é um fenômeno emergentemente cerebral, como explicar a capacidade de negar meu próprio prazer, sacrificar meu bem-estar ou mesmo aniquilar minha vida por uma ideia, um valor ou outra pessoa?",
        "O encontro com o 'outro' — em seu rosto, em sua vulnerabilidade — impõe uma ética anterior a qualquer contrato social. O que, na constituição desse encontro, me torna responsável por um sofrimento que eu não causei?",
        "Se buscamos a felicidade, mas organizamos a sociedade em torno do trabalho, da produtividade e do adiamento do prazer, a infelicidade é um acidente ou uma estrutura necessária da vida civilizada?",
        "Como distinguir entre a humildade autêntica, que reconhece a própria contingência, e a humilhação imposta, que destrói o valor do sujeito? Há uma linha ontológica entre reconhecer-se pequeno e ser tratado como lixo?",
        "Se a tecnologia promete superar os limites biológicos da doença, do envelhecimento e até da morte, o que restará da condição humana quando o sofrimento e a finitude forem opcionais? A morte é um problema a resolver ou uma condição de possibilidade do sentido?",
        "Por que a ironia — a capacidade de dizer o contrário do que se pensa, de suspender o sentido — é uma forma privilegiada de verdade em certos contextos? O que isso revela sobre a distância constitutiva entre a linguagem e o real?",
        "Se o silêncio é o horizonte de toda fala, o que há de mais verdadeiro no ser humano — aquilo que ele consegue articular ou aquilo que o deixa irremediavelmente mudo?",
        "Como avaliar se a esperança é uma virtude ou uma armadilha? Há sofrimentos tão extremos em que a esperança prolonga a tortura, e resignações tão dignas em que o abandono de toda esperança é o último ato de liberdade?",
        "A saudade — esse desejo por algo que não tem nome ou que talvez nunca tenha existido — é um defeito da memória ou a prova de que fomos feitos para uma plenitude que o tempo nos nega?",
        "Se o corpo é o veículo do eu, mas também sua prisão (adoece, envelhece, trai), qual a relação justa que se deve ter com ele: a disciplina ascética, o culto hedonista ou a aceitação compassiva de sua fragilidade?",
        "Por que a infância retorna na memória adulta como uma 'pátria perdida', mesmo para aqueles que não tiveram uma infância feliz? O que esse arquétipo revela sobre a estrutura do tempo e da perda?",
        "Se a razão é nossa ferramenta mais confiável, como explicar que as decisões mais importantes da vida — casar, ter um filho, escolher uma vocação — são tomadas por saltos irracionais, por paixões e por riscos incalculáveis?",
        "O que significa 'dar a vida por algo'? Se a vida é tudo o que temos, que tipo de realidade (pátria, ideia, pessoa) deve ter um valor maior do que o próprio existir para que o sacrifício não seja insano, mas sublime?",
        "Se todo conhecimento é interpretação, como evitar o relativismo absoluto, no qual todas as visões de mundo seriam igualmente válidas e, portanto, igualmente insignificantes?",
        "A consciência da própria insignificância cósmica — um ser humano é menor que um grão de poeira na vastidão do universo — deve gerar niilismo ou, paradoxalmente, alívio e liberdade diante da ausência de um espectador cósmico?",
        "Por que o tédio — a experiência do tempo vazio, da falta de interesse por tudo — é uma das experiências mais dolorosas e temidas, revelando que o ser humano não suporta o puro existir sem um 'para quê'?",
        "Se o riso frequentemente emerge da quebra de uma expectativa séria ou da exposição de uma incongruência, o que a comédia nos ensina sobre a fragilidade de todas as nossas certezas e hierarquias sociais?",
        "Como conciliar a busca humana por autonomia — ser senhor de si mesmo — com a experiência universal de se apaixonar, onde se perde o controle, onde se é 'tomado' por algo ou alguém que não se escolheu?",
        "Se a verdade ofende, fere e desestabiliza, e a mentira acolhe e conforta, qual é o fundamento para preferir a verdade, a não ser uma aposta irracional em seu valor mesmo quando ela destrói a felicidade?",
        "O que significa 'crescer ou 'amadurecer'? É aprender a negociar com a realidade e reduzir os ideais, ou é encontrar meios mais autênticos e potentes de perseguir aquilo que, desde o início, nos importava?",
        "Se os sonhos são produções do cérebro sem finalidade adaptativa clara, por que eles carregam, para o sujeito, uma força existencial frequentemente maior do que a realidade diurna? O que é, afinal, o 'real'?",
        "Como olhar para a própria história de vida não como uma sequência de acidentes ou um script determinado, mas como uma narrativa da qual se é autor, sem cair na ilusão de que o controle foi total?",
        "A capacidade de suportar a dúvida sem respostas imediatas, de viver na incerteza radical — isso é uma fraqueza do intelecto ou a maior prova de coragem e maturidade espiritual?",
        "Se o trabalho dá sentido à vida de muitos, mas frequentemente a reduz a um ciclo de repetição e exaustão, o trabalho é uma vocação ontológica do ser humano ou um desvio histórico que precisa ser superado?",
        "Por que o ser humano constrói ruínas, mausoléus e monumentos? O que a necessidade de deixar uma marca na pedra, mesmo sabendo que a pedra também se desfará, diz sobre a relação entre o desejo de eternidade e a aceitação da transitoriedade?",
        "Se o amor é, em parte, um fenômeno químico, como explicar sua permanência para além do prazer, na doença, na decrepitude e na perda da capacidade de troca — um amor que continua mesmo quando nada 'ganha' com isso?",
        "Como é possível a experiência de um 'presente' puro — aquele instante em que a angústia do futuro e o peso do passado desaparecem — e o que essa experiência rara revela sobre a natureza ilusória ou redentora do tempo?",
        "Se a justiça é um conceito humano, por que sentimos revolta diante de um terremoto que mata crianças? A natureza é injusta ou nossa projeção de justiça sobre o mundo natural é que é o verdadeiro erro?",
        "Por que a narrativa da 'redenção' — a ideia de que alguém pode se tornar melhor, de que o passado não dita o futuro — é tão poderosa em todas as culturas, mesmo na ausência de evidências empíricas de que as pessoas mudem radicalmente?",
        "O conforto material e a segurança eliminam a angústia existencial ou apenas a adiam e a tornam mais surda, como um zumbido de fundo que só é percebido no silêncio da noite?",
        "Se a linguagem é uma prisão (pois nos força a categorizar um fluxo contínuo de realidade), a poesia seria a chave da cela ou apenas um modo mais sofisticado de cantar a própria prisão?",
        "O que significa 'perdoar a si mesmo'? Se a consciência é uma instância interna, quem é o juiz e quem é o réu? E quem autorizou esse tribunal interior a existir e a nos condenar?",
        "Se a racionalidade econômica reduziu o mundo a recursos e o trabalho a fator de produção, a nostalgia do artesão — que fazia uma coisa inteira com as próprias mãos — é um saudosismo romântico ou a memória de uma relação mais autêntica com o existir?",
        "Por que a experiência do sublime — o terror diante da vastidão do oceano ou da altura da montanha — é também fonte de prazer? O que há de libertador em ser reduzido a nada pela escala do real?",
        "Se a história humana é um ciclo de guerras e pazes, cada geração jura que 'nunca mais' e a geração seguinte repete os mesmos erros. Essa repetição é um fracasso da memória ou uma condição trágica da natureza humana?",
        "No fim da vida, quando a energia vital se esvai, o que pesa mais: o saldo das ações realizadas ou a qualidade da atenção que se foi capaz de dar ao que realmente importava? E o que, afinal, realmente importava?"
    ]

    cont = 0

    for p in perguntas:
        cont += 1
        print("\n" + "="*60)
        print("Pergunta:", p)

        resposta = pipeline(p)

        print("\nResposta Final:\n")
        print(resposta)
        print("\n" + "="*60)
        if cont % 5 == 0:
            aplicar_decay()
            
if __name__ == "__main__":
    main()