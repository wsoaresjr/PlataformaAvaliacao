from django import template

register = template.Library()

@register.filter
def numero_para_letra(numero):
    """
    Converte números (1, 2, 3, 4, 5) para letras (A, B, C, D, E).
    """
    letras = ['A', 'B', 'C', 'D', 'E']
    try:
        return letras[int(numero) - 1]
    except (IndexError, ValueError, TypeError):
        return ''

@register.filter
def get_item(dictionary, key):
    """Retorna o valor de uma chave em um dicionário."""
    return dictionary.get(key, '')

@register.filter
def index(value, arg):
    """Acessa o índice de uma lista."""
    try:
        return value[int(arg)]
    except (IndexError, ValueError, TypeError):
        return ''
