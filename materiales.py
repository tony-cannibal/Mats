

class Materiales:
    todos = {}
    def __init__(self, area, codigo, cantidad=0, pkg=0, cantidad_pkg=0, pkg_entregado=0):

        self.area = area
        self.codigo = codigo
        self.cantidad = cantidad
        self.pkg = pkg
        self.cantidad_pkg = cantidad_pkg
        self.pkg_entregado = pkg_entregado
        self.cantidad_entregada = self.pkg * self.pkg_entregado
        
        # Append all Instances of the Class to Dictionary
        Materiales.todos[f"{self.area}{self.codigo}"] = self

    def esta_excedido(self):
        if  self.pkg_entregado >= self.cantidad_pkg:
            print('El material esta excedido')
            return True
        else:
            print('El material no esta excedido')
            return False

    def entregar_material(self):
        if self.esta_excedido() == True:
            print('El material esta excedido')
            print('No se puede entregar')
        else:
            self.pkg_entregado += 1

    def __repr__(self):
        return f"area: {self.area}, codigo: {self.codigo}, cantidad:{self.cantidad}, pkg: {self.pkg}, pkg_entregado: {self.pkg_entregado}"


terminal = Materiales('m1', 'tkt', 3000, 1500, 2, 0)
terminal_2 = Materiales('m1', 'tyr', 4000, 2000, 2, 0)

print(terminal.pkg_entregado)
terminal.entregar_material()
print(terminal.pkg_entregado)

