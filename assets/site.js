/* Research candidates are kept outside the ancestral graph. */
const branchRoutes = {
  'denis-maternal': { owner: 'denis', title: 'Денис → линия матери', families: 'Нечаевы · Шибаевы · Виноградовы', caption: 'Через маму Ингу и деда Ивана',
    path: [['denis','Денис','Вы'],['inga_nech','Инга Ивановна','Мама'],['ivan_vas_nech','Иван Васильевич Нечаев','Дед по матери'],['olga_shibaeva','Ольга Николаевна Шибаева','Мать деда · прабабушка']],
    target: 'olga_shibaeva', finding: 'shibaev', note: 'Здесь находится новая находка по Шибаевым. Путь к Ольге показан по семейным сведениям; её родители пока не установлены.' },
  'denis-paternal': { owner: 'denis', title: 'Денис → линия отца', families: 'Семёновы · Карпущенко · Мядины', caption: 'Через отца Александра и бабушку Людмилу',
    path: [['denis','Денис','Вы'],['alex_sem','Александр Анатольевич','Отец'],['lyudmila_karp','Людмила Ивановна Карпущенко','Бабушка по отцу'],['ivan_karp','Иван Яковлевич Карпущенко','Отец бабушки · прадед']],
    target: 'ivan_karp', finding: 'karpushchenko', note: 'Здесь ищем связь Ивана 1907 года с семьёй из переписи 1897. Другая линия отца ведёт через деда Анатолия к предполагаемому Петру Семёнову. Родительство Ивана и Анны для Людмилы пока известно по семейным сведениям.' },
  'margo-paternal': { owner: 'margo', title: 'Маргарита → линия отца', families: 'Женцовы · Медведиха', caption: 'Через отца Сергея и деда Николая',
    path: [['margo','Маргарита','Исходная персона'],['sergey_zhents','Сергей Николаевич Женцов','Отец'],['nikolay_zhents','Николай Женцов','Возможный дед · связь проверяется']],
    target: 'nikolay_zhents', note: 'Связь Николая с Сергеем в исследовании остаётся кандидатной. Медведиха и Ильгощи — направления архивного поиска: ранние жители этих мест ещё не установлены как предки.' },
  'margo-maternal': { owner: 'margo', title: 'Маргарита → линия матери', families: 'Рыжиковы · Ливенси · Токмаковы', caption: 'Через маму Викторию и бабушку Лидию',
    path: [['margo','Маргарита','Исходная персона'],['victoria_ryzh','Виктория Николаевна Рыжикова','Мама'],['lidia_livensi','Лидия Михайловна Ливенси','Бабушка по матери'],['mikhail_livensi','Михаил Ли-Вен-Си','Прадед · семейная версия']],
    target: 'mikhail_livensi', note: 'Здесь находятся харбинский и новосибирский маршруты. Публикации о человеке и семейные рассказы оцениваются отдельно от актов о родстве.' }
};

