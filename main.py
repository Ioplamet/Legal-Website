from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from database import engine, get_db, create_tables
from models import News, Service, FAQ, ClientRequest
from admin import NewsAdmin, ServiceAdmin, FAQAdmin, ClientRequestAdmin

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title=settings.SITE_TITLE)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Передаём настройки сайта во все шаблоны автоматически
templates.env.globals["site"] = settings


# ---------------------------------------------------------------------------
# Admin auth
# ---------------------------------------------------------------------------

class BasicAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        if (
            form.get("username") == settings.ADMIN_USERNAME
            and form.get("password") == settings.ADMIN_PASSWORD
        ):
            request.session.update({"admin_logged_in": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_logged_in", False)


admin = Admin(
    app,
    engine,
    authentication_backend=BasicAuthBackend(secret_key=settings.SECRET_KEY),
    title=f"Админ — {settings.SITE_TITLE}",
)
admin.add_view(NewsAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(FAQAdmin)
admin.add_view(ClientRequestAdmin)


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    create_tables()
    _seed_demo_data()


def _seed_demo_data():
    """Добавляет демо-данные, если БД пустая."""
    db = next(get_db())
    try:
        if db.query(Service).count() == 0:
            db.add_all([
                Service(
                    title="Снятие ограничений по 161-ФЗ",
                    description="Федеральный закон №161-ФЗ направлен на борьбу с мошенничеством, однако в этот список нередко попадают добросовестные граждане. Помогаем подготовить и сопроводить процедуру снятия ограничений в рамках действующего законодательства.",
                    price="от 10 000 ₽",
                    order=1,
                ),
                Service(
                    title="Снятие ограничений по 115-ФЗ",
                    description="Федеральный закон №115-ФЗ направлен на борьбу с отмыванием доходов. Помогаем подготовить пояснения, собрать документы и восстановить доступ к вашим финансам.",
                    price="от 10 000 ₽",
                    order=2,
                ),
                Service(
                    title="Снятие банковских ограничений",
                    description="Восстанавливаем доступ к счетам и картам при любых ограничениях. Независимо от причины блокировки, решим проблему максимально оперативно.",
                    price="от 8 000 ₽",
                    order=3,
                ),
                Service(
                    title="Налоговые вопросы",
                    description="Консультируем по налоговым вопросам и ведём дела по налоговым спорам, обеспечивая защиту ваших интересов и законное решение проблемы.",
                    price="от 5 000 ₽",
                    order=4,
                ),
                Service(
                    title="Досудебная работа",
                    description="Помогаем подготовить досудебные претензии и даём профессиональные консультации по вопросам незаконной блокировки счетов и карт.",
                    price="от 5 000 ₽",
                    order=5,
                ),
                Service(
                    title="Судебное сопровождение",
                    description="Полное ведение дела в судах общей юрисдикции и арбитражных судах: от составления иска до исполнения решения.",
                    price="от 30 000 ₽",
                    order=6,
                ),
            ])
        if db.query(FAQ).count() == 0:
            db.add_all([
                FAQ(
                    question="Сколько времени занимает снятие блокировки?",
                    answer="Сроки зависят от конкретного банка и причины блокировки. В среднем досудебное урегулирование занимает от 7 до 30 дней. При наличии полного пакета документов мы стремимся решить вопрос максимально быстро.",
                    order=1,
                ),
                FAQ(
                    question="Что делать, если банк заблокировал карту по 115-ФЗ?",
                    answer="Не паникуйте. Первый шаг — запросить у банка официальное уведомление с указанием причины блокировки. Второй — обратитесь к нам: мы проанализируем ситуацию, подготовим пояснения и необходимые документы для подачи в банк.",
                    order=2,
                ),
                FAQ(
                    question="Гарантируете ли вы результат?",
                    answer="Мы честно оцениваем каждую ситуацию ещё на этапе консультации. Если перспективы дела сомнительны — скажем об этом прямо. Мы не берёмся за заведомо бесперспективные дела и не берём деньги впустую.",
                    order=3,
                ),
                FAQ(
                    question="Работаете ли вы дистанционно?",
                    answer="Да. Мы работаем с клиентами по всей России. Документы принимаем и отправляем в электронном виде, консультации проводим онлайн или по телефону.",
                    order=4,
                ),
                FAQ(
                    question="Сколько стоит первичная консультация?",
                    answer="Первичная консультация по телефону — бесплатно. Мы оцениваем ситуацию и сообщаем, можем ли помочь и на каких условиях. Стоимость дальнейшей работы фиксируется в договоре.",
                    order=5,
                ),
            ])
        if db.query(News).count() == 0:
            db.add_all([
                News(
                    title="Как защититься от блокировки счёта по 115-ФЗ: практические советы",
                    content="Блокировка счёта по 115-ФЗ — одна из самых неприятных ситуаций для предпринимателя или физического лица. Банки обязаны контролировать операции клиентов, и нередко под подозрение попадают вполне законные транзакции.\n\nЧтобы снизить риск блокировки, придерживайтесь нескольких правил:\n\n1. Всегда указывайте назначение платежа. Чем подробнее описание — тем меньше вопросов у банка.\n2. Не дробите платежи без явной необходимости. Частые переводы небольших сумм могут вызвать подозрения.\n3. Держите документы под рукой. Договоры, накладные и счета должны быть готовы для предоставления по запросу банка.\n4. Если получили запрос из банка — отвечайте быстро. Промедление увеличивает риск заморозки средств.\n\nЕсли блокировка уже произошла — обратитесь к нам. Мы поможем подготовить пояснения и восстановить доступ к счёту.",
                ),
                News(
                    title="Изменения в применении 161-ФЗ: что важно знать в 2024 году",
                    content="В 2024 году Центральный банк выпустил ряд разъяснений, касающихся применения Федерального закона №161-ФЗ «О национальной платёжной системе».\n\nКлючевые изменения коснулись порядка оспаривания ограничений и сроков рассмотрения заявлений. Теперь банки обязаны рассматривать обращения клиентов в течение 30 дней и предоставлять мотивированный ответ.\n\nЕсли вы столкнулись с ограничениями по 161-ФЗ — не ждите. Чем раньше начата работа по делу, тем выше шанс на быстрое и успешное решение вопроса. Обратитесь за бесплатной консультацией.",
                ),
            ])
        db.commit()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Routes — публичная часть
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    services = db.query(Service).order_by(Service.order).all()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"services": services}
    )


@app.get("/news", response_class=HTMLResponse)
def news_list(request: Request, db: Session = Depends(get_db)):
    news = db.query(News).order_by(News.created_at.desc()).all()
    return templates.TemplateResponse(
        request=request, name="news.html", context={"news": news}
    )


@app.get("/news/{news_id}", response_class=HTMLResponse)
def news_detail(news_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        return templates.TemplateResponse(
            request=request, name="404.html", context={}, status_code=404
        )
    return templates.TemplateResponse(
        request=request, name="news_detail.html", context={"item": item}
    )


@app.get("/faq", response_class=HTMLResponse)
def faq(request: Request, db: Session = Depends(get_db)):
    questions = db.query(FAQ).order_by(FAQ.order).all()
    return templates.TemplateResponse(
        request=request, name="faq.html", context={"questions": questions}
    )


@app.post("/request", response_class=HTMLResponse)
def submit_request(
    request: Request,
    name: str = Form(...),
    phone: str = Form(...),
    message: str = Form(""),
    db: Session = Depends(get_db),
):
    db.add(ClientRequest(name=name.strip(), phone=phone.strip(), message=message.strip()))
    db.commit()
    return RedirectResponse("/?sent=1", status_code=303)
