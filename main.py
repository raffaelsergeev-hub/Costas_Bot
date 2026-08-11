import asyncio
import os
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, or_f

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = 7940715245
router = Router()

if not TOKEN:  # check TOKEN
    raise ValueError("Нету Токена")

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )
dp = Dispatcher()


class BookingForm(StatesGroup):
    name = State()  # Шаг 1: Ожидание имени
    category = State()  # Шаг: категория
    phone = State()  # Шаг 2: Ожидание телефона
    dates = State()  # Шаг 3: Ожидание дат заезда
    other = State()


# клавиатура
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Заявка на бронирование")],
            [KeyboardButton(text="Об отеле")],
            [KeyboardButton(text="Контакты")],
            [KeyboardButton(text="Номера")],
            [KeyboardButton(text="Частые вопросы")],
            [KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Конференц-зал")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите пункт из меню"

    )


def booking_bottoms() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Супериор панорамный (22 м²)", callback_data="cat_standard")],
            [InlineKeyboardButton(text="Делюкс (30 м²)", callback_data="cat_deluxe")],
            [InlineKeyboardButton(text="Люкс Классический (50 м²)", callback_data="cat_suite")],

        ]
    )


def rooms_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Делюкс (30 м²)", callback_data="room_deluxe")],
            [InlineKeyboardButton(text="Супериор панорамный (22 м²)", callback_data="room_superior")],
            [InlineKeyboardButton(text="Люкс Классический (50 м²)", callback_data="room_suite")],
            [InlineKeyboardButton(text="🔴 Оставить заявку на бронь", callback_data="start_booking_fsm")]
        ]
    )


def faq_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏰ Время заезда и выезда", callback_data="faq_time")],
            [InlineKeyboardButton(text="🍳 Как производится питание?", callback_data="faq_breakfast")],
            [InlineKeyboardButton(text="🚗 Есть ли парковка?", callback_data="faq_parking")]
        ]
    )


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back")],
        ]
    )


# сообщения
def text_home() -> str:
    return (
        "Добрый день! Буду рад помочь вам.\nПрошу вас, выберете пункт из меню:"
    )


def text_hotel() -> str:
    return (
        "<b>Отель КОСТАС 4★</b> — новый отель в центре Санкт-Петербурга, "
        "расположенный на пересечении Невского проспекта и тихой улицы Профессора Ивашенцова. 🏛\n\n"
        "• Просторные светлые номера от 30 м² с уюцтными эркерами и собственными террасами.\n"
        "• Превосходные завтраки («шведский стол» и по меню) из свежих продуктов.\n"
        "• Собственная подземная парковка, лобби-бар, фитнес-центр и прачечная.\n"
        "• Искренний сервис и гостеприимная атмосфера для каждого гостя!"
    )


def text_rooms_start() -> str:
    return ("Выберите интересующую вас категорию номера из списка ниже:")


def text_contacts() -> str:
    return (
        "📍 <b>Адрес:</b>\n191167, Санкт-Петербург, ул. Профессора... Ивашенцова, 2А\n\n"
        "📞 <b>Контакты отеля:</b>\n"
        "• Отель: +7 (812) 635-02-02, +7 (921) 962-11-11\n"
        "• Ресторан: +7 (812) 710-23-90, +7 (921) 646-38-18\n"
        "• Мероприятия: +7 (812) 710-24-22, +7 (921) 090-78-02\n\n"
        "💬 Доступна связь через Max, Telegram по указанным мобильным номерам!"
    )


def text_faq_start():
    return 'Часто задаваемые вопросы. Выберите интересующую тему:'


def text_faq_time():
    return (
        "⏰ <b>Время заезда и выезда:</b>\n\n"
        "• Заезд в отель начинается с <b>14:00</b>.\n"
        "• Выезд из номеров осуществляется до <b>12:00</b>.\n\n"
        "Возможность раннего заезда или позднего выезда уточняйте у администратора."
    )