const newPeople = {
  shibaev_nikolai: { name: 'Николай Сергиев Шибаев', dates: 'Упомянут в метрике 1902 года · Крусаново, Ефремовская волость', badge: 'Историческая персона · связь с Ольгой не установлена',
    facts: [{badge:'doc',text:'В записи рождения Александра назван отцом: крестьянин Костромской губернии, Кологривского уезда, Ефремовской волости, деревни Крусанова.'},{badge:'doc',text:'Его законная жена — Анна Васильева; оба православные. «Сергиев» — форма отчества в оригинале.'},{badge:'hyp',text:'Может быть отцом Ольги Николаевны Шибаевой 1899 года. Ольга в этой записи не названа; совпадение имени, фамилии и варианта деревни не доказывает родство.'}],
    family: [{role:'Жена по акту 1902',id:'shibaev_anna',name:'Анна Васильева'},{role:'Сын по акту 1902',id:'shibaev_alexander',name:'Александр'}],
    sources:'<a href="https://digihakemisto.net/item/1298792229/14963843022/209" target="_blank" rel="noopener">Национальный архив Финляндии: I Ca:1, кадр 209, запись 26 ↗</a>', questions:'Найти акт рождения или брака Ольги с именами родителей. Год рождения и родители самого Николая неизвестны.', route:'denis-maternal', candidate:true },
  shibaev_anna: { name:'Анна Васильева', dates:'Упомянута в метрике 1902 года · девичья фамилия неизвестна', badge:'Мать Александра по акту · связь с Ольгой не установлена',
    facts:[{badge:'doc',text:'В записи рождения Александра названа законной женой Николая Сергиева Шибаева и матерью ребёнка; православная.'},{badge:'hyp',text:'Возможная мать Ольги Николаевны Шибаевой. Прямой связывающей записи нет. «Васильева» в этой записи — форма отчества, не установленная девичья фамилия.'}],
    family:[{role:'Муж по акту 1902',id:'shibaev_nikolai',name:'Николай Сергиев Шибаев'},{role:'Сын по акту 1902',id:'shibaev_alexander',name:'Александр'}],
    sources:'<a href="https://digihakemisto.net/item/1298792229/14963843022/209" target="_blank" rel="noopener">Оригинал записи 26, 1902 ↗</a>',questions:'Установить девичью фамилию и проверить, названа ли она матерью Ольги.',route:'denis-maternal',candidate:true },
  shibaev_alexander: {name:'Александр · сын Николая Шибаева',dates:'Рождение 20 августа 1902 · крещение 25 августа 1902',badge:'Ребёнок в метрике · возможное братство с Ольгой не доказано',
    facts:[{badge:'doc',text:'Оригинальная запись 26 Казанской церкви Терийоки: родился 20 августа, крещён 25 августа 1902. Даты приведены как в книге, без пересчёта календаря.'},{badge:'doc',text:'Родители: Николай Сергиев Шибаев и его законная жена Анна Васильева. Крусаново указано при отце; отдельное место рождения младенца не названо.'},{badge:'doc',text:'Восприемники: Пётр Иоаннов Смирнов из Крусанова и Параскева Александрова Петрова из Евдокимова. Это крёстные, их родство с родителями не установлено.'},{badge:'hyp',text:'Мог быть младшим братом Ольги 1899 года. Их общие родители пока не установлены документами.'}],
    family:[{role:'Отец по акту',id:'shibaev_nikolai',name:'Николай Сергиев Шибаев'},{role:'Мать по акту',id:'shibaev_anna',name:'Анна Васильева'}],sources:'<a href="https://digihakemisto.net/item/1298792229/14963843022/209" target="_blank" rel="noopener">Метрическая книга I Ca:1, запись 26 ↗</a>',questions:'Проверить родительство Ольги; её имя в акте Александра отсутствует.',route:'denis-maternal',candidate:true},
  census_yakov: {name:'Яков Степанов Карпущенко',dates:'17 лет в переписи 1897 · Кочковатый, Драгунская волость',badge:'Семья в переписи · возможный отец Ивана не установлен',
    facts:[{badge:'doc',text:'В переписи 1897 записан 17-летним сыном 45-летнего Степана Дмитриева Карпущенко. Возраст даёт приблизительно 1879–1880 год рождения, не точную дату.'},{badge:'hyp',text:'Может быть отцом Ивана Яковлевича Карпущенко 1907 года. Отчество Ивана и общая местность этой связи не доказывают.'}],
    family:[{role:'Отец по переписи',id:'census_stepan',name:'Степан Дмитриев Карпущенко'}],sources:'<a href="https://www.familysearch.org/ark:/61903/3:1:3QS7-L9FQ-SKBQ" target="_blank" rel="noopener">Перепись 1897: ф. 417, оп. 2, д. 3987, кадр 769 ↗</a> · просмотр может потребовать входа',questions:'Нужна запись рождения Ивана 1907 с полными именами родителей.',route:'denis-paternal',candidate:true},
  census_stepan: {name:'Степан Дмитриев Карпущенко',dates:'45 лет в переписи 1897 · Кочковатый',badge:'Глава исторического хозяйства · связь с нашей семьёй не установлена',
    facts:[{badge:'doc',text:'В переписи 1897 указан главой хозяйства, 45 лет; Яков 17 лет записан его сыном.'},{badge:'hyp',text:'Станет кандидатом в деды Ивана 1907 только если будет проверена связь Якова с Иваном. Прямого связывающего акта нет.'}],family:[{role:'Сын по переписи',id:'census_yakov',name:'Яков Степанов Карпущенко'}],sources:'<a href="https://www.familysearch.org/ark:/61903/3:1:3QS7-L9FQ-SKBQ" target="_blank" rel="noopener">Оригинал переписи, кадр 769 ↗</a>',questions:'Проверить каждое поколение отдельно. Совпадение фамилии с другим двором не доказывает братство.',route:'denis-paternal',candidate:true},
  census_foma:{name:'Фома Дмитриев Карпущенко',dates:'60 лет в переписи 1897 · отдельное хозяйство',badge:'Историческая персона · родство не установлено',facts:[{badge:'doc',text:'Найден в другом хозяйстве Кочковатого в переписи 1897, возраст 60 лет.'},{badge:'hyp',text:'Общая фамилия и отчество не доказывают, что Фома — брат Степана, а также не устанавливают его связь с Иваном 1907.'}],family:[],sources:'<a href="https://www.familysearch.org/ark:/61903/3:1:3QS7-89FQ-SLTS" target="_blank" rel="noopener">Перепись 1897, кадр 796 ↗</a>',questions:'Нужен отдельный документ о родстве; не соединять два хозяйства по фамилии.',route:'denis-paternal',candidate:true},
  military_petr:{name:'Пётр Мартимянович (Мартимьянович) Семёнов',dates:'Военные записи августа 1941 · Нуримановский РВК',badge:'Однофамилец из военных записей · тождество не установлено',facts:[{badge:'doc',text:'В военных списках назван Пётр Мартимянович (вариант: Мартимьянович) Семёнов, поступивший из Нуримановского РВК в августе 1941. Окончание отчества читается неуверенно.'},{badge:'hyp',text:'Связь с отцом Анатолия Петровича Семёнова 1935 года не доказана. В просмотренных документах нет достаточной связки по году рождения, селу и семье.'},{badge:'doc',text:'Нуримановский РВК — место призыва; его нельзя автоматически считать местом рождения.'}],family:[],sources:'<a href="https://obd-memorial.ru/html/info.htm?id=60040879700" target="_blank" rel="noopener">Военный список ОБД ↗</a> · <a href="https://obd-memorial.ru/html/info.htm?id=1984769592" target="_blank" rel="noopener">Другая запись ОБД ↗</a>',questions:'Первый шаг — акт рождения Анатолия с полным именем отца. Отчество этого кандидата в семейную карточку Петра не перенесено.',route:'denis-paternal',candidate:true}
};
Object.assign(dossierData, newPeople);

