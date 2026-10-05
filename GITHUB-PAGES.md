# Тестовая публикация РЕСК на GitHub Pages

Цель: получить ссылку для согласования с заказчиком вида `https://GITHUB_USER.github.io/resk-site-preview/`. VPS и домен **реск.рф** для этого не нужны. HTTPS на стандартном адресе GitHub Pages предоставляется автоматически — покупать SSL не нужно.

Инструкция рассчитана на текущий статический сайт и терминал Linux. Вместо `GITHUB_USER` подставьте ваш логин GitHub. Если выберете другое имя репозитория, замените `resk-site-preview` в командах и ссылке.

## 1. Подготовьте файлы

Откройте терминал в папке сайта:

```bash
cd '/home/val/Documents/Презентация РЕСК/РЕСК — Лендинг'
ls -la
```

Для публикации нужны `dist/` и `.github/workflows/pages.yml`. Готовый workflow уже добавлен: он загружает содержимое `dist/` на Pages без сборки. На сайте появится `dist/index.html`, а не папка с презентацией.

**На GitHub Free выбирайте публичный репозиторий.** Его файлы будут доступны всем. Загружаем только сайт и инструкции; исходную презентацию, внутренние материалы и ключи туда не добавляем. Обычный Pages-сайт тоже доступен по открытой ссылке: это предпросмотр для согласования, без пароля. Приватные репозитории поддерживаются на платных планах, но сами по себе не делают опубликованный сайт закрытым.

## 2. Создайте репозиторий

На GitHub нажмите **+ → New repository**:

- Repository name: `resk-site-preview`.
- Visibility: **Public**.
- Не включайте создание README, .gitignore или лицензии: файлы уже есть локально.
- Нажмите **Create repository**.

Если сайт уже загружен в существующий репозиторий, используйте его: не повторяйте инициализацию и создание `origin`. Для приватного репозитория на Free лучше создать отдельный публичный репозиторий только с файлами сайта, чем открывать весь существующий проект.

## 3. Отправьте сайт в GitHub

Для новой папки, в которой ещё нет Git-репозитория:

```bash
git init -b main
git add dist .github README.md GITHUB-PAGES.md .gitignore
git status
git commit -m "Add RESK landing preview and Pages deployment"
git remote add origin https://github.com/GITHUB_USER/resk-site-preview.git
git push -u origin main
```

Перед коммитом посмотрите `git status`: в списке должны быть только перечисленные файлы сайта и инструкции. Архивы и скриншоты исключены через `.gitignore`.

Если Git просит имя автора, задайте свои данные и повторите коммит:

```bash
git config user.name 'Ваше имя'
git config user.email 'ВАШ_EMAIL'
```

Для доступа к GitHub удобно заранее авторизоваться через GitHub CLI, если он установлен:

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

Пароль от аккаунта GitHub не подходит для `git push` по HTTPS. Без CLI используйте настроенный SSH-доступ либо персональный токен с доступом к этому репозиторию и правом добавлять workflow. Не вставляйте токен в адрес `origin` или файлы проекта.

Если репозиторий уже существует локально, проверьте `git remote -v` и `git branch --show-current`, добавьте `dist/` и `.github/`, сделайте коммит и push в `main`. Workflow запускается именно для `main`; если рабочая ветка другая, измените строку `branches: [main]` в workflow на её название.

## 4. Включите GitHub Pages

В репозитории откройте **Settings → Pages → Build and deployment**. В поле **Source** выберите **GitHub Actions**.

**Custom domain оставьте пустым.** DNS домена реск.рф сейчас не меняем. Не выбирайте публикацию из ветки: сайт лежит в `dist/`, для этого подготовлен Actions workflow.

Откройте вкладку **Actions → Publish preview to GitHub Pages → Run workflow**, выберите `main` и нажмите **Run workflow**. Ручной запуск нужен для первого развёртывания после включения Pages. Если запуск после первого push уже завершился ошибкой из-за выключенного Pages, просто выполните новый ручной запуск.

Дождитесь зелёной галочки. Обычно это занимает несколько минут. Ссылка будет в результате задачи `deploy` и в **Settings → Pages → Visit site**:

```text
https://GITHUB_USER.github.io/resk-site-preview/
```

Именно её отправляйте заказчику. Для конкретного блока можно добавить `#services`, `#formats` или `#team` в конец адреса.

## 5. Проверьте опубликованный сайт

Откройте ссылку на компьютере и телефоне. Проверьте фотографии, четыре вкладки питания, раскрытие «Состав услуг», меню и форму запроса. Пути к стилям и изображениям в текущем сайте относительные, поэтому адрес с названием репозитория поддерживается.

Форма пока скачивает текст заявки на устройство посетителя — отправка на почту или в CRM не подключена. Объясните это заказчику при согласовании.

В **Settings → Pages** проверьте HTTPS; если доступен переключатель **Enforce HTTPS**, включите его.

## 6. Публикуйте правки

После изменения сайта выполните из той же папки:

```bash
git add dist
git diff --cached --stat
git commit -m "Update landing after review"
git push
```

GitHub автоматически запустит публикацию. Дождитесь зелёной галочки в Actions, затем обновите страницу. Ссылка для заказчика останется той же. Если браузер показывает старую версию, используйте Ctrl+Shift+R или откройте ссылку в приватном окне.

Изменения только в инструкциях не запускают публикацию; при необходимости есть **Run workflow**. Изменение самого workflow запускает публикацию автоматически при push в `main`.

## Если что-то не работает

| Симптом | Что проверить |
|---|---|
| 404 после первой публикации | Зелёная галочка в Actions, адрес из Settings → Pages, правильное имя репозитория. После первого развёртывания подождите несколько минут. |
| Ошибка Configure Pages | В Settings → Pages выбрано GitHub Actions, репозиторий поддерживает Pages на вашем плане. |
| Workflow не появился | Файл находится в `.github/workflows/pages.yml` в корне репозитория, загружен в GitHub; Actions разрешены в Settings → Actions → General. |
| Push не запускает публикацию | Изменены файлы `dist/`, push идёт в ветку, указанную в workflow. |
| Ошибка deployment / permissions | Смотрите красный шаг в Actions. В workflow должны сохраниться `pages: write`, `id-token: write` и environment `github-pages`; проверьте ограничения организации и окружения. |
| Нет фотографий или стилей | Папка `dist/assets/`, `dist/style.css` и `dist/script.js` загружены; пути и регистр имён совпадают. |

Когда согласование закончится, основной сайт можно разместить на VPS по [MANUAL.md](MANUAL.md). Чтобы убрать тестовую публикацию, откройте **Settings → Pages → Unpublish site**; затем отключите workflow через **Actions → Publish preview to GitHub Pages → … → Disable workflow**, чтобы следующий push не опубликовал её снова.

Основа настройки: [официальная инструкция GitHub по custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [настройка источника публикации](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https).
