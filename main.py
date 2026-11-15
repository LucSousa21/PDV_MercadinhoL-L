from src.views.interface import iniciar_pdv
from src.database.criar_banco import criar_banco


def main():
    criar_banco()
    iniciar_pdv()
    
    


if __name__ == "__main__":
    main()