// These are separate research identities, never replacements for family members.
Object.assign(dossierData, {
  candidate_timofey: {name:'Тимофей Яковлевич Карпущенко',dates:'1912 · Кочковатка по военной картотеке',badge:'Историческая персона · родство с Иваном не доказано',route:'denis-paternal',candidate:true,war:true,
    facts:[{badge:'doc',text:'Военная картотека называет 1912 год и Кочковатку; прочитанные наградные листы подтверждают военные сведения.'},{badge:'hyp',text:'Общие отчество и местность дают наводку для проверки рядом с Иваном Яковлевичем 1907. Братство и общие родители не установлены.'}],family:[],sources:'<a href="https://podvignaroda.ru/?#id=1377727334&amp;tab=navDetailManCard" target="_blank" rel="noopener">Официальная военная картотека ↗</a> · <a href="docs/research/2026-10-08-timofey-primary-awards.md" target="_blank" rel="noopener">Проверка наградных оригиналов</a>',questions:'Найти личные записи Ивана и Тимофея с именами родителей.'},
  candidate_professor: {name:'Николай Иванович Карпущенко',dates:'Железнодорожный профессор · Новосибирск',badge:'Кандидат на тождество семейному родственнику',route:'denis-paternal',candidate:true,
    facts:[{badge:'pub',text:'Институциональная публикация СГУПС называет Николая Ивановича Карпущенко, выпускника 1960 года, работника Называевской дистанции пути и профессора.'},{badge:'mem',text:'Семья сообщила о родственнике дедушки — железнодорожном профессоре в Новосибирске, без ФИО.'},{badge:'hyp',text:'Тождество этого человека семейному родственнику, его родители и степень родства с Иваном Яковлевичем не установлены. Отчество не доказывает отцовство Ивана.'}],family:[],sources:'<a href="https://www.stu.ru/education/index.php?page=3746" target="_blank" rel="noopener">Публикация СГУПС ↗</a> · <a href="https://www.pravo.mgimo.ru/?q=node%2F17877" target="_blank" rel="noopener">Биографическая публикация ↗</a>',questions:'Уточнить ФИО семейного родственника и найти документ с именами родителей.'},
  candidate_myadin_dmitry: {name:'Дмитрий Михайлович Мядин',dates:'1922 · индекс ИАОО, Кочковатка',badge:'Архивный однофамилец · родство не установлено',route:'denis-paternal',candidate:true,
    facts:[{badge:'pub',text:'Открытый индекс ИАОО содержит Дмитрия Михайловича Мядина, 1922, в Кочковатке. Оригинальная запись и родители не прочитаны.'},{badge:'hyp',text:'Совпадение местности и отчества не устанавливает связь с Анной Михайловной или её предполагаемым отцом Михаилом.'}],family:[],sources:'<a href="https://lk.iaoo.ru/database/record?id=39597" target="_blank" rel="noopener">Индекс ИАОО, запись 39597 ↗</a>',questions:'Прочитать исходную запись и проверить родителей; не соединять по отчеству.'},
  candidate_myadin_ivan: {name:'Иван Фёдорович Мядин',dates:'1922 · индекс ИАОО, Кочковатка',badge:'Архивный однофамилец · родство не установлено',route:'denis-paternal',candidate:true,
    facts:[{badge:'pub',text:'Открытый индекс ИАОО содержит Ивана Фёдоровича Мядина, 1922, в Кочковатке; исходная запись не прочитана.'},{badge:'hyp',text:'Отношение к семье Анны Михайловны неизвестно. Фёдор не добавляется как новый родственник по одному отчеству.'}],family:[],sources:'<a href="https://lk.iaoo.ru/database/record?id=89092" target="_blank" rel="noopener">Индекс ИАОО, запись 89092 ↗</a>',questions:'Нужен оригинал записи с родителями и независимая связь с семейной ветвью.'},
  candidate_myadin_nikolai: {name:'Николай Михайлович Мядин',dates:'1920 · индекс ИАОО, Кочковатка',badge:'Архивный однофамилец · родство не установлено',route:'denis-paternal',candidate:true,
    facts:[{badge:'pub',text:'Открытый индекс ИАОО содержит Николая Михайловича Мядина, 1920, в Кочковатке; оригинальная запись не прочитана.'},{badge:'hyp',text:'Общее отчество с Анной не доказывает общего отца или братство.'}],family:[],sources:'<a href="https://lk.iaoo.ru/database/record?id=270734" target="_blank" rel="noopener">Индекс ИАОО, запись 270734 ↗</a>',questions:'Получить исходную запись и проверить полные имена родителей.'},
  candidate_vera: {name:'Вера · фамилия не установлена',dates:'В газетном очерке указана смерть в 1957 году',badge:'Сестра героини публикации · связь с нашей Лидией проверяется',route:'margo-maternal',candidate:true,
    facts:[{badge:'pub',text:'Очерк «Женщина с характером», 2018, называет сестру героини Веру и 1957 год смерти; фамилия и отчество не приведены.'},{badge:'hyp',text:'Тождество героини очерка нашей Лидии Михайловне ещё требует связывающей проверки. Вера не отождествлена с Верой Семёновой из другой ветви.'}],family:[],sources:'<a href="https://tverlife.ru/pdf/87-2018.pdf#page=5" target="_blank" rel="noopener">Тверская жизнь, 03.11.2018, с. 5 ↗</a>',questions:'Проверить тождество Лидии и документы сестёр; не достраивать фамилию и отчество.'},
  candidate_stanislava: {name:'Станислава · фамилия не установлена',dates:'Дочь героини газетного очерка',badge:'Публикационный кандидат · связь с нашей семьёй проверяется',route:'margo-maternal',candidate:true,
    facts:[{badge:'pub',text:'Очерк 2018 года называет Станиславу дочерью героини Лидии; фамилия и отчество не указаны.'},{badge:'hyp',text:'Необходима проверка тождества героини с бабушкой Маргариты. Родство Станиславы с нашей семьёй пока не установлено.'}],family:[],sources:'<a href="https://tverlife.ru/pdf/87-2018.pdf#page=5" target="_blank" rel="noopener">Очерк «Женщина с характером», с. 5 ↗</a>',questions:'Проверить семейную связь, сохраняя имя без достроенных персональных данных.'},
  candidate_nikolai_zhents: {name:'Николай Иванович Женцов',dates:'1921 · Медведиха · военная карточка',badge:'Военный однофамилец · тождество деду Маргариты не установлено',route:'margo-paternal',candidate:true,war:true,
    facts:[{badge:'pub',text:'В исследовании сохранена военная карточка Николая Ивановича Женцова, 1921, Медведиха.'},{badge:'hyp',text:'Связь с Сергеем Николаевичем и тождество предполагаемому деду Маргариты не доказаны. Это отдельная поисковая личность.'}],family:[],sources:'<a href="docs/research/2026-09-20-current-evidence-audit.md" target="_blank" rel="noopener">Реестр кандидатов и проверенные ограничения</a>',questions:'Нужна запись Сергея с полным именем отца, затем сверка военной личности.'}
});
newPeople.military_petr.war=true;
dossierData.nikolay_zhents.badge='Предполагаемый дед · семейная версия';
dossierData.nikolay_zhents.dates='Отец Сергея по семейной версии · полное имя уточняется';
dossierData.nikolay_zhents.facts=[{badge:'mem',text:'В семейной схеме обозначен Николай — предполагаемый отец Сергея Николаевича. Полное имя и связывающий акт требуют уточнения.'},{badge:'hyp',text:'Военный Николай Иванович Женцов 1921 года — отдельный кандидат на тождество этому человеку; он вынесен в собственную карточку. Они не объединены.'}];
dossierData.nikolay_zhents.sources='Семейная схема. Военная карточка и исторический контекст Медведихи не заменяют акт о родительстве Сергея.';

