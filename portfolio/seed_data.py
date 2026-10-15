"""Initial site content (taken from the original AI Studio design).

Loaded by `python manage.py seed_portfolio`. After seeding, everything is
edited from the Django admin.
"""

PROFILE = {
    "site_name": "My Rezume",
    "logo_short": "MR",
    "full_name": "Musulmankulov Musulman",
    "role": "Python Developer",
    "specialization": "FastAPI / Django / PostgreSQL",
    "age": 18,
    "city_ru": "Ташкент, Узбекистан",
    "city_uz": "Toshkent, O‘zbekiston",
    "hero_description_ru": (
        "Разрабатываю быстрые асинхронные API на FastAPI и масштабируемые веб-платформы на Django. "
        "Проектирую надёжные базы данных PostgreSQL, распределённые очереди задач Celery "
        "и продуманные Telegram-экосистемы."
    ),
    "hero_description_uz": (
        "FastAPI va Django yordamida yuqori tezlikdagi asinxron API hamda masshtablanuvchi "
        "veb-platformalar yarataman. PostgreSQL ma’lumotlar bazasi, Celery navbatlar tizimi "
        "va murakkab Telegram-ekotizimlarni loyihalashtiraman."
    ),
    "is_available": True,
    "availability_ru": "Открыт для новых предложений",
    "availability_uz": "Yangi takliflarga ochiqman",
    "email": "mmmmmwww200@gmail.com",
    "phone_display": "+998 (95) 801-10-60",
    "phone_raw": "+998958011060",
    "telegram_handle": "@MusulmanMM008",
    "telegram_url": "https://t.me/MusulmanMM008",
    "telegram_channel_url": "https://t.me/MusulmanMM008",
    "github_url": "https://github.com/MusulmanMM008",
    "linkedin_url": "https://linkedin.com/in/musulmankulov-musulman",
    "instagram_url": "https://instagram.com/musulmanmm008",
    "meta_description_ru": (
        "Портфолио Python-разработчика Musulmankulov Musulman (Ташкент, Узбекистан). "
        "FastAPI, Django, PostgreSQL, Celery, микросервисы и Telegram-экосистемы."
    ),
    "meta_description_uz": (
        "Python dasturchi Musulmankulov Musulman portfoliosi (Toshkent, O‘zbekiston). "
        "FastAPI, Django, PostgreSQL, Celery, mikroservislar va Telegram-ekotizimlar."
    ),
}

PROFILE_MEDIA = {
    "hero_video": "hero-video.mp4",
    "hero_poster": "hero_poster.jpg",
}

METRICS = [
    {"value": "18", "unit_ru": "лет", "unit_uz": "yosh", "label_ru": "Возраст · Ташкент, UZ", "label_uz": "Yosh · Toshkent, UZ"},
    {"value": "15+", "unit_ru": "сервисов", "unit_uz": "xizmatlar", "label_ru": "Реализованных Python-проектов", "label_uz": "Yaratilgan Python loyihalar"},
    {"value": "99.9%", "unit_ru": "uptime", "unit_uz": "uptime", "label_ru": "Стабильность API в продакшене", "label_uz": "API barqarorlik ko‘rsatkichi"},
    {"value": "< 35", "unit_ru": "мс", "unit_uz": "ms", "label_ru": "Среднее время ответа FastAPI", "label_uz": "FastAPI o‘rtacha javob vaqti"},
]

