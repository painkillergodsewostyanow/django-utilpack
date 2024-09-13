import csv
from io import StringIO

from django.http import HttpResponse
from django.views import View


class CustomExportCsvView(View):
    """
    Класс для настраиваемого экспорта данных в csv
    Для минимальной работы переопределите методы get_column_names/trans_obj_to_row,
    и вызовите export в любом HTTP-методе на выбор
    """
    encoding = 'utf-8-sig'
    delimiter = ';'
    filename = None

    def __fill_file(self, queryset):
        column_names = self.get_column_names()
        buffer = StringIO()

        writer = csv.writer(buffer, delimiter=self.delimiter)
        writer.writerow(column_names)

        for obj in queryset:
            row = self.trans_obj_to_row(obj)
            writer.writerow(row)

        return buffer.getvalue().encode(self.encoding)

    def __csv_attach_response(self, queryset, filename=None,):
        """ Логика экспорта """
        filename = filename if filename else self.get_filename()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        response.write(self.__fill_file(queryset))

        return response

    def export(self, queryset, filename=None):
        return self.__csv_attach_response(queryset, filename)

    def get_column_names(self, queryset=None, *args, **kwargs) -> list[str]:
        """ Первая строка (Названия столбцов) """
        raise NotImplementedError('Переопределите метод в классе родителя')

    def trans_obj_to_row(self, obj, *args, **kwargs) -> list[str]:
        """ Логика перевода объектов в csv строки """
        raise NotImplementedError('Переопределите метод в классе родителя')

    def get_filename(self, *args, **kwargs):
        if not self.filename:
            self.filename = 'export.csv'
        return self.filename


class LazyExportCsvView(View):
    """
    'Ленивый' экспорт. Для минимальной работы необходимо указать queryset или переопределить get_queryset.
    :param fields указываются импортируемые поля
    :param filename / get_filename желаемое имя файла
    """
    delimiter = ';'
    encoding = 'utf-8-sig'
    queryset = None
    fields = None
    filename = None

    def __fill_file(self, every_field):
        column_names = self.__get_column_names(self.queryset, every_field)
        buffer = StringIO()

        writer = csv.writer(buffer, delimiter=self.delimiter)
        writer.writerow(column_names)

        for obj in self.queryset:
            row = self.__convert_to_row(obj, every_field)
            writer.writerow(row)

        return buffer.getvalue().encode(self.encoding)

    def __csv_attach_response(self):
        """ Логика экспорта """
        filename = self.get_filename()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        if self.queryset is None:
            self.queryset = self.get_queryset()

        every_field = True if self.fields is None or len(self.fields) == 0 else False

        response.write(self.__fill_file(every_field))

        return response

    def get(self, request, *args, **kwargs):
        return self.__csv_attach_response()

    def __get_column_names(self, queryset, every_field):
        if every_field:
            return [field.name for field in queryset.model._meta.fields]
        return [field.name for field in queryset.model._meta.fields if field.name in self.fields]

    def __convert_to_row(self, obj, every_field):
        if every_field:
            return [getattr(obj, field.name) for field in self.queryset.model._meta.fields]
        return [getattr(obj, field.name) for field in self.queryset.model._meta.fields if field.name in self.fields]

    def get_queryset(self):
        raise NotImplementedError(
            'Переопределите метод get_queryset в классе наследнике, либо задайте классу атрибут queryset'
        )

    def get_filename(self):
        if not self.filename:
            self.filename = 'export.csv'

        return self.filename