const candidateBranches = [
  {anchor:'petr_sem',owner:'denis',title:'Семёновы · проверка личности Петра',note:'Пунктир означает возможное тождество, а не установленного отца Анатолия.',people:[['military_petr','Возможное тождество Петру · не доказано']]},
  {anchor:'ivan_karp',owner:'denis',title:'Карпущенко · возможные продолжения',note:'Яков и Степан связаны переписью между собой. Их связь с Иваном, как и родство остальных кандидатов, ещё не установлена.',people:[['census_yakov','Возможный отец Ивана · гипотеза'],['census_stepan','Отец Якова по переписи · связь с Иваном открыта'],['census_foma','Другой двор · братство со Степаном не доказано'],['candidate_timofey','Возможный родственник · степень неизвестна'],['candidate_professor','Возможный семейный родственник · тождество открыто']]},
  {anchor:'anna_myadina',owner:'denis',title:'Мядины · архивные однофамильцы',note:'Эти имена есть в индексе, оригиналы ещё не прочитаны. Родство с Анной или между кандидатами не установлено.',people:[['candidate_myadin_dmitry','Кандидат для проверки · связь неизвестна'],['candidate_myadin_ivan','Кандидат для проверки · связь неизвестна'],['candidate_myadin_nikolai','Кандидат для проверки · связь неизвестна']]},
  {anchor:'olga_shibaeva',owner:'denis',title:'Шибаевы · возможная семья Ольги',note:'Николай и Анна — родители Александра по акту 1902. Их связь с Ольгой пока является гипотезой.',people:[['shibaev_nikolai','Возможный отец Ольги · гипотеза'],['shibaev_anna','Возможная мать Ольги · гипотеза'],['shibaev_alexander','Возможный брат Ольги · гипотеза']]},
  {anchor:'nikolay_zhents',owner:'margo',title:'Женцовы · проверка личности Николая',note:'Военный однофамилец показан отдельно от предполагаемого деда. Связывающего акта нет.',people:[['candidate_nikolai_zhents','Возможное тождество деду · не доказано']]},
  {anchor:'lidia_livensi',owner:'margo',title:'Ливенси · имена из газетного очерка',note:'Роли названы в публикации о Лидии. Тождество героини нашей Лидии и связь с семьёй ещё проверяются.',people:[['candidate_vera','Сестра героини очерка · кандидат'],['candidate_stanislava','Дочь героини очерка · кандидат']]}
];

const familyPaths = {
  denis:'Денис · исходная персона', inga_nech:'Денис → мама Инга', ivan_vas_nech:'Денис → Инга → дед Иван Нечаев',
  olga_shibaeva:'Денис → Инга → Иван Нечаев → Ольга Шибаева · материнская ветка',
  vasily_efim_nech:'Денис → Инга → Иван Нечаев → Василий Нечаев', tamara_vinogr:'Денис → Инга → бабушка Тамара',
  ivan_luk_vinogr:'Денис → Инга → Тамара → Иван Виноградов', anastasia_dem_vinogr:'Денис → Инга → Тамара → Анастасия Виноградова',
  alex_sem:'Денис → отец Александр', anatoly_sem:'Денис → Александр → дед Анатолий', petr_sem:'Денис → Александр → Анатолий → Пётр · семейная версия',
  lyudmila_karp:'Денис → Александр → бабушка Людмила', ivan_karp:'Денис → Александр → Людмила → Иван Карпущенко', anna_myadina:'Денис → Александр → Людмила → Анна · семейная версия'
};
const candidateAssociations = { olga_shibaeva:['shibaev_nikolai','shibaev_anna','shibaev_alexander'],ivan_karp:['census_yakov','census_stepan','census_foma'],petr_sem:['military_petr'],anatoly_sem:['military_petr'] };
candidateBranches.forEach(branch=>candidateAssociations[branch.anchor]=branch.people.map(([id])=>id));

