from django import template
from django.utils.safestring import mark_safe
from mainapp.models import Smartphone

register = template.Library()
TABLE_HEAD = """
        <table class="table">
          <tbody>
            """
TABLE_TAIL = """
            </tbody>
        </table>
            """
TABLE_CONTENT = """
            <tr>
              <td>{name}</td>
              <td>{value}</td>
            </tr>
            """
PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Частота процесора': 'processor_freq',
        'Оперативная память': 'ram',
        'Ведеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge'
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Заряд аккумулятора': 'accum_volume',
        'Оперативная память': 'ram',
        'Максимальный объм карты памяти': 'sd_volume_max',
        'Камера (МР)': 'main_can_np',
        'Фронтальная камера (МР)': 'frontal_can_np'
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        PRODUCT_SPEC['smartphone']['Наличия карты памяти'] = 'have_sd'
        if product.sd == False and 'Максимальный объм карты памяти' in PRODUCT_SPEC['smartphone']:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объм карты памяти')
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объм карты памяти'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
