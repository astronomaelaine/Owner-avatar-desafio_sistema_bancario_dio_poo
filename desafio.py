class UsuarioTelefone:
    def __init__(self, nome, telefone, plano):
        self._nome = nome
        self._telefone = telefone
        self._plano = plano

    @property
    def nome(self):
        return self._nome

    @property
    def telefone(self):
        return self._telefone

    @property
    def plano(self):
        return self._plano

    def __str__(self):
        return f"Usuário {self.nome} criado com sucesso."

# Entrada:
nome = input()
numero = input()
plano = input()
# TODO: Crie um novo objeto `UsuarioTelefone` com os dados fornecidos:

usuario = UsuarioTelefone(nome, numero, plano)

print(usuario.__str__())