function renderCandidateBranches() {
  document.querySelectorAll('.candidate-branch').forEach(el=>el.remove());
  for(const branch of candidateBranches) {
    document.querySelectorAll(`.p-card[data-person-id="${branch.anchor}"]`).forEach(anchor=>{
      const group=document.createElement('section');
      group.className='candidate-branch';group.dataset.anchor=branch.anchor;group.dataset.family=branch.owner;
      group.setAttribute('aria-label',branch.title+' · родство не доказано');
      group.innerHTML=`<span class="evidence-label candidate">Возможные связи · не доказаны</span><h3>${branch.title}</h3><p class="candidate-anchor">От <button type="button" onclick="openDossier('${branch.anchor}')">${dossierData[branch.anchor].name}</button> <span aria-hidden="true">┄</span></p><div class="candidate-node-grid">${branch.people.map(([id,role])=>{const d=dossierData[id];return `<button type="button" class="candidate-node ${d.war?'war-status':''}" data-candidate-id="${id}" data-family="${branch.owner}" aria-haspopup="dialog" onclick="openDossier('${id}')"><span class="candidate-node-name">${d.name}</span><span class="candidate-node-role">${role}</span><span class="candidate-node-meta">${d.dates}</span><span class="candidate-node-source">Открыть досье и источник →</span></button>`;}).join('')}</div><p class="candidate-branch-note">${branch.note}</p>`;
      anchor.insertAdjacentElement('afterend',group);
    });
  }
  layoutCandidateBranches();
}
function layoutCandidateBranches() {
  const canvas=document.querySelector('.pedigree-canvas');
  const mobile=matchMedia('(max-width:720px)').matches;
  const family=document.querySelector('.pedigree-family:not([hidden])');
  document.querySelectorAll('.candidate-lines').forEach(el=>el.remove());
  if(mobile) {canvas.style.width='';canvas.style.height='';return;}
  if(!family||!family.getClientRects().length) return;
  const groups=[...family.querySelectorAll('.candidate-branch')];
  const columns=[32,370,700,1030].map(x=>[...family.querySelectorAll('.ped-card')].filter(c=>parseFloat(c.style.left)===x));
  const parents=new Map();parents.set(columns[0][0],columns[1]);
  columns[1].forEach((card,i)=>parents.set(card,columns[2].slice(i*2,i*2+2)));
  if(family.id==='pedigree-denis') columns[2].forEach((card,i)=>parents.set(card,columns[3].slice(i*2,i*2+2)));
  else parents.set(columns[2][3],columns[3]);
  const groupFor=card=>groups.find(g=>g.dataset.anchor===card.dataset.personId);
  const blockHeight=card=>Math.max(card.offsetHeight,groupFor(card)?.offsetHeight||0,(parents.get(card)||[]).reduce((sum,c)=>sum+blockHeight(c)+24,0));
  const place=(card,top)=>{
    const block=blockHeight(card),center=top+block/2;card.style.top=(center-card.offsetHeight/2)+'px';
    const group=groupFor(card);if(group) group.style.top=(center-group.offsetHeight/2)+'px';
    let next=top;
    for(const parent of parents.get(card)||[]) {place(parent,next);next+=blockHeight(parent)+24;}
  };
  place(columns[0][0],30);
  const paths=[],familyPaths=[];
  for(const [card,ancestors] of parents) {
    const x=parseFloat(card.style.left)+card.offsetWidth,y=parseFloat(card.style.top)+card.offsetHeight/2;
    for(const ancestor of ancestors) {
      const ax=parseFloat(ancestor.style.left),ay=parseFloat(ancestor.style.top)+ancestor.offsetHeight/2,mid=(x+ax)/2;
      familyPaths.push(`<path class="family-edge" d="M${x} ${y} H${mid} V${ay} H${ax}"/>`);
    }
  }
  family.querySelector('.pedigree-lines').innerHTML=familyPaths.join('');
  for(const group of groups) {
    const anchor=family.querySelector(`.ped-card[data-person-id="${group.dataset.anchor}"]`);
    const x=parseFloat(anchor.style.left)+anchor.offsetWidth,y=parseFloat(anchor.style.top)+anchor.offsetHeight/2;
    const gy=parseFloat(group.style.top)+group.offsetHeight/2;
    paths.push(`<path d="M${x} ${y} H${1330+paths.length*12} V${gy} H1400"/>`);
  }
  const height=Math.max(1090,blockHeight(columns[0][0])+60);
  canvas.style.width=groups.length?'2000px':'1450px';canvas.style.height=height+'px';
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.classList.add('candidate-lines');
  svg.setAttribute('width','2000');svg.setAttribute('height',String(height));svg.setAttribute('aria-hidden','true');svg.innerHTML=paths.join('');family.prepend(svg);
}
window.addEventListener('resize',()=>requestAnimationFrame(layoutCandidateBranches));
document.fonts?.ready.then(()=>requestAnimationFrame(layoutCandidateBranches));
dossierData.olga_shibaeva.facts.push({badge:'hyp',text:'Новая находка 27.10.2026: Николай Сергиев Шибаев и Анна Васильева названы родителями Александра в метрике Терийоки 1902 года; при Николае указана деревня Крусанова. Их связь с Ольгой не установлена.'});
dossierData.olga_shibaeva.questions='Установить точный приход нужного Крусанова на 1899 год и найти акт Ольги с именами родителей. В просмотренном терийокском указателе крещений 1899 подходящей записи нет; это не полный просмотр оригиналов.';
dossierData.ivan_karp.facts.push({badge:'hyp',text:'Яков Степанов Карпущенко, 17 лет в переписи 1897 Кочковатого, — кандидат в отцы. Его родство с Иваном 1907 пока не доказано; в дереве не присоединён.'});
dossierData.petr_sem.facts.push({badge:'hyp',text:'Пётр Мартимянович из военных списков — отдельный кандидат. Совпадение с отцом Анатолия не установлено, его отчество здесь не принимается.'});
dossierData.ivan_luk_vinogr.facts[0]={badge:'doc',text:'Официальный индекс ОБД 56443382 указывает 1910 год и строку «Ивановская обл., Каверинский р-н, д. Галянина». Оригинал просмотрен, но почерк места рождения не даёт уверенного чтения и современной геопривязки. Отождествление с Галанино Ковернинской волости не установлено.'};

