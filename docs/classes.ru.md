# Классы-прототипы модулей PySca
Процесс сканирования в PySca разделён на этапы. За каждый этап сканирования отвечает отдельный класс - модуль, реализующий все необходимые для данного этапа функции, декларированнынные в соответствующем классе-прототипе.
Каждая функция модуля PySca - элемент конвеера. На вход она получает результаты выполнения предидущей функции (явно - в виде словаря или же как значения аргументов согласно аннотациям к аргументам) другого модуля и возвращет значение в следующую в цепочке функцию. Связи между функциями можно представить в виде таблицы:
 Название функции в абстрактном классе |  Функция-источник аргументов  |  Функция - приёмник результатов
:------------------------------------: | :---------------------------: | :------------------------------: 
 AbstractParser.parse_fields | вводится пользователем | AbstractAddresGenerator.set_parsed_fields
 AbstractAddressGenerator.set_parsed_fields | AbstractParser.parse_fields | нет 
 AbstractAddressGenerator.get_next_address | AbstractScanner.scan_address + AbstractAddressGenerator.get_next_address или None при первом запросе адреса  | AbstractScanner.scan_address и AbstractStorage.put_responce
 AbstractScanner.scan_address | AbstractAddressGenerator.get_next_address  | AbstractAddressGenerator.get_next_address и AbstractStorage.put_responce
 AbstractStorage.put_responce | AbstractAddressGenerator.get_next_address + AbstractScanner.scan_address | нет
 AbstractStorage.save | нет | нет
## Описание классов модулей по отдельности
### AbstractParser
    Задача этого класса - обработка пользовательского ввода, преобразование строк в именованные python-объекты.
#### Методы AbstractParser
    * __init__()
    В аргументы передаются запрошенные параметры из config.py
    * parse_fields()
    В аргументы функции передаётся содержимое текстовых полей, введённое пользователем.
### AbstractAddressGenerator
    Задача модулей-наследников этого класса - обработка вывода парсера и генерация адресов - задач для сканирования на основе не только данных парсера, но и результатов, полученных от сканирования предидущих адресов.
#### Методы AbstractAddressGenerator
    * __init__()
    В аргументы передаются запрошенные параметры из config.py
    * set_parsed_fields()
    В аргументы получает разультаты AbstractParser.parse_fields. Если нужно обрабатывает их и сохраняет как поля класса.
    * get_next_address()
    В аргументы получает либо None как значение всех аргументов - для получения первого адреса, либо результаты работы AbstractScanner.scan_address + результаты собственной работы (тот адрес, который сканировал экземпляр AbstractScanner). На основе полученных данных/внутренних полей возвращает адрес для последующего сканирования либо None, если адресов больше нет.
    ВАЖНО: Так как обращения к функции класса возможны в асинхронном виде, рекомндуется либо оборачивать код функции в lock класса Threading, либо использоват потокобезопасные структуры как поля класса (Queue и т. п.).
### AbstractScanner
    Модули этого класса отвечают за сам процесс сканирования. На данный момент доступно сканирование через функцию только одного адреса, своя реализация параллелизма пока невозможна.
#### Методы AbstractScanner
    * __init__()
    В аргументы передаются запрошенные параметры из config.py
    * scan_address()
    На вход метод получает адрес, сгенерированный AbstractAddresGenerator'ом, возвращает результаты сканирования. В процессе сканирования не рекомендуется менять поля класса, а если менять, то только потокобезопасно.
#### Методы AbstractStorage
    * __init__()
    В аргументы передаются запрошенные параметры из config.py
    * put_responce()
    На вход получает сумму результатов выполнения AbstractAddressGenerator.get_next_address и AbstractScammer.scan_address и сохраняет их себе в поля/ в реальном времени записывает их в файл. 
    * save()   
    Метод вызывается в конце сканирования, когда все потоки скаенра остановлены. Сохраняет информацию в файл.
