## views:

[export.py](export.py) - Содержит CBV(Class Based View) с реализованным экспортом под различные разширения

```python
class GoodsCustomExportCsvView(CustomExportCsvView):

    def get(self, request, store_id):
        store = get_object_or_404(Store, pk=store_id)
        return self.export(Goods.objects.filter(store=store), self.get_filename(store))


    def get_column_names(self, *args, **kwargs):

        return [

            'NAME',
            'QUANTITY',
            'COAST',
            'DESCR',
            'DELIVERY DATE',
            
        ]

    def trans_obj_to_row(self, obj, *args, **kwargs):

        return [
            obj.name,
            obj.quantity,
            obj.coast,
            obj.delivary_date,
        ]

    def get_filename(self, store):
        return f"{store.name}__{datetime.date.today()}__goods.csv"


class GoodsLazyExportCsvView(LazyExportCsvView):
    fields = # Оставить пустым для вывода всех полей, ('field1', 'field2', 'field3' ... ) для вывода определенных
    objects = None
    
    def get_queryset(self):
        store = self.get_objects()
        return Goods.objects.filter(store=store)

    def get_objects(self):
        if not self.objects:
            self.objects = get_object_or_404(Store, self.kwargs.get('store_id'))
        return self.get_objects()
    
    def get_filename(self):
        return f"{self.get_objects()}__{datetime.date.today()}__goods.csv"
```

Разница между этими двумя классами по сути в том, что в первом название и контент в столбцах определяется в ручную, а во втором это делается автоматически