const findingFamilies = [
  {id:'shibaev',route:'denis-maternal',eyebrow:'Материнская ветка Дениса · новая находка',title:'Семья Шибаевых в метрике 1902 года',
    path:'Денис → Инга → Иван Нечаев → Ольга Шибаева',
    fact:'Александр родился 20 августа и крещён 25 августа 1902 года. В оригинале названы его родители: Николай Сергиев Шибаев и Анна Васильева. При отце указано Крусаново Ефремовской волости Кологривского уезда.',
    limit:'Кем они приходятся Ольге 1899 года — неизвестно. Николай и Анна могут быть её родителями, Александр — братом. Ольга в записи не названа.',
    people:['shibaev_nikolai','shibaev_anna','shibaev_alexander'],anchor:'olga_shibaeva',
    next:'Найти запись Ольги с полными именами родителей; определить приход нужного Крусанова в 1899 году.',
    source:'https://digihakemisto.net/item/1298792229/14963843022/209',sourceLabel:'Оригинальная метрика · запись 26',image:true},
  {id:'karpushchenko',route:'denis-paternal',eyebrow:'Отцовская ветка Дениса · через бабушку Людмилу',title:'Карпущенко в переписи 1897 года',
    path:'Денис → Александр → Людмила Карпущенко → Иван Яковлевич, 1907',
    fact:'В Кочковатом Драгунской волости прочитан двор Степана Дмитриева Карпущенко, 45 лет. Яков Степанов, 17 лет, записан его сыном. Фома Дмитриев, 60 лет, найден в другом хозяйстве.',
    limit:'Не доказано, что этот Яков — отец Ивана 1907 года. Не установлено и братство Степана с Фомой. Эти семьи не соединены с нашим деревом.',
    people:['census_yakov','census_stepan','census_foma'],anchor:'ivan_karp',
    next:'Прочитать акт рождения Ивана за 1907 год в Лесковской книге. Официальное дело найдено, удалённый просмотр требует входа и оплаты.',
    source:'https://www.familysearch.org/ark:/61903/3:1:3QS7-L9FQ-SKBQ',sourceLabel:'Перепись · кадр 769 (может потребоваться вход)'},
  {id:'semenov',route:'denis-paternal',eyebrow:'Отцовская ветка Дениса · через деда Анатолия',title:'Пётр Семёнов в военных списках',
    path:'Денис → Александр → Анатолий Петрович → предполагаемый отец Пётр',
    fact:'Найден Пётр Мартимянович (вариант чтения: Мартимьянович) Семёнов, связанный с Нуримановским РВК в августе 1941 года.',
    limit:'Это однофамилец, а не установленный прадед. В документах нет достаточной связки с Анатолием: год рождения, конкретное село и семья не установлены.',
    people:['military_petr'],anchor:'anatoly_sem',next:'Получить запись рождения Анатолия 1935 года с именами родителей. Дополнительная наводка на перепись 1917: Р-473/1/5226; шифр ещё требует официальной сверки.',
    source:'https://obd-memorial.ru/html/info.htm?id=60040879700',sourceLabel:'Военный документ ОБД'}
];

