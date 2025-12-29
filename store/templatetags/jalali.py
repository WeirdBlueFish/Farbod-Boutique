from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value):
    if value:
        # تبدیل تاریخ میلادی به شمسی
        return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y/%m/%d')
    return ""

@register.filter
def to_jalali_time(value):
    if value:
        # تبدیل تاریخ + ساعت
        return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y/%m/%d ساعت %H:%M')
    return ""