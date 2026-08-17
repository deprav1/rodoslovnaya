import os

html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Родословная · Семёновы и Женцовы</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Plus+Jakarta+Sans:wght@400;500;700&family=Spectral:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #f8f6f0;
            --surface: #ffffff;
            --ink: #221d17;
            --muted: #6a6254;
            --denis: #2a598c;
            --margo: #784880;
            --gold: #b3822a;
            --war: #9e3831;
            --living: #2d6a4f;
            --border-radius: 16px;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg);
            color: var(--ink);
            line-height: 1.6;
        }

        h1, h2, h3, h4, .cinzel { font-family: 'Cinzel', serif; }
        .spectral { font-family: 'Spectral', serif; }

        header {
            background-color: var(--surface);
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }
        
        .hero-stats {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: var(--muted);
        }

        .tabs {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .tab-btn {
            background: var(--surface);
            border: 1px solid #e0ddd5;
            padding: 0.75rem 1.5rem;
            border-radius: 30px;
            cursor: pointer;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 500;
            transition: all 0.2s;
        }

        .tab-btn.active {
            background: var(--ink);
            color: var(--surface);
            border-color: var(--ink);
        }

        .tab-content { display: none; padding: 0 2rem 4rem; max-width: 1200px; margin: 0 auto; }
        .tab-content.active { display: block; }

        /* Tree Styles */
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .filters { display: flex; gap: 0.5rem; flex-wrap: wrap; }
        
        .filter-btn {
            background: transparent;
            border: 1px solid #ccc;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
        }
        .filter-btn.active { background: #e0ddd5; }

        .search-box {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: 1px solid #ccc;
            width: 250px;
            font-family: inherit;
        }

        .tree-container {
            overflow-x: auto;
            padding-bottom: 2rem;
        }

        .tree-wrapper {
            display: flex;
            flex-direction: column;
            gap: 3rem;
            min-width: 800px;
        }

        .tree-branch {
            background: var(--surface);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        .branch-title {
            text-align: center;
            margin-bottom: 2rem;
            color: var(--muted);
        }

        .person-card {
            background: var(--surface);
            border: 2px solid #e0ddd5;
            border-radius: var(--border-radius);
            padding: 1rem;
            width: 260px;
            cursor: pointer;
            position: relative;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .person-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        }

        .person-card[data-side="denis"] { border-color: var(--denis); }
        .person-card[data-side="margo"] { border-color: var(--margo); }
        .person-card[data-status="gold"] { border-color: var(--gold); background: #fdfaf4; }
        .person-card[data-status="war"] { border-color: var(--war); background: #fcf4f4; }
        .person-card[data-status="living"] { border-color: var(--living); background: #f2f9f5; }

        .card-role {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--muted);
            font-weight: 700;
        }

        .card-name { font-weight: 700; font-size: 1.1rem; }
        .card-dates { font-size: 0.85rem; color: var(--muted); }
        .card-snippet { font-size: 0.8rem; font-style: italic; color: var(--ink); border-top: 1px solid #eee; padding-top: 0.5rem;}
        
        .person-card.highlight {
            box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.5);
        }
        
        .tree ul {
            padding-top: 20px; position: relative;
            transition: all 0.5s;
            -webkit-transition: all 0.5s;
            -moz-transition: all 0.5s;
            display: flex;
            justify-content: center;
        }

        .tree li {
            float: left; text-align: center;
            list-style-type: none;
            position: relative;
            padding: 20px 5px 0 5px;
            transition: all 0.5s;
            -webkit-transition: all 0.5s;
            -moz-transition: all 0.5s;
        }

        .tree li::before, .tree li::after{
            content: '';
            position: absolute; top: 0; right: 50%;
            border-top: 2px solid #ccc;
            width: 50%; height: 20px;
        }
        .tree li::after{
            right: auto; left: 50%;
            border-left: 2px solid #ccc;
        }

        .tree li:only-child::after, .tree li:only-child::before {
            display: none;
        }

        .tree li:only-child{ padding-top: 0;}

        .tree li:first-child::before, .tree li:last-child::after{
            border: 0 none;
        }
        .tree li:last-child::before{
            border-right: 2px solid #ccc;
            border-radius: 0 5px 0 0;
            -webkit-border-radius: 0 5px 0 0;
            -moz-border-radius: 0 5px 0 0;
        }
        .tree li:first-child::after{
            border-radius: 5px 0 0 0;
            -webkit-border-radius: 5px 0 0 0;
            -moz-border-radius: 5px 0 0 0;
        }

        .tree ul ul::before{
            content: '';
            position: absolute; top: 0; left: 50%;
            border-left: 2px solid #ccc;
            width: 0; height: 20px;
        }

        /* Modal */
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.5);
            display: none; justify-content: center; align-items: center;
            z-index: 1000; padding: 2rem;
        }
        
        .modal-overlay.active { display: flex; }

        .modal {
            background: var(--surface);
            border-radius: var(--border-radius);
            width: 100%; max-width: 720px; max-height: 90vh;
            overflow-y: auto; position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }

        .modal-close {
            position: absolute; top: 1rem; right: 1.5rem;
            font-size: 2rem; cursor: pointer; color: var(--muted);
            line-height: 1; border: none; background: none;
        }

        .modal-header {
            padding: 2rem; border-bottom: 1px solid #eee;
            background: #faf9f6;
        }

        .modal-body { padding: 2rem; }

        .badge {
            display: inline-block; padding: 0.25rem 0.75rem;
            border-radius: 12px; font-size: 0.8rem; font-weight: 600;
            margin-right: 0.5rem; margin-bottom: 0.5rem;
        }

        .fact-item {
            margin-bottom: 1rem; padding: 1rem;
            background: #faf9f6; border-radius: 8px;
            display: flex; gap: 1rem; align-items: flex-start;
        }
        
        .fact-icon { font-size: 1.2rem; }

        .section-title {
            margin: 2rem 0 1rem; font-size: 1.2rem;
            color: var(--ink); border-bottom: 2px solid #eee; padding-bottom: 0.5rem;
        }

        .link-item { color: var(--denis); text-decoration: none; font-weight: 500; cursor:pointer;}
        .link-item:hover { text-decoration: underline; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; background: var(--surface); box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden;}
        th, td { padding: 1rem; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #faf9f6; font-weight: 600; }
        tr:hover { background: #faf9f6; }

        /* Progress */
        .progress-card {
            background: var(--surface); padding: 1.5rem;
            border-radius: var(--border-radius); margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        progress { width: 100%; height: 12px; border-radius: 6px; margin: 1rem 0; }
        progress::-webkit-progress-bar { background-color: #eee; border-radius: 6px; }
        progress::-webkit-progress-value { background-color: var(--denis); border-radius: 6px; }
        
        .template-card {
            border: 1px solid #e0ddd5; border-radius: 8px;
            margin-bottom: 1rem; overflow: hidden;
        }
        .template-header {
            padding: 1rem; background: #faf9f6; cursor: pointer;
            display: flex; justify-content: space-between; font-weight: 600;
        }
        .template-body { padding: 1rem; display: none; white-space: pre-wrap; font-family: monospace; background: #fff;}
        .template-card.open .template-body { display: block; }
        .copy-btn { margin-top: 1rem; padding: 0.5rem 1rem; background: var(--ink); color: white; border: none; border-radius: 4px; cursor: pointer; }

        /* Timeline */
        .timeline { position: relative; max-width: 800px; margin: 0 auto; }
        .timeline::before {
            content: ''; position: absolute; width: 2px; background: #ccc;
            top: 0; bottom: 0; left: 50%; margin-left: -1px;
        }
        .timeline-item {
            padding: 10px 40px; position: relative; background: inherit; width: 50%;
        }
        .timeline-item::after {
            content: ''; position: absolute; width: 16px; height: 16px;
            right: -8px; background: var(--surface); border: 4px solid var(--denis);
            top: 15px; border-radius: 50%; z-index: 1;
        }
        .left { left: 0; }
        .right { left: 50%; }
        .right::after { left: -8px; }
        .timeline-content {
            padding: 20px; background: var(--surface); position: relative;
            border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>

    <header>
        <h1 class="cinzel">Родословная</h1>
        <h2 class="spectral" style="font-weight:400; color:var(--muted); margin-top:0.5rem;">Семёновы и Женцовы</h2>
        <div class="hero-stats">
            <span>👥 42 персоны</span>
            <span>📜 Документы с 1627 г.</span>
            <span>🌳 2 главные ветви</span>
        </div>
    </header>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('tree')">🌳 Древо</button>
        <button class="tab-btn" onclick="switchTab('sources')">📚 Библиотека источников</button>
        <button class="tab-btn" onclick="switchTab('progress')">🔬 Прогресс</button>
        <button class="tab-btn" onclick="switchTab('chronicle')">⏳ Хроника</button>
    </div>

    <!-- TAB 1: TREE -->
    <div id="tab-tree" class="tab-content active">
        <div class="controls">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">Все</button>
                <button class="filter-btn" data-filter="denis">Ветвь Дениса</button>
                <button class="filter-btn" data-filter="margo">Ветвь Маргариты</button>
                <button class="filter-btn" data-filter="war">Фронтовики</button>
                <button class="filter-btn" data-filter="living">Живые</button>
            </div>
            <input type="text" class="search-box" id="search-input" placeholder="Поиск персоны...">
        </div>
        
        <div class="tree-container">
            <div class="tree-wrapper">
                
                <div class="tree-branch" id="branch-denis">
                    <h3 class="branch-title cinzel">Ветвь Семёновых (Денис)</h3>
                    <div class="tree" id="render-denis"></div>
                </div>

                <div class="tree-branch" id="branch-margo">
                    <h3 class="branch-title cinzel">Ветвь Женцовы (Маргарита)</h3>
                    <div class="tree" id="render-margo"></div>
                </div>

            </div>
        </div>
    </div>

    <!-- TAB 2: SOURCES -->
    <div id="tab-sources" class="tab-content">
        <div class="filters" style="margin-bottom:1rem;">
            <button class="filter-btn active">Все</button>
            <button class="filter-btn">🟢 Документы</button>
            <button class="filter-btn">🟡 Публикации</button>
            <button class="filter-btn">🟠 Семейная память</button>
            <button class="filter-btn">🔴 Гипотезы</button>
        </div>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Тип</th>
                    <th>Источник</th>
                    <th>Персоны</th>
                    <th>Ссылка</th>
                    <th>Достоверность</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>1</td><td>Архив ЦАМО</td><td>Донесение 2-й гв. мехбригады о потерях</td><td>И. Л. Виноградов</td><td><a href="https://pamyat-naroda.ru">pamyat-naroda.ru</a></td><td>🟢 Документ</td></tr>
                <tr><td>2</td><td>Архив ЦАМО</td><td>Донесение о потерях 1-й гв. мбр</td><td>И. В. Нечаев (1924)</td><td><a href="https://pamyat-naroda.ru">pamyat-naroda.ru</a></td><td>🟢 Документ</td></tr>
                <tr><td>3</td><td>Публикация</td><td>Газета «Тверская жизнь», очерк</td><td>Семья Ли-Вен-Си</td><td><a href="https://tverlife.ru">tverlife.ru</a></td><td>🟡 Публикация</td></tr>
                <tr><td>4</td><td>Архив СО РАН</td><td>Избирательные списки ИЦиГ СО АН СССР</td><td>Алевтина Ли-Вен-Си</td><td><a href="https://sbras.info">sbras.info</a></td><td>🟢 Документ</td></tr>
                <tr><td>5</td><td>Архив ЦАМО</td><td>Картотека военврачей 17 тп</td><td>Николай Женцов</td><td><a href="https://pamyat-naroda.ru">pamyat-naroda.ru</a></td><td>🟡 Кандидат</td></tr>
                <tr><td>6</td><td>Писцовые книги</td><td>Бежецкий уезд 1627 г.</td><td>с. Медведиха</td><td>ГАТО</td><td>🟢 Документ</td></tr>
                <tr><td>7</td><td>Архив ГИАОО</td><td>Фонд Р-580, карточки эвакуированных</td><td>Карпущенко</td><td>Омский архив</td><td>🟢 Документ</td></tr>
                <tr><td>8</td><td>Семейная память</td><td>Рассказ Маргариты Женцовой (авг. 2026)</td><td>А. Токмакова, Л. Ливенси</td><td>—</td><td>🟠 Память</td></tr>
                <tr><td>9</td><td>Семейная память</td><td>Рассказ Дениса Семёнова (авг. 2026)</td><td>Иван Нечаев, Т. Виноградова</td><td>—</td><td>🟠 Память</td></tr>
                <tr><td>10</td><td>Краеведение</td><td>Реестр переселенческих участков</td><td>д. Кочковатка</td><td>Библиотека ОГИК</td><td>🟡 Публикация</td></tr>
                <tr><td>11</td><td>Архив ЦАМО</td><td>Именной список потерь 2 гв. мбр, Венгрия</td><td>И. Л. Виноградов</td><td><a href="https://pamyat-naroda.ru">pamyat-naroda.ru</a></td><td>🟢 Документ</td></tr>
                <tr><td>12</td><td>База данных</td><td>Книга Памяти Костромской области</td><td>И. В. Нечаев</td><td><a href="https://kniga-pamyati.ru">kniga-pamyati.ru</a></td><td>🟡 Публикация</td></tr>
            </tbody>
        </table>
    </div>

    <!-- TAB 3: PROGRESS -->
    <div id="tab-progress" class="tab-content">
        
        <div class="progress-card">
            <h3 class="cinzel">Семёновы (Омск) - 65%</h3>
            <progress value="65" max="100"></progress>
            <ul>
                <li>✅ Установлены: Пётр → Анатолий → Александр → Денис</li>
                <li>❓ Не хватает: родители Петра Семёнова, подробности о нём</li>
                <li>📋 Действие: Запрос в ЗАГС Омска о рождении Анатолия</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Карпущенко–Мядины (Кочковатка) - 70%</h3>
            <progress value="70" max="100"></progress>
            <ul>
                <li>✅ Установлены: Иван + Анна Мядина → Людмила + Дмитрий</li>
                <li>✅ Найдены: 7 фронтовиков-однофамильцев, белорусские корни</li>
                <li>❓ Не хватает: отчество прадеда Ивана Карпущенко</li>
                <li>📋 Действие: Запрос в ЗАГС Называевска</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Нечаевы (Глебово, Кострома) - 82%</h3>
            <progress value="82" max="100"></progress>
            <ul>
                <li>✅ Установлены: Ефим Моисеевич → Василий Ефимович + Ольга Шибаева → 5 детей → Иван (жив!)</li>
                <li>❓ Не хватает: метрическая запись о рождении Василия (1892)</li>
                <li>📋 Действие: Запрос в ГАКО</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Виноградовы (Нея–Ковернино) - 75%</h3>
            <progress value="75" max="100"></progress>
            <ul>
                <li>✅ Установлены: Лукьян → Иван Лукьянович (погиб 1945) + Анастасия Демидовна → Тамара + Валентин</li>
                <li>✅ Найдены: боевой путь, место гибели, донесение ЦАМО</li>
                <li>❓ Не хватает: метрика рождения в ЦАНО, увековечение в Венгрии</li>
                <li>📋 Действие: Обращение в Посольство</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Женцовы (Медведиха, Тверь) - 35%</h3>
            <progress value="35" max="100"></progress>
            <ul>
                <li>✅ Установлены: с. Медведиха — вотчина монастыря с 1627 г.</li>
                <li>✅ Найден кандидат: военврач Николай Иванович (1921)</li>
                <li>❓ Не подтверждён: точный дед Николай</li>
                <li>📋 Действие: Спросить отца Маргариты (Сергея)</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Ли-Вен-Си (Харбин → Новосибирск) - 60%</h3>
            <progress value="60" max="100"></progress>
            <ul>
                <li>✅ Установлены: Михаил Ли-Вен-Си (модельер), 5 детей, Алевтина (генетик ИЦиГ)</li>
                <li>✅ Найдены: публикация «Тверская жизнь», архивы СО РАН</li>
                <li>❓ Не хватает: запись о браке в ЗАГС Новосибирска, личное дело в СО РАН</li>
                <li>📋 Действие: Запрос в ЗАГС Новосибирска</li>
            </ul>
        </div>
        
        <div class="progress-card">
            <h3 class="cinzel">Токмаковы (Харьковская губ.) - 20%</h3>
            <progress value="20" max="100"></progress>
            <ul>
                <li>✅ Установлено: Антонина Валентиновна Токмакова, сирота, отец Валентин</li>
                <li>❓ Всё остальное: уезд, село, судьба родителей</li>
                <li>📋 Действие: Ждать справку ЗАГС Новосибирска</li>
            </ul>
        </div>

        <h3 class="section-title">📋 Готовые шаблоны запросов</h3>
        
        <div class="template-card">
            <div class="template-header" onclick="this.parentElement.classList.toggle('open')">
                1. ЗАГС Новосибирска (брак Ли-Вен-Си × Токмакова) <span>▼</span>
            </div>
            <div class="template-body">
Прошу выдать справку о заключении брака между Михаилом Ли-Вен-Си и Антониной Валентиновной Токмаковой (ориентировочно 1920-е годы). Прошу указать иные сведения: возраст вступающих в брак, место рождения, место жительства.
                <br><button class="copy-btn" onclick="copyTemplate(this)">Копировать текст</button>
            </div>
        </div>
        <div class="template-card">
            <div class="template-header" onclick="this.parentElement.classList.toggle('open')">
                2. ЗАГС Называевского р-на (рождение Людмилы Карпущенко) <span>▼</span>
            </div>
            <div class="template-body">
Прошу выдать справку о рождении Карпущенко Людмилы Ивановны (10.03.1937, д. Кочковатка). Прошу включить в справку иные сведения: полные ФИО родителей, их возраст, место работы, место жительства.
                <br><button class="copy-btn" onclick="copyTemplate(this)">Копировать текст</button>
            </div>
        </div>
        <div class="template-card">
            <div class="template-header" onclick="this.parentElement.classList.toggle('open')">
                3. Посольство РФ в Венгрии (увековечение И. Л. Виноградова) <span>▼</span>
            </div>
            <div class="template-body">
Прошу рассмотреть вопрос об увековечении памяти моего прадеда, гвардии сержанта Виноградова Ивана Лукьяновича (1910 г.р.), погибшего 22 января 1945 года у с. Капольнашньек. Прилагаю копии донесений ЦАМО.
                <br><button class="copy-btn" onclick="copyTemplate(this)">Копировать текст</button>
            </div>
        </div>
        <div class="template-card">
            <div class="template-header" onclick="this.parentElement.classList.toggle('open')">
                4. ГАКО Кострома (метрики Нечаевых) <span>▼</span>
            </div>
            <div class="template-body">
Прошу выявить актовую запись о рождении Василия Ефимовича Нечаева (ок. 1892 г.р.) в метрических книгах Троицкой церкви с. Солтаново Кологривского уезда (д. Глебово).
                <br><button class="copy-btn" onclick="copyTemplate(this)">Копировать текст</button>
            </div>
        </div>
    </div>

    <!-- TAB 4: CHRONICLE -->
    <div id="tab-chronicle" class="tab-content">
        <div class="timeline">
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>1627</h3>
                    <p>Первое упоминание с. Медведиха как вотчины Кирилло-Белозерского монастыря (род Женцовых).</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>1790</h3>
                    <p>Построена каменная Троицкая церковь в с. Солтаново (приход деревни Глебово, род Нечаевых).</p>
                </div>
            </div>
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>1892</h3>
                    <p>Рождение Василия Ефимовича Нечаева в д. Глебово.</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>1896</h3>
                    <p>Основание д. Кочковатка белорусскими переселенцами (Карпущенко, Мядины).</p>
                </div>
            </div>
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>Нач. XX в.</h3>
                    <p>Рождение Ли Вэнь Си в Харбине. Антонина Токмакова рождается в Харьковской губернии.</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>1945</h3>
                    <p>Гибель Ивана Лукьяновича Виноградова в Венгрии у озера Веленце.</p>
                </div>
            </div>
            <div class="timeline-item left">
                <div class="timeline-content">
                    <h3>1990</h3>
                    <p>Рождение Дениса Семёнова в Омске.</p>
                </div>
            </div>
            <div class="timeline-item right">
                <div class="timeline-content">
                    <h3>1999</h3>
                    <p>Рождение Маргариты Женцовой в Твери.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL -->
    <div class="modal-overlay" id="dossier-modal">
        <div class="modal">
            <button class="modal-close" onclick="closeModal()">×</button>
            <div class="modal-header" id="modal-header">
                <!-- Injected via JS -->
            </div>
            <div class="modal-body" id="modal-body">
                <!-- Injected via JS -->
            </div>
        </div>
    </div>

<script>
const persons = {
  denis: {
    name: "Денис Семёнов",
    dates: "род. 6 мая 1990 г.",
    places: "г. Омск",
    role: "Центральная персона",
    side: "denis",
    status: "normal",
    snippet: "Объединяет сибирскую и костромскую ветви",
    facts: [
      { text: "Родился 6 мая 1990 года в г. Омске", level: "doc", source: "Свидетельство о рождении" },
      { text: "Сын Александра Анатольевича Семёнова и Инги Ивановны Нечаевой", level: "doc", source: "Свидетельство о рождении" }
    ],
    sources: [
      { type: "Документ", name: "Свидетельство о рождении", link: "" }
    ],
    family: {
      father: "alex_sem",
      mother: "inga_nech"
    },
    timeline: [
      { year: "1990", event: "Родился в Омске" }
    ],
    questions: []
  },
  margo: {
    name: "Маргарита Сергеевна Женцова",
    dates: "род. 11 июля 1999 г.",
    places: "г. Тверь",
    role: "Центральная персона",
    side: "margo",
    status: "normal",
    snippet: "Наследница тверских монастырских крестьян и харбинского модельера",
    facts: [
      { text: "Родилась 11 июля 1999 года в г. Твери", level: "doc", source: "Свидетельство о рождении" },
      { text: "Дочь Сергея Николаевича Женцова и Виктории Николаевны Рыжиковой", level: "doc", source: "Свидетельство о рождении" }
    ],
    sources: [
      { type: "Документ", name: "Свидетельство о рождении", link: "" }
    ],
    family: {
      father: "sergey_zhents",
      mother: "victoria_ryzh"
    },
    timeline: [
      { year: "1999", event: "Родилась в Твери" }
    ],
    questions: []
  },
  alex_sem: {
    name: "Александр Анатольевич Семёнов",
    dates: "",
    places: "г. Омск",
    role: "Отец Дениса",
    side: "denis",
    status: "normal",
    snippet: "Сибирская ветвь Семёновых",
    facts: [
      { text: "Сын Анатолия Семёнова и Людмилы Ивановны Карпущенко", level: "memory", source: "Семейная память (2026)" }
    ],
    sources: [],
    family: {
      father: "anatoly_sem",
      mother: "lyudmila_karp",
      children: ["denis"]
    },
    timeline: [],
    questions: ["Точная дата и место рождения"]
  },
  inga_nech: {
    name: "Инга Ивановна Семёнова (Нечаева)",
    dates: "род. 5 мая 1968 г.",
    places: "г. Омск · ОмГУ",
    role: "Мать Дениса",
    side: "denis",
    status: "normal",
    snippet: "Создатель семейного архива и страницы деда на «Бессмертном полку»",
    facts: [
      { text: "Родилась 5 мая 1968 года в г. Омске", level: "doc", source: "Свидетельство о рождении" },
      { text: "Выпускница Омского государственного университета", level: "memory", source: "Семейная память" },
      { text: "Создала страницу деда И. Л. Виноградова на «Бессмертном полку»", level: "pub", source: "Портал moypolk.ru" }
    ],
    sources: [
      { type: "Портал", name: "Страница на «Бессмертном полку»", link: "https://www.moypolk.ru" }
    ],
    family: {
      father: "ivan_vas_nech",
      mother: "tamara_vinogr",
      children: ["denis"]
    },
    timeline: [
      { year: "1968", event: "Родилась в Омске" }
    ],
    questions: []
  },
  anatoly_sem: {
    name: "Анатолий Семёнов",
    dates: "ум. 22 февраля 2012 г.",
    places: "г. Омск",
    role: "Дед Дениса (по отцу)",
    side: "denis",
    status: "normal",
    snippet: "Сын Петра Семёнова, супруг Людмилы Карпущенко",
    facts: [
      { text: "Умер 22 февраля 2012 года в г. Омске", level: "doc", source: "Свидетельство о смерти" },
      { text: "Имел брата Геннадия и сестру Веру (ум. 2013, Уфа)", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: {
      father: "petr_sem",
      spouse: "lyudmila_karp",
      children: ["alex_sem"],
      siblings: ["Геннадий Семёнов", "Вера Семёнова (ум. 2013, Уфа)"]
    },
    timeline: [
      { year: "2012", event: "Умер в Омске" }
    ],
    questions: ["Точная дата рождения", "Место рождения"]
  },
  petr_sem: {
    name: "Пётр Семёнов",
    dates: "",
    places: "Омская область",
    role: "Прадед Дениса",
    side: "denis",
    status: "normal",
    snippet: "Омская ветвь Семёновых",
    facts: [
      { text: "Отец Анатолия Семёнова", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: { children: ["anatoly_sem"] },
    timeline: [],
    questions: ["Полное ФИО", "Даты жизни", "Место рождения", "Родители"]
  },
  lyudmila_karp: {
    name: "Людмила Ивановна Карпущенко",
    dates: "род. 10 марта 1937 г.",
    places: "д. Кочковатка, Называевский р-н, Омская обл.",
    role: "Бабушка Дениса (по отцу)",
    side: "denis",
    status: "gold",
    snippet: "Родилась в белорусской переселенческой деревне 1896 года",
    facts: [
      { text: "Родилась 10 марта 1937 года в д. Кочковатка", level: "doc", source: "Запись ЗАГС Называевского района" },
      { text: "Дочь Ивана Карпущенко и Анны Михайловны Мядиной", level: "memory", source: "Семейная память" },
      { text: "Имела брата Дмитрия Карпущенко", level: "memory", source: "Семейная память" },
      { text: "Деревня Кочковатка основана белорусскими переселенцами в 1896 году", level: "pub", source: "Краеведческие реестры Омской области" }
    ],
    sources: [
      { type: "Краеведение", name: "Реестр переселенческих участков", link: "" }
    ],
    family: {
      father: "ivan_karp",
      mother: "anna_myadina",
      spouse: "anatoly_sem",
      children: ["alex_sem"],
      siblings: ["Дмитрий Карпущенко"]
    },
    timeline: [
      { year: "1937", event: "Родилась в д. Кочковатка" }
    ],
    questions: ["Отчество отца Ивана Карпущенко — ключ к родовому кусту фронтовиков"]
  },
  ivan_karp: {
    name: "Иван Карпущенко",
    dates: "",
    places: "д. Кочковатка, Называевский р-н, Омская обл.",
    role: "Прадед Дениса",
    side: "denis",
    status: "gold",
    snippet: "Родовой куст из 7 фронтовиков-однофамильцев",
    facts: [
      { text: "Жил в деревне Кочковатка Называевского района", level: "memory", source: "Семейная память" },
      { text: "В деревне найдены 7 фронтовиков Карпущенко", level: "doc", source: "База «Память народа» и ГИАОО ф. Р-580" },
      { text: "Дочь Вера Дмитриевна Карпущенко (1921 г.р.) найдена в архиве ГИАОО", level: "doc", source: "ГИАОО, ф. Р-580" }
    ],
    sources: [
      { type: "Архив", name: "ГИАОО, ф. Р-580", link: "" },
      { type: "База данных", name: "Память народа", link: "https://pamyat-naroda.ru" }
    ],
    family: {
      spouse: "anna_myadina",
      children: ["lyudmila_karp", "Дмитрий Карпущенко"]
    },
    timeline: [],
    questions: ["ГЛАВНЫЙ ВОПРОС: Отчество Ивана."]
  },
  anna_myadina: {
    name: "Анна Михайловна Мядина",
    dates: "ум. 21 августа 2002 г.",
    places: "г. Омск (родом из д. Кочковатка)",
    role: "Прабабушка Дениса",
    side: "denis",
    status: "gold",
    snippet: "Девичья фамилия — от белорусского озера Мядель",
    facts: [
      { text: "Умерла 21 августа 2002 года в г. Омске", level: "doc", source: "Свидетельство о смерти" },
      { text: "Девичья фамилия Мядина восходит к белорусскому топониму Мядель", level: "hypothesis", source: "Топонимический анализ" }
    ],
    sources: [],
    family: {
      spouse: "ivan_karp",
      children: ["lyudmila_karp", "Дмитрий Карпущенко"]
    },
    timeline: [
      { year: "2002", event: "Умерла в Омске" }
    ],
    questions: ["Родители Анны Михайловны"]
  },
  ivan_vas_nech: {
    name: "Нечаев Иван Васильевич",
    dates: "род. 1942 г.",
    places: "д. Глебово, Костромская обл.",
    role: "Дед Дениса (по матери)",
    side: "denis",
    status: "living",
    snippet: "ЖИВ! 84 года. Главный свидетель рода.",
    facts: [
      { text: "Родился в 1942 году в д. Глебово", level: "memory", source: "Семейная память" },
      { text: "Жив, 84 года (на август 2026 г.)", level: "memory", source: "Подтверждено Ингой Ивановной" },
      { text: "Назван в честь старшего брата Ивана (1924–1943), погибшего на войне", level: "hypothesis", source: "Совпадение имени и дат" },
      { text: "Имел братьев и сестёр", level: "doc", source: "ЦАМО РФ" }
    ],
    sources: [
      { type: "Архив", name: "ЦАМО РФ", link: "https://pamyat-naroda.ru" },
      { type: "Книга", name: "Книга Памяти", link: "" }
    ],
    family: {
      father: "vasily_efim_nech",
      mother: "olga_shibaeva",
      spouse: "tamara_vinogr",
      children: ["inga_nech"],
      siblings: ["Мария (1924)", "Иван (1924–1943)", "Алексей (1927)", "Валентина (1934)"]
    },
    timeline: [
      { year: "1942", event: "Родился в д. Глебово" },
      { year: "1976", event: "Потерял мать Ольгу Николаевну" }
    ],
    questions: ["Точная дата рождения", "Воспоминания о родителях и деревне Глебово"]
  },
  vasily_efim_nech: {
    name: "Василий Ефимович Нечаев",
    dates: "род. ~1892 г.",
    places: "д. Глебово, Солтановская вол.",
    role: "Прадед Дениса",
    side: "denis",
    status: "normal",
    snippet: "Приход Троицкой церкви с. Солтаново",
    facts: [
      { text: "Родился около 1892 года в д. Глебово", level: "doc", source: "Данные военкомата" },
      { text: "Приход — Троицкая церковь с. Солтаново", level: "doc", source: "Клировые ведомости ГАКО" }
    ],
    sources: [
      { type: "Архив", name: "ГАКО, ф. 56", link: "" }
    ],
    family: {
      father: "efim_mois_nech",
      spouse: "olga_shibaeva",
      children: ["ivan_vas_nech", "Мария (1924)", "Иван (1924)", "Алексей (1927)", "Валентина (1934)"]
    },
    timeline: [
      { year: "~1892", event: "Родился в д. Глебово" }
    ],
    questions: ["Точная дата рождения", "Дата и место бракосочетания"]
  },
  efim_mois_nech: {
    name: "Ефим Моисеевич Нечаев",
    dates: "",
    places: "Костромская губерния",
    role: "Прапрадед Дениса",
    side: "denis",
    status: "normal",
    snippet: "Отец Василия",
    facts: [
      { text: "Отец Василия Ефимовича Нечаева", level: "doc", source: "Отчество сына" },
      { text: "Отчество 'Моисеевич' установлено из военных документов внуков", level: "doc", source: "Учётные карточки ЦАМО" }
    ],
    sources: [],
    family: {
      children: ["vasily_efim_nech"]
    },
    timeline: [],
    questions: ["Метрика рождения", "Жена"]
  },
  olga_shibaeva: {
    name: "Ольга Николаевна Шибаева",
    dates: "1899 — 1976",
    places: "Николо-Поломская вол. → д. Глебово",
    role: "Прабабушка Дениса",
    side: "denis",
    status: "gold",
    snippet: "Родом из окрестностей Николо-Поломы",
    facts: [
      { text: "Родилась в 1899 году в Николо-Поломской волости", level: "memory", source: "Семейная память" },
      { text: "Умерла в 1976 году", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: {
      spouse: "vasily_efim_nech",
      children: ["ivan_vas_nech"]
    },
    timeline: [
      { year: "1899", event: "Родилась" },
      { year: "1976", event: "Умерла" }
    ],
    questions: ["Точная деревня рождения"]
  },
  tamara_vinogr: {
    name: "Тамара Ивановна Виноградова (Нечаева)",
    dates: "",
    places: "Костромская обл.",
    role: "Бабушка Дениса (по матери)",
    side: "denis",
    status: "gold",
    snippet: "Дочь фронтовика",
    facts: [
      { text: "Дочь гвардии сержанта Ивана Лукьяновича Виноградова", level: "doc", source: "Похоронка 1945 г." }
    ],
    sources: [
      { type: "Архив", name: "ЦАМО РФ", link: "https://pamyat-naroda.ru" }
    ],
    family: {
      father: "ivan_luk_vinogr",
      mother: "anastasia_dem_vinogr",
      spouse: "ivan_vas_nech",
      children: ["inga_nech"],
      siblings: ["Валентин Виноградов"]
    },
    timeline: [],
    questions: ["Дата и место рождения"]
  },
  ivan_luk_vinogr: {
    name: "Иван Лукьянович Виноградов",
    dates: "1910 — 22 января 1945",
    places: "д. Галанино → Венгрия",
    role: "Прадед-фронтовик Дениса",
    side: "denis",
    status: "war",
    snippet: "Погиб в Венгрии",
    facts: [
      { text: "Родился в 1910 году в д. Голянина", level: "doc", source: "ЦАМО РФ" },
      { text: "Погиб 22 января 1945 года", level: "doc", source: "ЦАМО РФ" }
    ],
    sources: [
      { type: "Архив ЦАМО", name: "Донесение", link: "https://pamyat-naroda.ru" }
    ],
    family: {
      father: "lukyan_vinogr",
      spouse: "anastasia_dem_vinogr",
      children: ["tamara_vinogr", "Валентин Виноградов"]
    },
    timeline: [
      { year: "1910", event: "Родился" },
      { year: "1945", event: "Погиб" }
    ],
    questions: ["Метрика рождения в ЦАНО", "Увековечение имени"]
  },
  lukyan_vinogr: {
    name: "Лукьян (Лука?) Виноградов",
    dates: "",
    places: "д. Галанино",
    role: "Прапрадед Дениса",
    side: "denis",
    status: "normal",
    snippet: "Отец прадеда-фронтовика",
    facts: [
      { text: "Отец Ивана Лукьяновича", level: "doc", source: "ЦАМО РФ" }
    ],
    sources: [],
    family: { children: ["ivan_luk_vinogr"] },
    timeline: [],
    questions: ["Полное имя"]
  },
  anastasia_dem_vinogr: {
    name: "Анастасия Демидовна Виноградова",
    dates: "",
    places: "г. Нея",
    role: "Прабабушка Дениса",
    side: "denis",
    status: "normal",
    snippet: "Вырастила троих детей",
    facts: [
      { text: "Жена Ивана Лукьяновича Виноградова", level: "doc", source: "ЦАМО РФ" }
    ],
    sources: [
      { type: "Архив ЦАМО", name: "Похоронка", link: "https://pamyat-naroda.ru" }
    ],
    family: {
      father: "demid_vinogr",
      mother: "lyubov_yak",
      spouse: "ivan_luk_vinogr",
      children: ["tamara_vinogr", "Валентин Виноградов"],
      siblings: ["Василий", "Алексей"]
    },
    timeline: [],
    questions: ["Дата и место рождения"]
  },
  demid_vinogr: {
    name: "Демид Арефьевич Виноградов",
    dates: "",
    places: "г. Нея",
    role: "Прапрадед Дениса",
    side: "denis",
    status: "normal",
    snippet: "Костромской крестьянин",
    facts: [
      { text: "Отец Анастасии Демидовны", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: {
      spouse: "lyubov_yak",
      children: ["anastasia_dem_vinogr"]
    },
    timeline: [],
    questions: ["Метрика в ГАКО"]
  },
  lyubov_yak: {
    name: "Любовь Яковлевна",
    dates: "",
    places: "Костромская губерния",
    role: "Прапрабабушка Дениса",
    side: "denis",
    status: "normal",
    snippet: "Жена Демида",
    facts: [
      { text: "Жена Демида Арефьевича", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: { spouse: "demid_vinogr" },
    timeline: [],
    questions: ["Девичья фамилия", "Метрика"]
  },
  sergey_zhents: {
    name: "Женцов Сергей Николаевич",
    dates: "",
    places: "г. Тверь / с. Медведиха",
    role: "Отец Маргариты",
    side: "margo",
    status: "normal",
    snippet: "Представитель древнего тверского рода",
    facts: [
      { text: "Отец Маргариты", level: "doc", source: "Свидетельство о рождении" }
    ],
    sources: [],
    family: {
      father: "nikolay_zhents",
      children: ["margo"]
    },
    timeline: [],
    questions: ["Точная дата рождения"]
  },
  nikolay_zhents: {
    name: "Николай Женцов",
    dates: "вероятно род. 22 июля 1921 г.",
    places: "с. Медведиха",
    role: "Дед Маргариты (по отцу)",
    side: "margo",
    status: "gold",
    snippet: "Наиболее вероятный кандидат — военврач",
    facts: [
      { text: "Все тверские Женцовы происходят из одного села", level: "pub", source: "Анализ базы" },
      { text: "Село Медведиха — вотчина Кирилло-Белозерского монастыря с 1627 года", level: "doc", source: "Писцовые книги" }
    ],
    sources: [
      { type: "Архив ЦАМО", name: "Картотека", link: "https://pamyat-naroda.ru" }
    ],
    family: {
      children: ["sergey_zhents"]
    },
    timeline: [
      { year: "1627", event: "Первое упоминание" }
    ],
    questions: ["ГЛАВНЫЙ ВОПРОС: подтвердить, что дед — именно Николай"]
  },
  victoria_ryzh: {
    name: "Рыжикова Виктория Николаевна",
    dates: "",
    places: "г. Тверь",
    role: "Мать Маргариты",
    side: "margo",
    status: "normal",
    snippet: "Соединяет ветви Рыжиковых и Ли-Вен-Си",
    facts: [
      { text: "Мать Маргариты", level: "doc", source: "Свидетельство о рождении" }
    ],
    sources: [],
    family: {
      father: "nikolay_ryzh",
      mother: "lidia_livensi",
      children: ["margo"]
    },
    timeline: [],
    questions: []
  },
  nikolay_ryzh: {
    name: "Николай Рыжиков",
    dates: "",
    places: "уточняется",
    role: "Дед Маргариты (по матери)",
    side: "margo",
    status: "normal",
    snippet: "Супруг бабушки Лидии",
    facts: [
      { text: "Отец Виктории", level: "memory", source: "Семейная память" }
    ],
    sources: [],
    family: {
      spouse: "lidia_livensi",
      children: ["victoria_ryzh"]
    },
    timeline: [],
    questions: ["ФИО полностью"]
  },
  lidia_livensi: {
    name: "Лидия Михайловна Ливенси (Рыжикова)",
    dates: "",
    places: "Новосибирск → Тверь(?)",
    role: "Бабушка Маргариты (по матери)",
    side: "margo",
    status: "gold",
    snippet: "Несклоняемая фамилия — от китайского имени отца",
    facts: [
      { text: "Дочь Михаила Ли-Вен-Си", level: "memory", source: "Рассказ" }
    ],
    sources: [
      { type: "Публикация", name: "Газета 'Тверская жизнь'", link: "https://tverlife.ru" }
    ],
    family: {
      father: "mikhail_livensi",
      mother: "antonina_tokm",
      spouse: "nikolay_ryzh",
      children: ["victoria_ryzh"],
      siblings: ["Алевтина Ли-Вен-Си"]
    },
    timeline: [],
    questions: ["Дата и место рождения"]
  },
  mikhail_livensi: {
    name: "Михаил Ли-Вен-Си (Ли Вэнь Си / 李文西)",
    dates: "",
    places: "Харбин → Новосибирск",
    role: "Прадед Маргариты",
    side: "margo",
    status: "gold",
    snippet: "Китайский сирота из Харбина, ставший модельером обуви",
    facts: [
      { text: "Сирота из Харбина", level: "memory", source: "Рассказ" },
      { text: "В Новосибирске стал востребованным модельером", level: "pub", source: "Газета" }
    ],
    sources: [
      { type: "Публикация", name: "Газета 'Тверская жизнь'", link: "https://tverlife.ru" }
    ],
    family: {
      spouse: "antonina_tokm",
      children: ["lidia_livensi"]
    },
    timeline: [
      { year: "нач. XX в.", event: "Родился в Харбине" }
    ],
    questions: ["Точная дата рождения", "Китайское происхождение"]
  },
  antonina_tokm: {
    name: "Антонина Валентиновна Токмакова",
    dates: "",
    places: "Харьковская губерния → Новосибирск",
    role: "Прабабушка Маргариты",
    side: "margo",
    status: "gold",
    snippet: "Сирота из Харьковской губернии",
    facts: [
      { text: "Родом из Харьковской губернии", level: "memory", source: "Рассказ" },
      { text: "Осталась сиротой", level: "memory", source: "Рассказ" }
    ],
    sources: [],
    family: {
      father: "valentin_tokm",
      spouse: "mikhail_livensi",
      children: ["lidia_livensi"]
    },
    timeline: [
      { year: "~1905-1910", event: "Родилась" }
    ],
    questions: ["ГЛАВНЫЙ ВОПРОС: Точный уезд"]
  },
  valentin_tokm: {
    name: "Валентин Токмаков",
    dates: "",
    places: "Харьковская губерния",
    role: "Прапрадед Маргариты",
    side: "margo",
    status: "normal",
    snippet: "Отец Антонины",
    facts: [
      { text: "Отец Антонины", level: "memory", source: "Рассказ" }
    ],
    sources: [],
    family: { children: ["antonina_tokm"] },
    timeline: [],
    questions: ["Всё: фамилия, уезд, село"]
  }
};

function generateCard(id) {
    if (!persons[id]) return '';
    const p = persons[id];
    return `
        <div class="person-card" data-id="${id}" data-side="${p.side}" data-status="${p.status}" onclick="openModal('${id}')">
            <div class="card-role">${p.role}</div>
            <div class="card-name spectral">${p.name}</div>
            <div class="card-dates">${p.dates} ${p.places ? '· ' + p.places : ''}</div>
            <div class="card-snippet">${p.snippet}</div>
        </div>
    `;
}

// Custom hierarchy for rendering a nice visual tree
function renderDenisTree() {
    return `
    <ul>
        <li>
            ${generateCard('denis')}
            <ul>
                <li>
                    ${generateCard('alex_sem')}
                    <ul>
                        <li>
                            ${generateCard('anatoly_sem')}
                            <ul>
                                <li>${generateCard('petr_sem')}</li>
                            </ul>
                        </li>
                        <li>
                            ${generateCard('lyudmila_karp')}
                            <ul>
                                <li>${generateCard('ivan_karp')}</li>
                                <li>${generateCard('anna_myadina')}</li>
                            </ul>
                        </li>
                    </ul>
                </li>
                <li>
                    ${generateCard('inga_nech')}
                    <ul>
                        <li>
                            ${generateCard('ivan_vas_nech')}
                            <ul>
                                <li>
                                    ${generateCard('vasily_efim_nech')}
                                    <ul>
                                        <li>${generateCard('efim_mois_nech')}</li>
                                    </ul>
                                </li>
                                <li>${generateCard('olga_shibaeva')}</li>
                            </ul>
                        </li>
                        <li>
                            ${generateCard('tamara_vinogr')}
                            <ul>
                                <li>
                                    ${generateCard('ivan_luk_vinogr')}
                                    <ul>
                                        <li>${generateCard('lukyan_vinogr')}</li>
                                    </ul>
                                </li>
                                <li>
                                    ${generateCard('anastasia_dem_vinogr')}
                                    <ul>
                                        <li>${generateCard('demid_vinogr')}</li>
                                        <li>${generateCard('lyubov_yak')}</li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
    `;
}

function renderMargoTree() {
    return `
    <ul>
        <li>
            ${generateCard('margo')}
            <ul>
                <li>
                    ${generateCard('sergey_zhents')}
                    <ul>
                        <li>${generateCard('nikolay_zhents')}</li>
                    </ul>
                </li>
                <li>
                    ${generateCard('victoria_ryzh')}
                    <ul>
                        <li>${generateCard('nikolay_ryzh')}</li>
                        <li>
                            ${generateCard('lidia_livensi')}
                            <ul>
                                <li>${generateCard('mikhail_livensi')}</li>
                                <li>
                                    ${generateCard('antonina_tokm')}
                                    <ul>
                                        <li>${generateCard('valentin_tokm')}</li>
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
        </li>
    </ul>
    `;
}

document.getElementById('render-denis').innerHTML = renderDenisTree();
document.getElementById('render-margo').innerHTML = renderMargoTree();

// Tabs logic
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById('tab-' + tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Modal logic
function openModal(id) {
    const p = persons[id];
    if (!p) return;
    
    let statusBadge = '';
    if (p.status === 'gold') statusBadge = '<span class="badge" style="background:var(--gold); color:#fff">Подтверждено</span>';
    if (p.status === 'war') statusBadge = '<span class="badge" style="background:var(--war); color:#fff">Фронтовик</span>';
    if (p.status === 'living') statusBadge = '<span class="badge" style="background:var(--living); color:#fff">Живой свидетель</span>';
    
    document.getElementById('modal-header').innerHTML = `
        <h2 class="spectral">${p.name}</h2>
        <div style="margin-top: 0.5rem;">
            <span class="badge" style="background:#eee">${p.role}</span>
            ${statusBadge}
        </div>
        <div style="color:var(--muted); margin-top: 0.5rem;">${p.dates} | ${p.places}</div>
    `;

    const getIcon = (level) => {
        if(level === 'doc') return '🟢';
        if(level === 'pub') return '🟡';
        if(level === 'memory') return '🟠';
        return '🔴';
    };

    let factsHtml = p.facts.map(f => `
        <div class="fact-item">
            <div class="fact-icon">${getIcon(f.level)}</div>
            <div>
                <div>${f.text}</div>
                <div style="font-size:0.8rem; color:var(--muted); margin-top:0.25rem;">Источник: ${f.source}</div>
            </div>
        </div>
    `).join('');

    let sourcesHtml = p.sources && p.sources.length ? p.sources.map(s => `
        <li>
            <strong>${s.type}:</strong> ${s.name} 
            ${s.link ? `<a href="${s.link}" target="_blank" class="link-item">↗</a>` : ''}
        </li>
    `).join('') : '<p>Нет прикрепленных источников.</p>';

    let familyHtml = `<ul>`;
    if (p.family) {
        if (p.family.father) familyHtml += `<li>Отец: <a href="javascript:void(0)" class="link-item" onclick="openModal('${p.family.father}')">${persons[p.family.father].name}</a></li>`;
        if (p.family.mother) familyHtml += `<li>Мать: <a href="javascript:void(0)" class="link-item" onclick="openModal('${p.family.mother}')">${persons[p.family.mother].name}</a></li>`;
        if (p.family.spouse) familyHtml += `<li>Супруг(а): <a href="javascript:void(0)" class="link-item" onclick="openModal('${p.family.spouse}')">${persons[p.family.spouse].name}</a></li>`;
        if (p.family.children && p.family.children.length) {
            p.family.children.forEach(c => {
                let cName = persons[c] ? persons[c].name : c;
                let cLink = persons[c] ? `<a href="javascript:void(0)" class="link-item" onclick="openModal('${c}')">${cName}</a>` : cName;
                familyHtml += `<li>Ребенок: ${cLink}</li>`;
            });
        }
        if (p.family.siblings && p.family.siblings.length) {
            p.family.siblings.forEach(s => {
                familyHtml += `<li>Брат/сестра: ${s}</li>`;
            });
        }
    }
    familyHtml += `</ul>`;

    let timelineHtml = p.timeline && p.timeline.length ? p.timeline.map(t => `
        <li><strong>${t.year}</strong> — ${t.event}</li>
    `).join('') : '<p>Хронология не составлена.</p>';

    let qHtml = p.questions && p.questions.length ? p.questions.map(q => `<li>${q}</li>`).join('') : '<p>Открытых вопросов нет.</p>';

    document.getElementById('modal-body').innerHTML = `
        <h3 class="section-title">📋 Установленные факты</h3>
        ${factsHtml}

        <h3 class="section-title">🔗 Источники</h3>
        <ul>${sourcesHtml}</ul>

        <h3 class="section-title">👥 Семейные связи</h3>
        ${familyHtml}

        <h3 class="section-title">⏳ Хронология жизни</h3>
        <ul>${timelineHtml}</ul>

        <h3 class="section-title">❓ Открытые вопросы</h3>
        <ul>${qHtml}</ul>
    `;
    
    document.getElementById('dossier-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('dossier-modal').classList.remove('active');
}

// Copy to clipboard
function copyTemplate(btn) {
    const text = btn.parentElement.innerText.replace('Копировать текст', '').trim();
    navigator.clipboard.writeText(text).then(() => {
        btn.innerText = 'Скопировано!';
        setTimeout(() => btn.innerText = 'Копировать текст', 2000);
    });
}

// Filters & Search
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        if (!e.target.dataset.filter) return;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        
        const filter = e.target.dataset.filter;
        document.querySelectorAll('.person-card').forEach(card => {
            if (filter === 'all') {
                card.style.opacity = '1';
            } else if (filter === 'denis' || filter === 'margo') {
                card.style.opacity = card.dataset.side === filter ? '1' : '0.2';
            } else {
                card.style.opacity = card.dataset.status === filter ? '1' : '0.2';
            }
        });
    });
});

document.getElementById('search-input').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    document.querySelectorAll('.person-card').forEach(card => {
        card.classList.remove('highlight');
        if (q.length > 2) {
            const name = card.querySelector('.card-name').innerText.toLowerCase();
            if (name.includes(q)) {
                card.classList.add('highlight');
            }
        }
    });
});

</script>
</body>
</html>
"""

os.makedirs(r"c:\Users\Lenovo\Desktop\Родословная", exist_ok=True)
with open(r"c:\Users\Lenovo\Desktop\Родословная\index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