function personButton(id, role) {
  return `<button type="button" onclick="openDossier('${id}')">${dossierData[id].name}${role ? `<small>${role}</small>` : ''}</button>`;
}
function renderFindings() {
  document.getElementById('findings-list').innerHTML=findingFamilies.map(f=>`
    <article class="finding-card" id="finding-${f.id}">
      <span class="eyebrow">${f.eyebrow}</span>
      <h3>${f.title}</h3><p class="finding-path">${f.path} · путь по семейным сведениям</p>
      <div class="finding-grid"><div class="finding-copy">
        <span class="evidence-label document">Прочитан документ о людях</span><p>${f.fact}</p>
        <div class="candidate-people">${f.people.map(id=>personButton(id,'Открыть сведения и источник')).join('')}</div>
        <div class="uncertain-link"><strong>Связь с нашей семьёй не установлена.</strong> ${f.limit}</div>
        <div class="source-links"><a href="${f.source}" target="_blank" rel="noopener">${f.sourceLabel} ↗</a></div>
      </div>${f.image ? `<figure class="document-preview"><a href="${f.source}" target="_blank" rel="noopener" aria-label="Открыть оригинальный разворот метрики 1902 года"><img src="assets/shibaev-1902.webp" width="1600" height="1235" loading="lazy" alt="Метрическая запись № 26: Александр, родители Николай Сергиев Шибаев и Анна Васильева"></a><figcaption>Оригинал, Национальный архив Финляндии. Терийоки, 1902, запись 26. Нажмите на изображение, чтобы открыть архивный просмотр.</figcaption></figure>` : `<div class="finding-next"><strong>Как проверить связь</strong>${f.next}<div class="route-actions"><button class="action-button secondary" onclick="openDossier('${f.anchor}')">Открыть человека в нашей семье</button></div></div>`}</div>
      ${f.image ? `<div class="finding-next"><strong>Следующая проверка</strong>${f.next}</div>` : ''}
      <div class="route-actions"><button class="action-button secondary" onclick="selectRoute('${f.route}',true,'${f.anchor}')">Показать семейный путь</button></div>
    </article>`).join('');
}
let currentRoute='denis-maternal';
let currentRouteDetails=branchRoutes[currentRoute];
function selectRoute(key, navigate=false, anchor=null) {
  let r=branchRoutes[key]; if(!r) return; currentRoute=key;
  if(key==='denis-paternal'&&anchor==='anatoly_sem') {
    r={...r,
      path:[['denis','Денис','Вы'],['alex_sem','Александр Анатольевич','Отец'],['anatoly_sem','Анатолий Петрович Семёнов','Дед по отцу'],['petr_sem','Пётр Семёнов','Предполагаемый прадед · связь проверяется']],
      target:'anatoly_sem',finding:'semenov',
      note:'Линия через деда Анатолия. Его родители пока не установлены документом. Пётр Мартимянович из военных списков — отдельный кандидат, его тождество с отцом Анатолия не доказано.'};
  }
  currentRouteDetails=r;
  document.querySelectorAll('.branch-choice').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.route===key)));
  document.getElementById('route-panel').innerHTML=`<span class="section-kicker">Выбранный семейный путь</span><h3>${r.title}</h3><ol class="kinship-path" aria-label="Путь родства">${r.path.map(([id,name,role],i)=>`<li><button class="path-person ${i===r.path.length-1?'path-target':''}" onclick="openDossier('${id}')"><small>${role}</small><strong>${name}</strong></button></li>`).join('')}</ol><p class="route-caption">${r.note}</p><div class="route-actions"><button class="action-button secondary" onclick="showRouteInTree()">Показать в дереве</button>${r.finding?`<button class="action-button" onclick="showFinding('${r.finding}')">Документы и кандидаты этой линии</button>`:''}</div>`;
  if(navigate) {switchTab('tree'); document.getElementById('branch-guide').scrollIntoView({block:'start'});}
}
function showFinding(id) {switchTab('findings'); requestAnimationFrame(()=>document.getElementById('finding-'+id)?.scrollIntoView({block:'start'}));}
function showRouteInTree() {
  const r=currentRouteDetails; switchTab('tree'); setViewMode('pedigree'); filterTree(r.owner); searchNodes('');
  document.querySelector('.search-input').value='';
  document.querySelectorAll('.ped-card').forEach(c=>c.classList.toggle('is-path',r.path.some(([id])=>c.dataset.personId===id)));
  const target=document.querySelector(`#pedigree-${r.owner} [data-person-id="${r.target}"]`);
  target?.scrollIntoView({block:'center',inline:'center'}); target?.focus({preventScroll:true});
}

let activeFilter='all';
let activeSearch='';
function switchTab(tabId) {
  if(!document.getElementById('tab-'+tabId)) return;
  document.querySelectorAll('.tab-pane').forEach(el=>el.classList.toggle('active',el.id==='tab-'+tabId));
  document.querySelectorAll('.nav-btn').forEach(el=>{const on=el.dataset.tab===tabId;el.classList.toggle('active',on);el.setAttribute('aria-pressed',String(on));});
  if(tabId==='tree') requestAnimationFrame(layoutCandidateBranches);
}
function setViewMode(mode) {
  for(const [id,m] of [['view-pedigree','pedigree'],['view-hierarchical','hier'],['view-generational','gen']]) document.getElementById(id).style.display=mode===m?'block':'none';
  document.querySelectorAll('.view-btn').forEach(b=>{const on=b.id==='btn-view-'+mode;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});
  updateHighlights();
  requestAnimationFrame(layoutCandidateBranches);
}
function switchPedigree(branch) {
  for(const who of ['denis','margo']) { document.getElementById('pedigree-'+who).hidden=who!==branch;const b=document.getElementById('ped-btn-'+who);b.classList.toggle('active',who===branch);b.setAttribute('aria-pressed',String(who===branch)); }
  if(['denis','margo'].includes(activeFilter)) activeFilter=branch;
  for(const who of ['denis','margo']) document.getElementById('tree-sec-'+who).hidden=['denis','margo'].includes(activeFilter)&&activeFilter!==who;
  updateHighlights(); renderSearchResults();
  requestAnimationFrame(layoutCandidateBranches);
}
function filterTree(type) {
  activeFilter=type;
  if(type==='denis'||type==='margo') switchPedigree(type);
  for(const who of ['denis','margo']) document.getElementById('tree-sec-'+who).hidden=['denis','margo'].includes(type)&&type!==who;
  updateHighlights(); renderSearchResults();
}
function normalizeSearch(text) {return text.toLocaleLowerCase('ru').replaceAll('ё','е');}
function searchNodes(query) {activeSearch=normalizeSearch(query.trim());updateHighlights();renderSearchResults();}
function matchesFilter(card) {
  if(activeFilter==='war') return card.classList.contains('war-status');
  if(activeFilter==='living') return card.classList.contains('living-status');
  if(['denis','margo'].includes(activeFilter)) return card.dataset.family===activeFilter;
  return true;
}
function updateHighlights() {
  document.querySelectorAll('.filter-chip').forEach(b=>{const on=b.dataset.filter===activeFilter;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});
  document.querySelectorAll('.p-card,.candidate-node').forEach(card=>{
    const matches=matchesFilter(card)&&(!activeSearch||normalizeSearch(card.textContent).includes(activeSearch));
    card.style.opacity=matches?'1':'.28'; card.style.borderColor=activeSearch&&matches?'var(--gold)':'';
  });
}
function renderSearchResults() {
  const box=document.getElementById('search-results'); box.hidden=!activeSearch;if(!activeSearch) return;
  const cards=[...document.querySelectorAll('.p-card[data-person-id]')].filter(matchesFilter);
  const allowed=new Set(cards.map(c=>c.dataset.personId));
  const matches=Object.entries(dossierData).filter(([id,d])=>{
    const candidateAllowed=d.candidate&&(activeFilter==='all'||activeFilter===branchRoutes[d.route]?.owner||(activeFilter==='war'&&d.war));
    if(!allowed.has(id)&&!candidateAllowed) return false;
    return normalizeSearch([d.name,d.dates,...d.facts.map(f=>f.text)].join(' ')).includes(activeSearch);
  });
  document.getElementById('search-summary').textContent=matches.length?`Найдено людей: ${matches.length}`:'В выбранном разделе совпадений нет';
  document.getElementById('search-matches').innerHTML=matches.map(([id,d])=>personButton(id,d.candidate?'Кандидат · связь с семьёй не установлена':familyPaths[id]||d.badge)).join('');
}

