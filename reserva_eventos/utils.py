
def obter_entrada(label, min, max):
    try:
        entrada = int(input(label))
        if entrada < min or entrada > max:
            print('INVALIDO')
            return obter_entrada(label, min, max)
    except ValueError:
        print('INVALIDO')
        return obter_entrada(label, min, max)
    
    return entrada