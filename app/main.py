from app import pipeline
from storage import init_db

def main():
    init_db()

    perguntas = [
        "Por que reconhecer meus erros é tão difícil?",
        "Por que o ser humano falha mesmo querendo acertar?",
        "Como lidar com uma culpa profunda?",
        "Qual o sentido do sofrimento?"
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