// Dossiers retain the existing content, with origins and uncertain associations visible.
const baseOpenDossier=openDossier;
let dossierReturnFocus=null;
openDossier=function(id) {
  if(!dossierData[id]) return;
  const overlay=document.getElementById('modal-overlay');
  if(!overlay.classList.contains('active')) dossierReturnFocus=document.activeElement;
  baseOpenDossier(id);
  const d=dossierData[id];
  document.getElementById('m-path').textContent=d.candidate?`Кандидат для проверки · ${branchRoutes[d.route].title}. Родство с нашей семьёй не установлено.`:familyPaths[id]||d.badge;
  document.getElementById('m-path').hidden=false;
  const candidates=candidateAssociations[id]||[];
  document.getElementById('m-candidates-section').hidden=!candidates.length;
  document.getElementById('m-candidates').innerHTML=candidates.map(x=>personButton(x,'Кандидат · связь ещё не доказана')).join('');
  document.body.classList.add('modal-open');overlay.setAttribute('aria-hidden','false');
  document.querySelector('.modal-box').scrollTop=0;
  document.querySelector('.modal-close').focus({preventScroll:true});
  document.querySelector('header').inert=true;document.querySelector('main').inert=true;
};
closeDossier=function(e) {
  const overlay=document.getElementById('modal-overlay');
  if(e&&e.target!==overlay&&!e.target.classList.contains('modal-close')) return;
  overlay.classList.remove('active');overlay.setAttribute('aria-hidden','true'); document.body.classList.remove('modal-open');
  document.querySelector('header').inert=false;document.querySelector('main').inert=false;
  if(dossierReturnFocus?.isConnected) dossierReturnFocus.focus({preventScroll:true});
};
document.addEventListener('keydown',e=>{
  if(!document.getElementById('modal-overlay').classList.contains('active')) return;
  if(e.key==='Escape') {e.preventDefault();closeDossier();return;}
  if(e.key==='Tab') {
    const focusable=[...document.querySelector('.modal-box').querySelectorAll('button,a[href],[tabindex="0"]')].filter(el=>el.getClientRects().length);
    const first=focusable[0], last=focusable[focusable.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
  }
});

// Make every existing interactive person card keyboard accessible.
document.querySelectorAll('.p-card').forEach(card=>{
  const id=card.getAttribute('onclick')?.match(/openDossier\('([^']+)'\)/)?.[1];
  const margo=card.closest('#pedigree-margo,#tree-sec-margo')||card.classList.contains('margo-branch')||card.classList.contains('margo-card');
  card.dataset.family=margo?'margo':'denis';
  if(card.classList.contains('ped-card')) {
    const x=parseInt(card.style.left,10);card.dataset.generation=x<100?'Исходная персона':x<500?'Родители':x<900?'Деды и бабушки':'Прадеды и прабабушки';
  }
  if(!id) return;
  card.dataset.personId=id;card.tabIndex=0;card.setAttribute('role','button');card.setAttribute('aria-haspopup','dialog');
  card.setAttribute('aria-label','Открыть сведения: '+(dossierData[id]?.name||id));
  card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openDossier(id);}});
});
document.getElementById('branch-choices').innerHTML=Object.entries(branchRoutes).map(([key,r])=>`<button type="button" class="branch-choice" data-route="${key}" aria-pressed="false" onclick="selectRoute('${key}')"><span class="branch-owner">${r.owner==='denis'?'Денис Семёнов':'Маргарита Женцова'}</span><strong>${key.endsWith('maternal')?'Линия матери':'Линия отца'}</strong><span class="branch-families">${r.families}</span><span class="branch-caption">${r.caption}</span></button>`).join('');
renderFindings();renderCandidateBranches();selectRoute(currentRoute);updateHighlights();
