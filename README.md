
# Милые пёсики
У нас есть программа для загрузки [картинок собак](https://dog.ceo/dog-api/documentation). Для этой программы уже написан тест.  
На вход подается порода собаки. Функция находит одну случайную картинку этой собаки и загружает её на [Я.Диск](https://yandex.ru/dev/disk/poligon/).
Если у породы есть подпороды, то для каждой подпороды загружается по одной картинки.
Например, для doberman будет одна картинка, а для spaniel 7 картинок по одной на каждую подпороду.

# Задание:
Нужно перечислить 10 основных проблем в коде.  
Все найденные проблемы нужно отранжировать по критичности.

# Задание со звёздочкой:
Переписать код так, как Вы считаете нужным, исправив все проблемы.

# Найденные проблемы

Найденные проблемы (overall):
1. (Critical). Большое количество хардкода и дублирования кода
2. (Critical). Токен авторизации для взаимодействия с API ЯД захардкожен в решение многократно (вынес отдельным пунктом, так как токен должен быть засекречен в целях безопасности)
3. (Critical). Большое количество магических значений
4. (Medium). Нет логического разделения на модули
5. (Low). Частичное несоответствие PEP8, падают линтеры
6. (Low). Плохой нейминг (пример: функция `u`, `proverka` в названии теста), отсутствие тайпингов
7. (Low). Наличие бессмысленного кода вроде комментария `# проверка`, `assert True` и пустого конструктора `YaUploader`

Найденные проблемы в тестах:

1. (Critical). Тесты взаимодействуют с одним и тем же каталогом на диске без очистки. Тесты не изолированы друг от друга
2. (Critical). Тесты не учитывают асинхронность API яда, операции добавления всех пикч могут быть еще не выполнены в момент, когда сравнивается количество файлов
3. (Critical). В исходных данных теста есть рандом - нет однозначной стабильности, потенциально может флакать, может быть сложно воспроизвести упавший тест
4. (Critical). Исходя из описания задачи, необходимо проверять не только количество файлов с подпородами, но и их соответствие действительным названиям
5. (Medium). Логически стоит разделить тесты на "с подпородой" и "без подпороды"

В ходе выполнения тестового задания описанные выше проблемы были исправлены, а изначальное решение было переписано.
