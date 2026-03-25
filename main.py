from agents import pipeline
from storage import init_db

def main():
    init_db()

    perguntas = [
        "Por que reconhecer meus erros é tão difícil segundo a Bíblia?",
        "O que pessoas maduras na Bíblia entenderam sobre o tempo e a vida?",
        "Como a Bíblia descreve o processo de autoavaliação verdadeira?",
        "Qual a diferença entre remorso e arrependimento nas Escrituras?"
    ]

    for p in perguntas:
        print("\n" + "="*60)
        print("Pergunta:", p)

        resposta = pipeline(p)

        print("\nResposta Final:\n")
        print(resposta)
        print("\n" + "="*60)


if __name__ == "__main__":
    main()