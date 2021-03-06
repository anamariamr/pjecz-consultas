import os
import tabulate
from comun.listas import Listas


class Sentencias(Listas):
    """ Sentencias """

    def alimentar(self):
        """ Alimentar la tabla con las columnas de Listas Especiales """
        super().alimentar()
        if self.alimentado == False:
            for item in self.archivos:
                # Separar .../autoridad/fecha-nnn-yyyy-nnn-yyyy-g.pdf
                archivo = os.path.basename(item.path)
                nombre = os.path.splitext(archivo)[0]
                directorio = os.path.dirname(item.path)
                carpetas = directorio.split('/')
                separados = nombre[11:].split('-') # ['nnn', 'yyyy', 'nnn', 'yyyy', 'g']
                # Renglón
                fecha = self.validar_fecha(nombre[:10])
                autoridad = self.validar_autoridad(carpetas[-1]) # Última carpeta
                if len(separados) == 5 and separados[4] == 'g':
                    p_genero = 'Sí'
                else:
                    p_genero = 'No'
                if len(separados) >= 4:
                    sentencia = f'{separados[0]}/{separados[1]}'
                    expediente = f'{separados[2]}/{separados[3]}'
                else:
                    sentencia = 'nnn/YYYY'
                    expediente = 'nnn/YYYY'
                url = self.validar_url(item.path)
                renglon = {
                    'Fecha': fecha,
                    'Juzgado/Tribunal': autoridad,
                    'P. Género': p_genero,
                    'Sentencia': sentencia,
                    'Expediente': expediente,
                    'Archivo': url,
                    }
                # Acumular en la tabla
                self.tabla.append(renglon)
            self.alimentado = True

    def __repr__(self):
        super().__repr__()
        tabla = [[
            'Fecha',
            'Juzgado/Tribunal',
            'P. Género',
            'Sentencia',
            'Expediente',
            'Archivo',
            ]]
        for renglon in self.tabla:
            tabla.append([
                renglon['Fecha'],
                renglon['Juzgado/Tribunal'],
                renglon['P. Género'],
                renglon['Sentencia'],
                renglon['Expediente'],
                renglon['Archivo'],
                ])
        salida = []
        salida.append('<Sentencias>')
        salida.append(tabulate.tabulate(tabla, headers='firstrow'))
        salida.append('Son {} archivos.'.format(len(self.archivos)))
        return('\n'.join(salida))
