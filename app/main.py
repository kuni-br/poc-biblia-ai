from app import pipeline
from storage import init_db, aplicar_decay

def main():
    init_db()

    perguntas = [
        "Se a existência humana é finita e contingente em um universo aparentemente indiferente, em que fundamento último pode o ser humano ancorar um propósito que não seja mera projeção subjetiva ou construção cultural efêmera?",
        "Como explicar a experiência universal de um imperativo ético interior — aquilo que chamamos de 'dever ser' — se a moralidade fosse apenas produto de evolução biológica ou convenção social, sem referência a uma ordem transcendente?",
        "Se tudo no corpo e na mente está em constante mudança, o que garante a unidade e a persistência do 'eu' ao longo do tempo, e como essa identidade pode ser preservada diante da inevitabilidade da dissolução física?",
        "Se somos condicionados por fatores biológicos, históricos e psicológicos, em que sentido podemos falar de liberdade autêntica? E se somos livres, como assumir a responsabilidade radical por escolhas cujas consequências ultrapassam nossa compreensão?",
        "Como conciliar a experiência do sofrimento que atinge indiscriminadamente justos e injustos com a aspiração humana por justiça, sentido e ordem cósmica, sem recorrer a explicações simplistas ou fatalistas?",
        "Por que o ser humano, mesmo ao alcançar seus objetivos mais profundos, continua experimentando uma nostalgia ou anseio por algo que nenhuma realização finita parece saciar plenamente?",
        "Se toda compreensão humana é mediada por linguagem limitada e perspectivas históricas, como acessar uma verdade que seja universal, objetiva e capaz de orientar a existência de forma confiável?",
        "Por que a experiência de ser verdadeiramente visto, conhecido e aceito em nossa totalidade — com luzes e sombras — parece ser ao mesmo tempo uma necessidade profunda e uma conquista rara na condição humana?",
        "Como interpretar o impulso humano de buscar o infinito, o eterno e o absoluto — expresso na arte, na filosofia, no amor e na contemplação — se a consciência humana estiver confinada a uma existência temporal e material?",
        "Se a vida é marcada pelo sofrimento e pela finitude, qual é o propósito real de existir?",
        "Diante da imensidão do universo e do caos aparente da história, como posso ter certeza de que minha existência individual tem algum valor ou significado?",
        "Se sou moldado por minha genética, minha história e meu ambiente, até que ponto sou verdadeiramente livre? Existe algo em mim que não seja determinado por forças externas?",
        "Se a morte é o fim inevitável, o que torna um ato de sacrifício ou de amor “maior” do que um ato de egoísmo, se ambos desaparecerão no esquecimento?",
        "Se Deus é todo-poderoso e totalmente bom, como conciliar Sua existência com a realidade do mal e da injustiça que assolam os inocentes?",
        "O que constitui a identidade verdadeira de um ser humano? Sou o que faço, o que penso, o que sinto ou algo mais profundo e imutável?",
        "Como posso distinguir entre uma verdade absoluta e aquilo que são apenas construções sociais ou preferências pessoais, especialmente em questões de moral e propósito?",
        "O amor é apenas um instinto biológico para a preservação da espécie e um jogo de recompensas químicas no cérebro, ou ele aponta para algo metafísico e transcendente?",
        "Diante da certeza do envelhecimento, da perda das capacidades e do declínio, existe esperança que não seja mero autoengano ou conformismo estoico?",
        "Se o universo emergiu do nada — ou de algo que ainda não era nada —, o que confere ao existente a qualidade de ser em vez de simplesmente não ser? Há uma intencionalidade anterior à matéria?",
        "Por que o ser humano, diante de toda a evidência de sua fragilidade biológica e contingência histórica, carrega em si uma intuição quase universal de que possui valor intrínseco — não derivado de utilidade, beleza ou poder?",
        "De onde provém o senso de culpa genuína — aquela que persiste mesmo quando nenhuma testemunha existe, nenhuma lei foi violada e nenhuma consequência social é temida? O que ele aponta?",
        "Por que toda satisfação humana é estruturalmente provisória? Toda posse, relação, conquista ou prazer parece conter em si mesma a semente de sua própria insuficiência. O desejo é um defeito ou uma seta?",
        "Se a morte é a dissolução total do sujeito, por que ela é vivenciada como escândalo e não como simples dado neutro? De onde vem a resistência ontológica ao fim de si mesmo?",
        "A linguagem não apenas descreve a realidade — ela a articula, nomeia e, em certo sentido, a convoca à existência para o sujeito. O que precede a linguagem? Existe pensamento antes da palavra, ou há uma Palavra anterior a todo pensamento?",
        "O perdão genuíno — aquele que não exige reparação, que absorve o dano sem transferi-lo — parece violar a lógica da causalidade e da justiça retributiva. Como é possível que tal ato exista? O que ele pressupõe sobre a natureza da realidade?",
        "A experiência estética intensa — diante de uma paisagem, de uma obra ou de um rosto — frequentemente provoca algo que excede o prazer sensorial: uma espécie de reconhecimento, como se a beleza fosse memória de algo. De onde vem essa sensação de familiaridade com o sublime?",
        "Nenhum sujeito pode ser reduzido à sua descrição objetiva. O outro me escapa sempre. Existe, porém, uma forma de conhecimento que acessa o interior de um ser sem objetificá-lo — um conhecimento por amor, e não por análise? E quem seria capaz de conhecer assim, plenamente?",
        "O ser humano é o único ente que sabe que vai morrer — e que, sabendo disso, ainda projeta, ama, constrói e dá sentido. Essa capacidade de agir como se o tempo não fosse o limite último sugere uma relação paradoxal com a eternidade. O que isso implica sobre a natureza da consciência e sua origem?",
        "Se o universo é o resultado de processos físicos aleatórios e impessoais, por que a mente humana possui uma busca incessante por propósito e significado que transcende a mera sobrevivência biológica?",
        "Como podemos encontrar uma justificativa lógica ou um valor intrínseco para o sofrimento humano, especialmente quando ele atinge aqueles que parecem não o merecer sob nenhuma ótica ética?",
        "A distinção entre o 'bem e o 'mal é apenas uma convenção social evolutiva para garantir a coesão do grupo, ou existe um padrão objetivo de justiça que permanece válido independentemente da cultura ou da época?",
        "A consciência da nossa própria morte torna todas as nossas conquistas inerentemente absurdas, ou a brevidade da vida é, de alguma forma, o que confere valor e peso às nossas escolhas?",
        "Somos os arquitetos soberanos do nosso destino, responsáveis por cada falha e sucesso, ou somos apenas passageiros de um determinismo biológico e ambiental complexo?",
        "Por que o ser humano experimenta uma sensação recorrente de 'saudade de algo desconhecido' ou um vazio que nenhuma posse material, relacionamento ou prazer sensorial parece ser capaz de preencher plenamente?",
        "A complexidade e a inteligibilidade do universo sugerem uma estrutura lógica subjacente que podemos descobrir, ou estamos apenas projetando padrões humanos em um caos desprovido de sentido?",
        "Como uma pessoa pode lidar com o peso psicológico de suas falhas passadas e alcançar uma sensação real de renovação sem recorrer ao autoengano ou à indiferença moral?",
        "O sacrifício pessoal por outro indivíduo, sem expectativa de retorno, é uma anomalia biológica ou a expressão mais alta de uma realidade que opera acima das leis da seleção natural?"
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