ABOUT_CARDS = [
    {
        "icon": "user",
        "title_ru": "Кто я",
        "title_uz": "Men kimman",
        "lead_ru": "Musulmankulov Musulman — 18-летний Python-разработчик из Ташкента, Узбекистан.",
        "lead_uz": "Musulmankulov Musulman — Toshkentlik 18 yoshli Python dasturchi.",
        "body_ru": (
            "Увлечён созданием серверной логики, которая выдерживает высокие нагрузки и остаётся простой "
            "в поддержке. Постоянно изучаю внутреннее устройство CPython, асинхронность asyncio "
            "и паттерны проектирования микросервисов."
        ),
        "body_uz": (
            "Yuqori yuklamalarga bardosh beradigan va kengaytirish oson bo‘lgan server tizimlarini "
            "yaratishga ixtisoslashganman. CPython, asyncio asinxronligi va mikroservis arxitekturasini "
            "chuqur o‘rganaman."
        ),
        "meta_ru": "Ташкент · Готов к удалённой и офисной работе",
        "meta_uz": "Toshkent · Masofaviy va ofisda ishlashga tayyor",
    },
    {
        "icon": "layers",
        "title_ru": "Что умею",
        "title_uz": "Nimalar qila olaman",
        "lead_ru": "Проектирование RESTful API, микросервисов, сложных Telegram-ботов и парсеров данных.",
        "lead_uz": "RESTful API, mikroservislar, mukammal Telegram-botlar va ma’lumotlar tahlili.",
        "body_ru": (
            "Создаю отказоустойчивые бэкенды на FastAPI, Django и Flask. Оптимизирую SQL-запросы "
            "в PostgreSQL через SQLAlchemy 2.0, настраиваю фоновую обработку задач в Celery + Redis "
            "и упаковываю приложения в Docker."
        ),
        "body_uz": (
            "FastAPI, Django va Flask asosida ishonchli backend tizimlar quraman. SQLAlchemy 2.0 orqali "
            "PostgreSQL so‘rovlarini optimallashtiraman, Celery + Redis yordamida fon vazifalarini sozlayman."
        ),
        "meta_ru": "FastAPI · Django · PostgreSQL · Celery · Docker",
        "meta_uz": "FastAPI · Django · PostgreSQL · Celery · Docker",
    },
    {
        "icon": "globe",
        "title_ru": "Языки",
        "title_uz": "Tillar",
        "lead_ru": "Свободная коммуникация в международных и локальных инженерных командах.",
        "lead_uz": "Mahalliy va xalqaro jamoalarda erkin muloqot.",
        "body_ru": (
            "Узбекский — родной язык (C2). Русский — свободное профессиональное владение и ведение "
            "документации (C1). Английский — чтение технической спецификации, код-ревью и рабочая "
            "коммуникация (B2)."
        ),
        "body_uz": (
            "O‘zbek tili — ona tili (C2). Rus tili — erkin professional muloqot va texnik hujjatlar (C1). "
            "Ingliz tili — texnik hujjatlarni o‘qish, code-review va ishchi muloqot (B2)."
        ),
        "meta_ru": "O‘zbek (C2) · Русский (C1) · English (B2)",
        "meta_uz": "O‘zbek (C2) · Русский (C1) · English (B2)",
    },
]

