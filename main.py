import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN: # check TOKEN
    raise ValueError("Нету Токена")

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )
dp = Dispatcher()
#клавиатура
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Об отеле")],
            [KeyboardButton(text="Контакты")],
            [KeyboardButton(text="Номера")],
            [KeyboardButton(text="Частые вопросы")],
            [KeyboardButton(text="Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберете пункт из меню"

    )
def rooms_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Делюкс (30 м²)", callback_data="room_deluxe")],
            [InlineKeyboardButton(text="Супериор панорамный (22 м²)", callback_data="room_superior")],
            [InlineKeyboardButton(text="Люкс Классический (50 м²)", callback_data="room_suite")]
        ]
    )
def faq_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏰ Время заезда и выезда", callback_data="faq_time")],
            [InlineKeyboardButton(text="🍳 Как проходят завтраки?", callback_data="faq_breakfast")],
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
    return(
        "⏰ <b>Время заезда и выезда:</b>\n\n"
        "• Заезд в отель начинается с <b>14:00</b>.\n"
        "• Выезд из номеров осуществляется до <b>12:00</b>.\n\n"
        "Возможность раннего заезда или позднего выезда уточняйте у администратора."
    )
def text_faq_breakfast():
    return(
        "🍳 <b>Завтраки в отеле КОСТАС:</b>\n\n"
        "Каждое утро в ресторане отеля на 1-м этаже вас ждут прекрасные завтраки:\n"
        "• Формат: «шведский стол» и по меню.\n"
        "• Приготовлены из свежих продуктов высокого качества.\n"
        "• 🥂 <b>Бонус:</b> безлимитное шампанское по выходным на завтраках!"
    )
def text_faq_parking():
    return(
        "🚗 <b>Парковка:</b>\n\n"
        "Да, у отеля есть <b>собственная подземная парковка</b>.\n"
        "Вы можете оставить свой автомобиль в безопасности на время проживания.\n"
        "(Бронирование мест и их наличие уточняйте у администратора /contacts)"
    )
def text_help():
    return(
        "❓ <b>Справка по командам отель-бота:</b>\n\n"
        "• /start или кнопка <b>Меню</b> — вернуться в главное меню\n"
        "• /hotel — узнать подробнее об отеле КОСТАС 4★\n"
        "• /contacts — посмотреть адрес и телефоны\n"
        "• /help — вызвать это меню помощи\n\n"
        "💡 Для удобства перемещения пользуйтесь кнопками на экране."
    )
# о номерах
def text_rooms_deluxe() -> str:
    return(
        "🛏 <b>Категория: Делюкс</b>\n"
        "📐 <b>Площадь:</b> 30 м²\n"
        "👥 <b>Размещение:</b> 2-х местный\n\n"
        "• Кровать размера «king-size» или две односпальные кровати\n"
        "• Вид на тихий внутренний двор\n"
        "• Телевизор, кондиционер, сейф, мини-бар, чайная станция\n"
        "• Ванная или душ, бесплатный WI-FI\n"
        "• Возможны вариации номера с понорамным видом и эркером\n"
        "• (Наличие проверяйте на сайте или у администратора /contacts)"
    )
def text_rooms_superior() -> str:
    return(
        "🛏 <b>Категория: Супериор панорамный вид на город</b>\n"
        "📐 <b>Площадь:</b> 22 м²\n"
        "👥 <b>Размещение:</b> 2-х местный\n\n"
        "• Кровать размера «king-size» или две односпальные кровати\n"
        "• Панорамный вид на исторический центр города\n"
        "• Телевизор с плоским экраном, кондиционер, душ\n"
        "• Сейф, мини-бар, чайная станция, бесплатный WI-FI\n"
        "• Возможны вариации номера с понорамным видом и эркером\n"
        "• (Наличие проверяйте на сайте или у администратора /contacts)"
    )
def text_rooms_suite() -> str:
    return(
        "🛏 <b>Категория: Двухкомнатный Люкс Классический</b>\n"
        "📐 <b>Площадь:</b> 50 м²\n"
        "👥 <b>Размещение:</b> до 4-х человек\n\n"
        "• Кровать размера «king-size» и уютный диван в гостевой зоне\n"
        "• Вид на тихий зеленый внутренний двор\n"
        "• Кофемашина, чайная станция, мини-бар, сейф, кондиционер\n"
        "• Ванная и душ, телевизор с плоским экраном, бесплатный WI-FI\n"
        "• Возможны вариации номера с понорамным видом и эркером\n"
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

@dp.message(Command('rooms_start'))
@dp.message(F.text == "Номера")
async def show_rooms(message: types.Message):
    await message.answer(text_rooms_start(), reply_markup=rooms_menu())
# deluxe
@dp.callback_query(F.data == "room_deluxe")
async def process_room_deluxe(callback:types.CallbackQuery):
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
async def process_room_superior(callback:types.CallbackQuery):
    await callback.message.delete()
    photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR98TJrhUKjf1_Y3oemM_8pVFbiA7nnDL9nnPm0lHzCIQ&s=10"
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text_rooms_superior(),
        reply_markup=back_menu())
    await callback.answer()

#suit
@dp.callback_query(F.data == "room_suite")
async def process_room_suite(callback:types.CallbackQuery):
    await callback.message.delete()
    photo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmY7TQzqIUjloKT1k4RniKZ2iP2_vLO0ZWjbEYNmfdLMV2Nur1gVoMYJI&s=10"
    await callback.message.answer_photo(
        photo=photo_url,
        caption=text_rooms_suite(),
        reply_markup=back_menu())
    await callback.answer()
#в меню номеров
@dp.callback_query(F.data == "back")
async def process_back(callback:types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text_rooms_start(), reply_markup=rooms_menu())
    await callback.answer()
# частые вопросы
@dp.message(Command('faq'))
@dp.message(F.text == "Частые вопросы")
async def show_faq(message: types.Message):
    await message.answer(text_faq_start(), reply_markup=faq_menu())

#check in time and check out time
@dp.callback_query(F.data == "faq_time")
async def process_faq_time(callback:types.CallbackQuery):
    await callback.message.answer(text_faq_time())
    await callback.answer()

#breakfast
@dp.callback_query(F.data == "faq_breakfast")
async def process_faq_breakfast(callback:types.CallbackQuery):
    await callback.message.answer(text_faq_breakfast())
    await callback.answer()

#parking
@dp.callback_query(F.data == "faq_parking")
async def process_faq_parking(callback:types.CallbackQuery):
    await callback.message.answer(text_faq_parking())
    await callback.answer()
@dp.message(Command('help'))
@dp.message(F.text == 'Помощь')
async def show_help(message: types.Message):
    await message.answer(text_help(), reply_markup=main_menu())

@dp.message()
async def echo_answwer(message: types.Message):
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