# Посещаемость МТУСИ

[![Join the chat at https://gitter.im/gogamwar/mtuci-attendance](https://badges.gitter.im/gogamwar/mtuci-attendance.svg)](https://gitter.im/gogamwar/mtuci-attendance?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
![Страница посещаемости](http://mtuci.azurewebsites.net/static/imgs/Screenshot1.png "Посещаемость МТУСИ")
[Главная страница](http://mtuci.azurewebsites.net/ "Главная страница")

Приложение предназначено для подсчёта количества часов, проведенных студентами на занятии
и состоавления соответствующей статистики.

#### Кто ты?
В репозитории почти всё, что необходимое для того, что бы просто клонировать его и помочь улучшить приложение. Но кое-что сделать всё-таки придётся. Во-первых, создать виртуальное окружение. Если есть желание потестить на Azure, то создавать нужно 32-битную windows версию. А далее установить все зависимости из requirements.txt. Во-вторых, сейчас в настройках секретный ключ и информация о базах данных импортируется из модуля private, которого в репозитории, естественно, нет, поэтому необходимо сгенерировать собственный ключ а базой данных указать sqlite3 (в репозитории уже есть пара старых, можно использовать одну из них, но обязательно применить все миграции).

#### Что внутри
Django-проект разделен на следующие приложения:
* Accounts - приложение для аутентификации с моделями пользователей и групп.
* App - основное приложение (и свалка мусора), всё, что сложно отнести к одно из других приложений здесь. А именно: основной шаблон, страница старосты, главная страница, многие статические файлы, страницы ошибок, модели последних и запланированных изменений.
* Attendance - приложение посещаемости. Содержит единственное представление на основе шаблона и 300 строк представления для отдачи статистики в виде json.
* Manager - (в других местах manage) приложение для панели управления, закрытой от большинства пользователей.

Остальные файлы и папки:
* cache - для файлов кэша (сейчас включен locMemCache)
* temporary - для временных файлов (которых теперь, впрочем, нет)
* wheelhouse - папка с бинарниками пакетов, которые хрен установишь через pip или easy_install обычным способом. На данный момент там только драйвера для MySQL.
* .pyproj, .sln - проект и решение для Visual Studio (PTVS обязателен)
* requirements.txt - файл со списком необходимых пакетов (чуть подробнее ниже)
* runtime.txt - необязательный файл для Azure, указывающий версию Python
* .config - Конфиги для IIS

#### Подробнее о requirements.txt
`--find-links wheelhouse` указывает, что прежде чем лезть на PyPi необходимо посмотреть в папке wheelhouse. Виртуальное окружение не входит в репозиторий, поэтому это важно. В папке wheelhouse обязательно должен лежать исходник пакета с драйвером для MySQL.

#### Список используемых технологий и фреймворков
* [Microsoft Azure](https://azure.microsoft.com/ru-ru/ "Microsoft Azure") и [ClearDB](https://www.cleardb.com/ "ClearDB") - хостинги для веб-приложения и для базы данных MySQl соответственно
* [Django](https://www.djangoproject.com/ "Django") - Python фреймворк
* [JQuery](https://jquery.com/ "JQuery") - основной javascript фреймворк
* [Materialize](http://materializecss.com/ "Materialize"), [Bootstrap](http://getbootstrap.com/ "Bootstrap") - фреймворки для адаптивной вёрстки
* [Hammer.js](http://hammerjs.github.io/ "Hammer.js") (в том числе в составе Materialize) - для контроля за жестами на сенсорных экранах
* [Chartist](https://gionkunz.github.io/chartist-js/ "Chartist") - для построения отзывчивых svg графиков
* [Offline.js](http://github.hubspot.com/offline/docs/welcome/ "Offline.js") - для постоянного контроля за подключением к серверу (т.к. многие функции работают через ajax это необходимо)
* [OudatedBrowser.js](http://outdatedbrowser.com/ru "OudatedBrowser.js") - для просветления пользователей IE6
* [Material Design for Bootstrap](https://fezvrasta.github.io/bootstrap-material-design/ "Material Design for Bootstrap"), [Snackbar.js](http://fezvrasta.github.io/snackbarjs/ "Snackbar.js") - дополнения для Bootstrap
* [Animate.css](https://github.com/daneden/animate.css "Animate.css") - для быстрого создания анимаций
* [WOW.js](https://github.com/matthieua/WOW "WOW.js") - для анимаций при прокрутке
* [Google Fonts](https://www.google.com/fonts "Google Fonts") - хостер веб-шрифтов
* [Md-preloader](https://github.com/rtheunissen/md-preloader "Md-preloader") - простенький svg прелоадер в стиле Material
* [Twitter Typeahead](https://twitter.github.io/typeahead.js/ "Twitter Typeahead") - для удобного поиска в панели управления
* [Google Material Icons](https://design.google.com/icons/ "Google Material Icons") - материальные иконки от Google
* [Fontello](http://fontello.com/ "Fontello") - немного недостающих иконок
* [Modernizr](https://modernizr.com/ "Modernizr") - для проверки поддержки браузером (пока только на главной)
* [SVG.js](https://github.com/wout/svg.js "SVG.js") - для простых анимаций svg
* [SvgPorn](http://svgporn.com/ "SvgPorn") - источник нескольких svg изображений

И, конечно же:
* [stackoverflow.com](http://stackoverflow.com/ "stackoverflow.com")
* [tympanus.net/codrops](http://tympanus.net/codrops/ "tympanus.net/codrops")
* [Atom](https://atom.io/ "Atom") - прекрасный редактор от GitHub на Electron (спасибо ему за линтинг моего ~~говно~~ низкокачественного кода)
* [Inkscape](https://inkscape.org/ru/ "Inkscape") - отличный редактор векторной графики

#### Послесловие
Я не постоянный житель GitHub (посмотрите профиль, господи), поэтому Pull request'ы или еще что-нибудь могу не заметить. В связи с этим пишите мне на [gogamwar@gmail.com](mailto:gogamwar@gmail.com "email") или в [vk.com/gogamwar](https://m.vk.com/write108063245 "vk")
