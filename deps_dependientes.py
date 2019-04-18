import os
import sys

def listado_dependencias(paquete):
    paquetes = []
    fin = os.popen('apt-cache depends {0}'.format(paquete))
    for l in fin:
        linea = l.strip()
        if linea.startswith('Depende:')  or linea.startswith('|Depende') or linea.startswith('Recomienda:') or linea.startswith('|Recomienda'):
            pac = linea.replace('Depende:','')
            pac = pac.replace('Recomienda:','')
            pac = pac.replace('|','')
            pac = pac.replace('<','')
            pac = pac.replace('>','')
            pac = pac.strip()
            paquetes.append(pac)
    fin.close()
    return paquetes

paquetes_todos = []
paquetes_padres = {}

def listado_completo(paquete):
    if paquete in paquetes_todos and paquete != None:
        return []
    paquetes_todos.append(paquete)
    print('    Se incluye {0}'.format(paquete))
    paquetes = listado_dependencias(paquete)
    for p in paquetes:
        print(p)
        if not p in paquetes_padres.keys():
            paquetes_padres[p] = paquete
        ps = listado_completo(p)
        #for pk in ps:
        #    if not pk in paquetes_todos:
        #        print('Se incluye {0}'.format(pk))
        #        paquetes_todos.append(pk)
    return paquetes_todos
        


l = listado_completo(sys.argv[1])
l.sort()
print(l)
print(paquetes_padres)
fout = open('salida.txt', 'w')
for p in paquetes_padres.keys():
    fout.write('{0} : {1}\n'.format(p, paquetes_padres[p]))
fout.close()
