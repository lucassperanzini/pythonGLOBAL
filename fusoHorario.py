from datetime import datetime
import pytz

def converter_fuso_horario(data_hora_original, fuso_horario_original, fuso_horario_destino):
    # Criar um objeto datetime a partir da string data_hora_original
    data_hora = datetime.strptime(data_hora_original, '%Y-%m-%dT%H:%M:%S')
    
    # Definir o fuso horário original
    fuso_original = pytz.timezone(fuso_horario_original)
    data_hora_com_fuso = fuso_original.localize(data_hora)

    # Converter para o fuso horário de destino
    fuso_destino = pytz.timezone(fuso_horario_destino)
    data_hora_no_destino = data_hora_com_fuso.astimezone(fuso_destino)

    return data_hora_no_destino.strftime('%Y-%m-%dT%H:%M:%S')

