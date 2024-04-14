## django-filters:
[ru_plur_morph.py](filters%2Fru_plur_morph.py) - Фильтр, который позволяет указать три окончания слова, и определяет нужное в зависимости от количества сущностей.
```html
<ul>
  <li>{{count_course_part}} разде{{ count_course_part|ru_plur_morph:"л,ла,лов" }}</li>
  <li>{{count_lesson}} уро{{ count_lesson|ru_plur_morph:"к,ка,ков" }}</li>
  <li>{{count_video}} видео</li>
  <li>{{count_simple_task}} задани{{ count_simple_task|ru_plur_morph:"e,й,й" }}</li>
</ul>
```
