# Проектное задание пятого спринта

Вам необходимо спроектировать и разработать файловое хранилище, которое позволяет хранить различные типы файлов — документы, фотографии, другие данные.

## Описание задания

Реализовать **http-сервис**, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080` (дефолтное значение, может быть изменено).

<details>
<summary> Список необходимых эндпойнтов. </summary>

1. Статус активности связанных сервисов.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /ping
    ```
    Получить информацию о времени доступа ко всем связанным сервисам, например, к БД, кэшам, примонтированным дискам и т.д.

    **Response**
    ```json
    {
        "db": 1.27,
        "cache": 1.89,
        ...
        "service-N": 0.56
    }
    ```
   </details>

   ![image](https://github.com/user-attachments/assets/0233a938-4107-4c72-b258-df2cb831fbbb)



2. Регистрация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /register
    ```
    Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи.

    </details>


3. Авторизация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /auth
    ```
    Запрос принимает на вход логин и пароль учетной записи и возвращает авторизационный токен. Далее все запросы проверяют наличие токена в заголовках - `Authorization: Bearer <token>`

    </details>

### Авторизация и регистрация происходит через библиотеку [Fief]().

![image](https://github.com/user-attachments/assets/5d04bc83-a208-4d03-aa5b-b250a5224e44)


**Для корректной работы необходимо добавить Redirect URI в таблицу возможных клиентов Fief**

![image](https://github.com/user-attachments/assets/e0005246-0a0e-45d2-973d-449ad9bf5958)

Чтобы получить доступ к защищенным роутам и проверить их работоспобность, необходимо авторизоваться в клиенте Swagger.
![image](https://github.com/user-attachments/assets/15488fc8-9c12-4e72-9082-46b9f1e47b90)

*При первом холодном запуске необходимо также применить все миграции Alembic `alembic upgrade head` в контейнере backend*

Пример успешной авторизации:
![image](https://github.com/user-attachments/assets/a05e5a82-bbb4-42da-a84f-30b056ac323e)

> В качестве OAuth2 провайдера выступает сам Fief, поэтому, чтобы авторизация прошла, предварительно нужно зайти в учетную запись Fief по адресу `http://localhost:8000/login`

> Дашборд станет доступен после авторизации по адресу `http://localhost:8000/admin`

4. Информация о загруженных файлах.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/
    ```
    Вернуть информацию о ранее загруженных файлах. Доступно только авторизованному пользователю.

    **Response**
    ```json
    {
        "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
        "files": [
              {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "name": "notes.txt",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/test-fodler/notes.txt",
                "size": 8512,
                "is_downloadable": true
              },
            ...
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              }
        ]
    }
    ```
    </details>
    
    ![image](https://github.com/user-attachments/assets/5d9850d1-c8c8-4dfc-a7c8-e4e4df824b15)



5. Загрузить файл в хранилище.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/upload
    ```
    Метод загрузки файла в хранилище. Доступно только авторизованному пользователю.
    Для загрузки заполняется полный путь до файла, в который будет загружен/переписан загружаемый файл. Если нужные директории не существуют, то они должны быть созданы автоматически.
    Так же есть возможность указать только путь до директории. В этом случае имя создаваемого файла будет создано в соответствии с передаваемым именем файла.

    **Request**
    ```
    {
        "path": <full-path-to-file>||<path-to-folder>,
    }
    ```

    **Response**
    ```json
    {
        "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
        "name": "notes.txt",
        "created_ad": "2020-09-11T17:22:05Z",
        "path": "/homework/test-fodler/notes.txt",
        "size": 8512,
        "is_downloadable": true
    }
    ```
    </details>
    
    ![image](https://github.com/user-attachments/assets/d34c22ea-0c20-42c7-aa37-d71cb1c47d07)



6. Скачать загруженный файл.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/download
    ```
    Скачивание ранее загруженного файла. Доступно только авторизованному пользователю.

    **Path parameters**
    ```
    /?path=<path-to-file>||<file-meta-id>
    ```
    Возможность скачивания есть как по переданному пути до файла, так и по идентификатору.
    </details>

    ![image](https://github.com/user-attachments/assets/a3e72624-dc9d-4790-b48c-c689268b3b58)



</details>



<details>
<summary> Список дополнительных (опциональных) эндпойнтов. </summary>


1. Добавление возможности скачивания в архиве.
   <details>

   <summary> Описание изменений. </summary>

    ```
    GET /files/download
    ```
    Path-параметр расширяется дополнительным параметром – `compression`. Доступно только авторизованному пользователю.

    Дополнительно в `path` можно указать как путь до директории, так и его **UUID**. При скачивании директории скачаются все файлы, находящиеся в ней.

    **Path parameters**
    ```
    /?path=[<path-to-file>||<file-meta-id>||<path-to-folder>||<folder-meta-id>] & compression"=[zip||tar||7z]
    ```
    </details>


2. Добавление информация об использовании пользователем дискового пространства.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /user/status
    ```
    Вернуть информацию о статусе использования дискового пространства и ранее загруженных файлах. Доступно только авторизованному пользователю.

    **Response**
    ```json
    {
        "account_id": "taONIb-OurWxbNQ6ywGRopQngc",
        "info": {
            "root_folder_id": "19f25-3235641",
            "home_folder_id": "19f25-3235641"
        },
        "folders": [
            "root": {
                "allocated": "1000000",
                "used": "395870",
                "files": 89
            },
            "home": {
                "allocated": "1590",
                "used": "539",
                "files": 19
            },
            ...,
            "folder-188734": {
                "allocated": "300",
                "used": "79",
                "files": 2
          }
        ]
    }
    ```
    </details>


3. Добавление возможности поиска файлов по заданным параметрам.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/search
    ```
    Вернуть информацию о загруженных файлах по заданным параметрам. Доступно только авторизованному пользователю.

    **Request**
    ```json
    {
        "options": {
            "path": <folder-id-to-search>,
            "extension": <file-extension>,
            "order_by": <field-to-order-search-result>,
            "limit": <max-number-of-results>
        },
        "query": "<any-text||regex>"
    }
    ```

    **Response**
    ```json
    {
        "mathes": [
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              },
            ...
        ]
    }
    ```
    </details>


4. Поддержка версионирования изменений файлов.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/revisions
    ```
    Вернуть информацию об изменениях файла по заданным параметрам. Доступно только авторизованному пользователю.

    **Request**
    ```json
    {
        "path": <path-to-file>||<file-meta-id>,
        "limit": <max-number-of-results>
    }
    ```

    **Response**
    ```json
    {
        "revisions": [
              {
                "id": "b1863132-5db6-44fe-9d34-b944ab06ad81",
                "name": "presentation.pptx",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/learning/presentation.pptx",
                "size": 3496,
                "is_downloadable": true,
                "rev_id": "676ffc2a-a9a5-47f6-905e-99e024ca8ac8",
                "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "modified_at": "2020-09-21T05:13:49Z"
              },
            ...
        ]
    }
    ```
    </details>

</details>


## Требования к решению

1. В качестве СУБД используйте PostgreSQL (не ниже 10 версии).
2. Опишите [docker-compose](docker-compose.yml) для разработки и локального тестирования сервисов.
3. Используйте концепции ООП.
4. Предусмотрите обработку исключительных ситуаций.
5. Приведите стиль кода в соответствие pep8, flake8, mypy.
6. Логируйте результаты действий.
7. Покройте написанный код тестами.


## Рекомендации к решению

1. За основу решения можно взять реализацию проекта 4 спринта.
2. Используйте готовые библиотеки и пакеты, например, для авторизации. Для поиска можно использовать [сервис openbase](https://openbase.com/categories/python), [PyPi](https://pypi.org/) или на [GitHub](https://github.com/search?).
3. Используйте **in-memory-db** для кэширования данных.
4. Для скачивания файлов можно использовать возможности сервера отдачи статики, для хранения — облачное объектное хранилище (s3).