SKILLS = [
    {
        "slug": "python",
        "name": "Python 3.12",
        "category": "backend",
        "level": "Advanced · Core",
        "experience_ru": "Глубокое понимание типизации (typing, TypeVar, Protocol), асинхронного программирования (asyncio), генераторов, контекстных менеджеров и профилирования памяти.",
        "experience_uz": "Qat’iy tipizatsiya (typing, Protocol), asyncio asinxron dasturlash, generatorlar, kontekst menejerlar va xotira optimizatsiyasi bo‘yicha chuqur tajriba.",
        "snippet_language": "python",
        "snippet": '''from typing import AsyncIterator, Protocol
from contextlib import asynccontextmanager


class RepositoryProtocol(Protocol):
    async def fetch_active_users(self, limit: int = 100) -> list[dict]: ...


@asynccontextmanager
async def unit_of_work(session_factory) -> AsyncIterator:
    session = session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()''',
    },
    {
        "slug": "fastapi",
        "name": "FastAPI",
        "category": "backend",
        "level": "Production Ready",
        "experience_ru": "Проектирование высокоскоростных асинхронных микросервисов с Dependency Injection, Pydantic v2 валидацией, JWT-аутентификацией и автогенерацией OpenAPI 3.1.",
        "experience_uz": "Dependency Injection, Pydantic v2 validatsiyasi, JWT-avtorizatsiya va OpenAPI 3.1 hujjatlari bilan yuqori tezlikdagi asinxron mikroservislar yaratish.",
        "snippet_language": "python",
        "snippet": '''from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Tashkent Commerce API", version="2.4.0")


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    sku_items: list[str] = Field(min_length=1)
    amount_uzs: int = Field(gt=1000)


@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate):
    return {"status": "queued", "customer_id": payload.customer_id, "items": len(payload.sku_items)}''',
    },
    {
        "slug": "django",
        "name": "Django & DRF",
        "category": "backend",
        "level": "Production Ready",
        "experience_ru": "Разработка корпоративных платформ на Django 5 и Django REST Framework: кастомные сериализаторы, оптимизация select_related / prefetch_related, кастомизация Admin-панели.",
        "experience_uz": "Django 5 va Django REST Framework yordamida korporativ tizimlar: maxsus serializerlar, select_related / prefetch_related optimizatsiyasi va Admin panel.",
        "snippet_language": "python",
        "snippet": '''from rest_framework import viewsets, permissions


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Transaction.objects
            .select_related("account", "merchant")
            .prefetch_related("audit_logs")
            .filter(account__owner=self.request.user)
            .order_by("-created_at")
        )''',
    },
    {
        "slug": "flask",
        "name": "Flask",
        "category": "backend",
        "level": "Solid Experience",
        "experience_ru": "Создание легковесных REST-сервисов, вебхук-обработчиков для платёжных шлюзов (Payme, Click, Stripe) и внутренних микросервисов.",
        "experience_uz": "Payme, Click va Stripe to‘lov tizimlari uchun yengil REST-servislar hamda webhook-handlerlar ishlab chiqish.",
        "snippet_language": "python",
        "snippet": '''import hashlib
import hmac

from flask import Flask, abort, jsonify, request

app = Flask(__name__)


@app.post("/webhooks/payme")
def handle_payment_webhook():
    signature = request.headers.get("X-Signature", "")
    expected = hmac.new(SECRET, request.get_data(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        abort(401)
    return jsonify({"result": "acknowledged"}), 200''',
    },
    {
        "slug": "postgresql",
        "name": "PostgreSQL",
        "category": "database",
        "level": "Advanced SQL",
        "experience_ru": "Проектирование нормализованных схем БД, сложных индексов (GIN, B-Tree, Partial), транзакций с уровнем изоляции Repeatable Read и аналитических CTE-запросов.",
        "experience_uz": "Normallashtirilgan DB sxemalari, murakkab indekslar (GIN, B-Tree), tranzaksiyalar va analitik CTE so‘rovlarini loyihalash.",
        "snippet_language": "postgresql",
        "snippet": '''WITH monthly_volume AS (
    SELECT
        merchant_id,
        DATE_TRUNC('month', created_at) AS period,
        SUM(amount_uzs) AS total_uzs,
        COUNT(*) AS tx_count
    FROM ledger_transactions
    WHERE status = 'COMPLETED'
    GROUP BY merchant_id, DATE_TRUNC('month', created_at)
)
SELECT merchant_id, period, total_uzs, tx_count
FROM monthly_volume
ORDER BY total_uzs DESC
LIMIT 20;''',
    },
    {
        "slug": "sqlalchemy",
        "name": "SQLAlchemy 2.0",
        "category": "database",
        "level": "Async ORM",
        "experience_ru": "Работа с асинхронным движком asyncpg, декларативными моделями Mapped[], миграциями Alembic и паттерном Repository / Unit of Work.",
        "experience_uz": "Asyncpg drayveri, Mapped[] deklarativ modellari, Alembic migratsiyalari hamda Repository / Unit of Work arxitekturasi.",
        "snippet_language": "python",
        "snippet": '''from datetime import datetime

from sqlalchemy import BigInteger, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserAccount(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())''',
    },
    {
        "slug": "celery",
        "name": "Celery & Redis",
        "category": "database",
        "level": "Distributed Queues",
        "experience_ru": "Построение распределённых очередей задач, периодических расписаний Celery Beat, ретраев с экспоненциальной задержкой и кэширования горячих данных в Redis.",
        "experience_uz": "Celery Beat davriy vazifalari, eksponensial qayta urinishlar (retry) va Redis kesh tizimini qurish.",
        "snippet_language": "python",
        "snippet": '''from celery import Celery

celery_app = Celery("worker", broker="redis://redis:6379/0", backend="redis://redis:6379/1")


@celery_app.task(bind=True, max_retries=3, default_retry_delay=15)
def generate_financial_report(self, organization_id: int):
    try:
        return ReportService.build(organization_id=organization_id)
    except ConnectionError as exc:
        raise self.retry(exc=exc)''',
    },
    {
        "slug": "rest-api",
        "name": "REST API & WebSockets",
        "category": "backend",
        "level": "Architecture",
        "experience_ru": "Проектирование чистых идемпотентных контрактов API, версионирование, пагинация курсорами, Rate Limiting и двусторонний обмен событиями по WebSockets.",
        "experience_uz": "Idempotent API shartnomalarini loyihalash, versiyalash, kursorli paginatsiya, Rate Limiting va WebSockets.",
        "snippet_language": "python",
        "snippet": '''from fastapi import WebSocket


async def stream_order_events(websocket: WebSocket, channel_id: str):
    await websocket.accept()
    await websocket.send_json({
        "channel": channel_id,
        "event": "STREAM_READY",
        "protocol": "WSS/JSON",
    })''',
    },
    {
        "slug": "aiogram",
        "name": "Aiogram 3 / Telegram API",
        "category": "backend",
        "level": "Bot Ecosystems",
        "experience_ru": "Разработка асинхронных Telegram-ботов и WebApp-интеграций на Aiogram 3.x: FSM-состояния, мидлвари, инлайн-клавиатуры и приём платежей.",
        "experience_uz": "Aiogram 3.x asosida asinxron Telegram-botlar va WebApp integratsiyalari: FSM holatlari, middleware va to‘lov tizimlari.",
        "snippet_language": "python",
        "snippet": '''from aiogram import F, Router
from aiogram.types import Message

router = Router(name="orders_router")


@router.message(F.text == "/profile")
async def show_developer_profile(message: Message):
    await message.answer(
        "Musulmankulov Musulman — Python Developer\\n"
        "Stack: FastAPI · Django · PostgreSQL · Celery"
    )''',
    },
    {
        "slug": "docker",
        "name": "Docker & Compose",
        "category": "devops",
        "level": "Containerization",
        "experience_ru": "Многоступенчатые Dockerfile (multi-stage builds) для уменьшения размера образов, оркестрация окружения (API + PostgreSQL + Redis + Celery + Nginx) через Docker Compose.",
        "experience_uz": "Multi-stage Dockerfile yordamida ixcham obrazlar yaratish va Docker Compose orqali barcha servislarni boshqarish.",
        "snippet_language": "docker",
        "snippet": '''FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]''',
    },
    {
        "slug": "git",
        "name": "Git & GitHub Actions",
        "category": "devops",
        "level": "CI/CD Workflow",
        "experience_ru": "Чистая история коммитов (Conventional Commits), Git Flow, автоматический запуск линтеров Ruff, проверки типов mypy и тестов Pytest в CI-пайплайнах.",
        "experience_uz": "Conventional Commits, Git Flow, Ruff linteri, mypy va Pytest testlarini GitHub Actions CI/CD orqali avtomatlashtirish.",
        "snippet_language": "yaml",
        "snippet": '''name: Python Backend CI
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff pytest
      - run: ruff check src/ && pytest -q''',
    },
    {
        "slug": "linux",
        "name": "Linux & Nginx",
        "category": "devops",
        "level": "Server Admin",
        "experience_ru": "Администрирование Ubuntu/Debian серверов, настройка systemd-юнитов, обратного прокси Nginx, SSL-сертификатов и безопасности SSH.",
        "experience_uz": "Ubuntu/Debian serverlarini boshqarish, systemd xizmatlari, Nginx reverse-proxy va SSL sertifikatlarini sozlash.",
        "snippet_language": "nginx",
        "snippet": '''server {
    listen 443 ssl http2;
    server_name api.myrezume.uz;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}''',
    },
]

