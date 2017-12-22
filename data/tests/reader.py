from data.lib.impuestos_internos import ImpuestosInternosHelper

class Reader():
    def __init__(self, file):
        self.file = open(file, 'r')
        self.impuestos = ImpuestosInternosHelper()

    def generate_test(self):
        lines = self.file.readlines()
        lines.pop(0)
        case_result = 0
        for line in lines:
            line = line.split('|')
            codigo_control = r.impuestos.generar_codigo_control(
                line[0],
                line[1],
                line[2],
                line[3],
                line[4],
                line[5])
            result = line[10]==codigo_control
            if result == True:
                case_result = case_result + 1
            print('Codigo impuestos: %s' % line[10])
            print('Codigo generado: %s' % codigo_control)
            print('=== %s ===' % result)
            print('================================================')
            print('\n')
        print('%s casos validados de %s' % (case_result, len(lines)))
if __name__ == '__main__':
    r = Reader('../data/casos.txt')
    r.generate_test()