def text_faq_breakfast():
    return (
        "🍽️ **Завтраки и Лобби-бар в отеле KOSTAS 4***\n\n"
        "🍳 **Завтраки «шведский стол»**\n"
        "Проходят ежедневно в ресторане отеля. В меню: мясные и рыбные деликатесы, сыры, "
        "домашний йогурт, свежая выпечка и десерты. По выходным и праздникам гостей бесплатно "
        "угощают шампанским без ограничений 🥂\n"
        "• **Будни:** с 07:30 до 11:00\n"
        "• **Выходные:** с 07:30 до 12:00\n"
        "• **Стоимость:** 1500 рублей (для детей до 2 лет — бесплатно).\n"
        "*Также доступен заказ ранних завтраков по меню a la carte в номер круглые сутки.*\n\n"
        "🍸 **Лобби-бар**\n"
        "• **Режим работы:** круглосуточно (24/7).\n"
        "• Атмосфера сдержанной роскоши, авторские коктейли, винная карта, согревающие напитки "
        "и полноценное меню европейской и средиземноморской кухни для позднего ужина или деловой встречи."
    )


def text_faq_parking():
    return (
        "🚗 <b>Парковка:</b>\n\n"
        "Да, у отеля есть <b>собственная подземная парковка</b>.\n"
        "Вы можете оставить свой автомобиль в безопасности на время проживания.\n"
        "(Стоимость и наличие мест уточняйте у администратора /contacts)"
    )


def text_confrerence_room() -> str:
    return (
        "🏢 **Конференц-пространства отеля KOSTAS 4***\n\n"
        "К вашим услугам 4 современные площадки (всего более 300 кв. м):\n"
        "• **Большой зал** (200 кв. м) — до 200 участников для масштабных событий.\n"
        "• **Конференц-фойе** (68 кв. м) — до 50 человек для велкам-зон и кофе-брейков.\n"
        "• **Малый зал** (50 кв. м) — до 32 гостей для камерных встреч и воркшопов.\n"
        "• **Переговорная** (24 кв. м) — до 12 человек для закрытых совещаний.\n\n"
        "🖥️ **Включено в стоимость:** проектор, экран, звукоусиление, микрофоны, кликер и Wi-Fi.\n"
        "🍽️ **Питание:** ресторанная служба организует кофе-брейки, ланчи и банкеты.\n"
        "Меню лобби-бара:https://kostashotel.ru/restaurant/bar-2/"

    )


def text_help():
    return (
        "❓ <b>Справка по командам отель-бота:</b>\n\n"
        "• /start или кнопка <b>Меню</b> — вернуться в главное меню\n"
        "• /hotel — узнать подробнее об отеле КОСТАС 4★\n"
        "• /contacts — посмотреть адрес и телефоны\n"
        "• /help — вызвать это меню помощи\n\n"
        "💡 Для удобства перемещения пользуйтесь кнопками на экране."
    )


# о номерах
def text_rooms_deluxe() -> str:
    return (
        "🛏 <b>Категория: Делюкс</b>\n"
        "📐 <b>Площадь:</b> 30 м²\n"
        "👥 <b>Размещение:</b> 2-х местный\n\n"
        "• Кровать размера «king-size» или две односпальные кровати\n"
        "• Вид на тихий внутренний двор\n"
        "• Телевизор, кондиционер, сейф, мини-бар, чайная станция\n"
        "• Ванная или душ, бесплатный WI-FI\n"
        "• Возможны вариации номера с панорамным видом и эркером\n"
        "• (Наличие проверяйте на сайте или у администратора /contacts)"
    )


def text_rooms_superior() -> str:
    return (
        "🛏 <b>Категория: Супериор панорамный вид на город</b>\n"
        "📐 <b>Площадь:</b> 22 м²\n"
        "👥 <b>Размещение:</b> 2-х местный\n\n"
        "• Кровать размера «king-size» или две односпальные кровати\n"
        "• Панорамный вид на исторический центр города\n"
        "• Телевизор с плоским экраном, кондиционер, душ\n"
        "• Сейф, мини-бар, чайная станция, бесплатный WI-FI\n"
        "• Возможны вариации номера с панорамным видом и эркером\n"
        "• (Наличие проверяйте на сайте или у администратора /contacts)"
    )