PROJECTS = [
    {
        "slug": "nexus-commerce-api",
        "title": "Nexus Commerce Microservices API",
        "subtitle_ru": "Высоконагруженное E-Commerce ядро на FastAPI и PostgreSQL",
        "subtitle_uz": "FastAPI va PostgreSQL asosidagi yuqori yuklamali E-Commerce API",
        "description_ru": "Асинхронная платформа для обработки заказов, складских остатков и мгновенных платежей. Реализована идемпотентность транзакций, кэширование каталога в Redis и фоновая генерация чеков через Celery.",
        "description_uz": "Buyurtmalar, ombor qoldiqlari va tezkor to‘lovlarni qayta ishlash uchun asinxron platforma. Tranzaksiyalar idempotentligi, Redis kesh va Celery orqali cheklar generatsiyasi joriy etilgan.",
        "architecture_ru": "Чистая гексагональная архитектура (Ports & Adapters): слой маршрутизации FastAPI отделён от доменной логики и асинхронного репозитория SQLAlchemy 2.0. Время ответа 95-го перцентиля — 28 мс.",
        "architecture_uz": "Toza arxitektura (Ports & Adapters): FastAPI marshrutlash qatlami domen mantiqidan va SQLAlchemy 2.0 asinxron repozitoriysidan ajratilgan. 95-persentil javob vaqti — 28 ms.",
        "metrics": "1,800 RPS · 28 ms latency · 99.95% uptime",
        "year": "2026",
        "accent": "cyan",
        "image": "project_nexus.jpg",
        "tags": "Python, FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker",
        "github_url": "https://github.com/MusulmanMM008",
        "code_filename": "checkout_router.py",
        "code_language": "python",
        "code_preview": '''@router.post("/checkout", response_model=CheckoutReceipt)
async def process_checkout(
    cmd: CheckoutCommand,
    uow: UnitOfWork = Depends(get_uow),
    redis: Redis = Depends(get_redis),
):
    lock_key = f"checkout:lock:{cmd.idempotency_key}"
    if not await redis.set(lock_key, "1", nx=True, ex=60):
        raise HTTPException(status_code=409, detail="Duplicate transaction in flight")

    async with uow:
        order = await uow.orders.reserve_inventory_and_create(cmd)
        await uow.commit()

    dispatch_receipt_task.delay(order.id)
    return CheckoutReceipt.model_validate(order)''',
    },
    {
        "slug": "telepulse-bot-cloud",
        "title": "TelePulse Automation & Webhook Suite",
        "subtitle_ru": "Платформа управления коммерческими Telegram-ботами и воронками",
        "subtitle_uz": "Tijorat Telegram-botlari va webhook oqimlarini boshqarish tizimi",
        "description_ru": "Единый бэкенд для сети Telegram-ботов на базе Aiogram 3 и FastAPI Webhooks. Включает визуальную аналитику конверсий, рассылки по сегментам через Celery и интеграцию локальных платёжных шлюзов Узбекистана.",
        "description_uz": "Aiogram 3 va FastAPI Webhooks asosidagi Telegram-botlar tarmog‘i uchun yagona backend. Konversiyalar tahlili, Celery orqali ommaviy xabarlar va to‘lov tizimlari integratsiyasiga ega.",
        "architecture_ru": "Вместо поллинга используется распределённый приём вебхуков через Nginx + FastAPI с постановкой событий в Redis Stream, что исключает потерю обновлений при пиковых нагрузках.",
        "architecture_uz": "Polling o‘rniga Nginx + FastAPI orqali webhooklar qabul qilinadi va Redis Stream navbatiga uzatiladi, bu esa yuqori yuklamada xabarlar yo‘qolishining oldini oladi.",
        "metrics": "45k+ users · < 15 ms webhook ack",
        "year": "2026",
        "accent": "purple",
        "image": "project_telepulse.jpg",
        "tags": "Python, Aiogram 3, FastAPI, Celery, PostgreSQL, Redis",
        "github_url": "https://github.com/MusulmanMM008",
        "code_filename": "telegram_webhook.py",
        "code_language": "python",
        "code_preview": '''@app.post("/webhook/telegram/{bot_token_hash}")
async def ingest_telegram_update(
    bot_token_hash: str,
    update: dict,
    stream: RedisStreamProducer = Depends(get_stream),
):
    await stream.publish(
        topic="tg_updates_high_priority",
        payload={"bot_hash": bot_token_hash, "update": update},
    )
    return {"ok": True}''',
    },
    {
        "slug": "chronos-celery-grid",
        "title": "Chronos Distributed Task Engine",
        "subtitle_ru": "Система мониторинга и оркестрации фоновых воркеров Celery + Redis",
        "subtitle_uz": "Celery + Redis fon vazifalarini monitoring va orkestratsiya qilish tizimi",
        "description_ru": "Сервис для планирования, трассировки и автоматического восстановления фоновых задач: парсинг маркетплейсов, генерация PDF/Excel-отчётов и синхронизация складских баз по расписанию.",
        "description_uz": "Fon vazifalarini rejalashtirish va monitoring qilish tizimi: marketpleyslarni tahlil qilish, PDF/Excel hisobotlar yaratish hamda ma’lumotlar bazasini sinxronlash.",
        "architecture_ru": "Применён паттерн Dead Letter Queue (DLQ) для сбойных задач, метрики времени выполнения агрегируются в реальном времени и отдаются через WebSockets на панель управления.",
        "architecture_uz": "Xatolik yuz bergan vazifalar uchun Dead Letter Queue (DLQ) qo‘llanilgan, bajarilish vaqti metrikalari WebSockets orqali jonli efirda uzatiladi.",
        "metrics": "1.2M+ tasks/day · auto-retries · WebSockets live",
        "year": "2025",
        "accent": "blue",
        "image": "project_chronos.jpg",
        "tags": "Python, Celery, Redis, FastAPI, Docker, Linux",
        "github_url": "https://github.com/MusulmanMM008",
        "code_filename": "inventory_tasks.py",
        "code_language": "python",
        "code_preview": '''@celery_app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_jitter=True,
)
def sync_marketplace_inventory(self, supplier_id: int) -> dict:
    started = time.perf_counter()
    synced_count = InventorySyncService.run_batch(supplier_id=supplier_id)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {"supplier_id": supplier_id, "synced": synced_count, "elapsed_ms": elapsed_ms}''',
    },
    {
        "slug": "fincore-ledger-django",
        "title": "FinCore Ledger & REST Analytics",
        "subtitle_ru": "Финансовый REST API и анализатор транзакций на Django & DRF",
        "subtitle_uz": "Django & DRF asosidagi moliyaviy REST API va tranzaksiyalar tahlilchisi",
        "description_ru": "Бэкенд двойной бухгалтерской записи для учёта мультивалютных операций (UZS, USD, EUR). Строгий контроль целостности балансов на уровне транзакций PostgreSQL и гибкие отчёты через Django REST Framework.",
        "description_uz": "Ko‘p valyutali (UZS, USD, EUR) operatsiyalarni hisobga olish uchun ikki yoqlama buxgalteriya backend tizimi. PostgreSQL tranzaksiyalari darajasida balans nazorati.",
        "architecture_ru": "Использованы блокировки SELECT ... FOR UPDATE для предотвращения состояния гонки (race conditions) при параллельных списаниях средств со счёта.",
        "architecture_uz": "Hisobdan parallel mablag‘ yechishda race condition holatlarining oldini olish uchun SELECT ... FOR UPDATE blokirovkalaridan foydalanilgan.",
        "metrics": "ACID transactions · 100% core coverage",
        "year": "2025",
        "accent": "violet",
        "image": "project_fincore.jpg",
        "tags": "Python, Django, DRF, PostgreSQL, Pytest, Git",
        "github_url": "https://github.com/MusulmanMM008",
        "code_filename": "ledger_services.py",
        "code_language": "python",
        "code_preview": '''from django.db import transaction
from django.db.models import F


@transaction.atomic
def transfer_funds(*, source_id: int, target_id: int, amount_tiyin: int) -> LedgerEntry:
    accounts = list(
        Account.objects.select_for_update()
        .filter(id__in=[source_id, target_id])
        .order_by("id")
    )
    source = next(a for a in accounts if a.id == source_id)
    if source.balance_tiyin < amount_tiyin:
        raise InsufficientFundsError("Insufficient UZS balance")

    Account.objects.filter(id=source_id).update(balance_tiyin=F("balance_tiyin") - amount_tiyin)
    Account.objects.filter(id=target_id).update(balance_tiyin=F("balance_tiyin") + amount_tiyin)
    return LedgerEntry.objects.create(source_id=source_id, target_id=target_id, amount_tiyin=amount_tiyin)''',
    },
]
