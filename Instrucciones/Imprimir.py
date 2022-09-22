from Abstracta.Instruccion import Instruccion
from Entorno.Entorno import Entorno
from Enum.TipoPrimitivo import TipoPrimitivo
from Entorno.Valor import Valor


class Imprimir(Instruccion):
    def __init__(self, fila, expresiones):
        super().__init__(fila)
        self.expresiones = expresiones

    def ejecutar(self, entorno: Entorno):
        if not self.expresiones:
            self.generador.agregarSaltoLinea()
        else:
            caracteres = []

            for expres in self.expresiones:
                print(expres.generador)
                expres.generador = self.generador
                caracteres.append(expres.ejecutar(entorno))

            tmp2 = self.generador.nuevoTemp()
            self.generador.agregarExpresion(tmp2, caracteres[0].valor, "", "")
            tmp3 = self.generador.nuevoTemp()
            self.generador.agregarExpresion(tmp3, "0", "", "")
            tmp4 = self.generador.nuevoTemp()
            self.generador.obtenerValorHeap(tmp4, tmp2)

            lbl1 = self.generador.nuevoLabel()
            lbl2 = self.generador.nuevoLabel()
            lbl3 = self.generador.nuevoLabel()
            lbl4 = self.generador.nuevoLabel()

            self.generador.agregarLabel(lbl1)
            self.generador.agregarIf(tmp4, "-1", "==", lbl2)
            self.generador.agregarIf(tmp4, "-2", "!=", lbl3)
            self.generador.agregarExpresion(tmp3, tmp3, "1", "+")
            self.generador.agregarGoto(lbl4)
            self.generador.agregarLabel(lbl3)
            self.generador.agregarPrintf("c", "(int)" + tmp4)
            self.generador.agregarExpresion(tmp2, tmp2, "1", "+")
            self.generador.obtenerValorHeap(tmp4, tmp2)
            self.generador.agregarGoto(lbl1)

            self.generador.agregarLabel(lbl4)
            labels = []
            for next in range(1, len(caracteres)):
                lbl = self.generador.nuevoLabel()
                labels.append(lbl)
                self.generador.agregarIf(tmp3, str(next), "==", lbl)

            for next in range(1, len(caracteres)):
                self.generador.agregarLabel(labels[next - 1])
                if caracteres[next].tipo == TipoPrimitivo.I64:
                    self.generador.agregarPrintf("d", caracteres[next].valor)
                    self.generador.agregarExpresion(tmp2, tmp2, "1", "+")
                    self.generador.obtenerValorHeap(tmp4, tmp2)
                    self.generador.agregarGoto(lbl1)

                elif caracteres[next].tipo == TipoPrimitivo.STR:
                    tmp5 = self.generador.nuevoTemp()
                    self.generador.agregarExpresion(tmp5, caracteres[next].valor, "", "")
                    tmp6 = self.generador.nuevoTemp()
                    self.generador.obtenerValorHeap(tmp6, tmp5)
                    lbl7 = self.generador.nuevoLabel()
                    self.generador.agregarLabel(lbl7)
                    lbl8 = self.generador.nuevoLabel()
                    self.generador.agregarIf(tmp6, "-1", "!=", lbl8)
                    self.generador.agregarExpresion(tmp2, tmp2, "1", "+")
                    self.generador.obtenerValorHeap(tmp4, tmp2)
                    self.generador.agregarGoto(lbl1)
                    self.generador.agregarLabel(lbl8)
                    self.generador.agregarPrintf("c", "(int)" + tmp6)
                    self.generador.agregarExpresion(tmp5, tmp5, "1", "+")
                    self.generador.obtenerValorHeap(tmp6, tmp5)
                    self.generador.agregarGoto(lbl7)

            self.generador.agregarLabel(lbl2)