def text_rooms_suite() -> str:
    return (
        "🛏 <b>Категория: Двухкомнатный Люкс Классический</b>\n"
        "📐 <b>Площадь:</b> 50 м²\n"
        "👥 <b>Размещение:</b> до 4-х человек\n\n"
        "• Кровать размера «king-size» и уютный диван в гостевой зоне\n"
        "• Вид на тихий зеленый внутренний двор\n"
        "• Кофемашина, чайная станция, мини-бар, сейф, кондиционер\n"
        "• Ванная и душ, телевизор с плоским экраном, бесплатный WI-FI\n"
        "• Возможны вариации номера с панорамным видом и эркером\n"
        "• (Наличие проверяйте на сайте или у администратора /contacts)"
    )


# команды
@dp.message(Command('start'))
@dp.message(F.text == 'Меню')
async def start(message: types.Message):
    await message.answer(text_home(), reply_markup=main_menu())


@dp.message(Command('hotel'))
@dp.message(F.text == "Об отеле")
async def hotel(message: types.Message):
    await message.answer(text_hotel(), reply_markup=main_menu())


@dp.message(Command('contacts'))
@dp.message(F.text == "Контакты")
async def contacts(message: types.Message):
    await message.answer(text_contacts(), reply_markup=main_menu())
    await message.answer_contact(
        phone_number='+79219621111',
        first_name='Reception',
    )


@dp.message(Command('rooms_start'))
@dp.message(F.text == "Номера")
async def show_rooms(message: types.Message):
    await message.answer(text_rooms_start(), reply_markup=rooms_menu())


# deluxe
@dp.callback_query(F.data == "room_deluxe")
async def process_room_deluxe(callback: types.CallbackQuery):
    await callback.message.delete()
    photo_url = "https://kostashotel.ru/wp-content/uploads/2022/05/a-9151.jpg"
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text_rooms_deluxe(),
        reply_markup=back_menu()
    )
    await callback.answer()


# superior
@dp.callback_query(F.data == "room_superior")
async def process_room_superior(callback: types.CallbackQuery):
    await callback.message.delete()
    photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR98TJrhUKjf1_Y3oemM_8pVFbiA7nnDL9nnPm0lHzCIQ&s=10"
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text_rooms_superior(),
        reply_markup=back_menu())
    await callback.answer()


# suit
@dp.callback_query(F.data == "room_suite")
async def process_room_suite(callback: types.CallbackQuery):
    await callback.message.delete()
    photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmY7TQzqIUjloKT1k4RniKZ2iP2_vLO0ZWjbEYNmfdLMV2Nur1gVoMYJI&s=10"
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text_rooms_suite(),
        reply_markup=back_menu())
    await callback.answer()


# в меню номеров
@dp.callback_query(F.data == "back")
async def process_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text_rooms_start(), reply_markup=rooms_menu())
    await callback.answer()


# частые вопросы
@dp.message(Command('faq'))
@dp.message(F.text == "Частые вопросы")
async def show_faq(message: types.Message):
    await message.answer(text_faq_start(), reply_markup=faq_menu())


# check in time and check out time
@dp.callback_query(F.data == "faq_time")
async def process_faq_time(callback: types.CallbackQuery):
    await callback.message.answer(text_faq_time())
    await callback.answer()


# new info
# breakfast
@dp.callback_query(F.data == "faq_breakfast")
async def process_faq_breakfast(callback: types.CallbackQuery):
    await callback.message.answer(text_faq_breakfast())
    await callback.answer()


# parking
@dp.callback_query(F.data == "faq_parking")
async def process_faq_parking(callback: types.CallbackQuery):
    await callback.message.answer(text_faq_parking())
    await callback.answer()


@dp.message(Command('help'))
@dp.message(F.text == 'Помощь')
async def show_help(message: types.Message):
    await message.answer(text_help(), reply_markup=main_menu())


@dp.message(Command('conference'))
@dp.message(F.text == 'Конференц-зал')
async def show_conference(message: types.Message):
    await message.answer(text_confrerence_room(), reply_markup=main_menu())


# 1. СТАРТ ИЗ ИНЛАЙН КНОПКИ
@dp.callback_query(F.data == "start_booking_fsm")
async def process_inline_booking(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Убираем часики
    await state.clear()  # Очищаем старые состояния
    if isinstance(callback.message, Message):
        await callback.message.answer("Отлично! Давайте оформим заявку. Введите ваше ФИО:")
    await state.set_state(BookingForm.name)


# 2. СТАРТ ИЗ ТЕКСТОВОГО МЕНЮ ИЛИ КОМАНДЫ
@dp.message(or_f(Command('booking'), F.text == "Заявка на бронирование"))
async def start_booking(message: Message, state: FSMContext):
    await state.clear()  # Очистка состояния
    await message.answer("Отлично! Давайте оформим заявку. Введите ваше ФИО:")
    await state.set_state(BookingForm.name)


# 3. ЛОВИМ ФИО -> ПЕРЕХОД К КАТЕГОРИИ
@dp.message(BookingForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    # Отправляем инлайн-кнопки для выбора категории
    await message.answer("Выберите категорию номера:", reply_markup=booking_bottoms())
    await state.set_state(BookingForm.category)


# 4. ЛОВИМ КАТЕГОРИЮ (ЧЕРЕЗ CALLBACK) -> ПЕРЕХОД К ТЕЛЕФОНУ
@dp.callback_query(BookingForm.category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    categories = {
        "cat_standard": "Супериор",
        "cat_deluxe": "Делюкс",
        "cat_suite": "Люкс"
    }
    chosen_cat = categories.get(callback.data or "cat_standard", "Не указана")
    await state.update_data(category=chosen_cat)
    await callback.answer()
    await callback.message.answer(f"Выбрано: {chosen_cat}\n\nТеперь введите ваш номер телефона:")
    await state.set_state(BookingForm.phone)


# 5. ЛОВИМ ТЕЛЕФОН -> ПЕРЕХОД К ДАТАМ
@dp.message(BookingForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Укажите желаемые даты заезда и выезда (например, 12.10 - 15.10):")
    await state.set_state(BookingForm.dates)


# 6. ЛОВИМ ДАТЫ -> ПЕРЕХОД К ПРИМЕЧАНИЯМ (OTHER)
@dp.message(BookingForm.dates)
async def process_dates(message: Message, state: FSMContext):
    await state.update_data(dates=message.text)
    await message.answer("Прошу, укажите дополнительную информацию, если необходимо (или напишите 'нет'):")
    await state.set_state(BookingForm.other)


# 7. ФИНАЛ: ЛОВИМ ДОП. ИНФОРМАЦИЮ -> ОТПРАВКА АДМИНАМ -> СБРОС FSM
@dp.message(BookingForm.other)
async def process_other_and_finish(message: types.Message, state: FSMContext):
    # 1. Сначала записываем инфу из последнего шага
    await state.update_data(other=message.text)

    # 2. Вытаскиваем всё, что насобирали в состоянии
    user_data = await state.get_data()
    username = f"@{message.from_user.username}" if message.from_user.username else "Скрыт"

    # 3. Формируем портянку для админов
    admin_text = (
        f"🔔 **НОВАЯ ЗАЯВКА НА БРОНИРОВАНИЕ**\n\n"
        f"👤 **ФИО:** {user_data.get('name')}\n"
        f"🏨 **Категория:** {user_data.get('category')}\n"
        f"📞 **Телефон:** {user_data.get('phone')}\n"
        f"📅 **Даты:** {user_data.get('dates')}\n"
        f"🆔 **Telegram ID:** `{message.from_user.id}`\n"
        f"🔗 **Ссылка:** {username}\n"
        f"📝 **Примечания:** {user_data.get('other')}"
    )

    # 4. Отправляем админу через глобальный объект bot
    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Админ-чат недоступен: {e}")

    # 5. Радуем гостя
    await message.answer("Спасибо! Ваша заявка успешно отправлена менеджерам. Ожидайте звонка.")

    # 6. Гасим FSM, возвращаем юзера в обычный мир
    await state.clear()


@dp.message()
async def echo_answer(message: types.Message):
    await message.answer(text='Простите, но я не понимаю, что вы хотите\nВернемся к началу? /start')


@dp.errors()
async def global_error_handler(event: types.ErrorEvent):
    print(f"⚠️ Ошибка в боте: {event.exception}")
    try:
        await event.update.message.answer(
            "Произошла небольшая ошибка, но я уже в порядке! 🛠\nВернемся в меню: /start"
        )
    except Exception:
        pass
    return True


# запуск бота
async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
