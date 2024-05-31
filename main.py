from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from state import AddUserState, GetUserState, UpdateUserForm
from keyboard import main_menu, next_menu, update_menu
from save import db
from logging import basicConfig, getLogger, INFO
import os

basicConfig(level=INFO)
log = getLogger()

storage = MemoryStorage()

BOT_TOKEN = "7021103475:AAEdeDmISk1idZKo4gYBabNyqu2tLBQhz0U"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

if not os.path.exists('photos'):
    os.makedirs('photos')


@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    await message.answer("Botga xush kelibsan ukam",
                         reply_markup=main_menu())


@dp.message_handler(Text(equals="User"))
async def start_bot(message: types.Message):
    await message.answer("Botga xush kelibsan ukam",
                         reply_markup=next_menu())


@dp.message_handler(Text(equals="Get user"), state=None)
async def start_bot(message: types.Message):
    await message.answer("Idni tanlang")
    await GetUserState.id.set()


@dp.message_handler(state=GetUserState.id)
async def start_bot(message: types.Message, state: FSMContext):
    user = db.get_user(id=message.text)
    await message.answer_photo(photo=user[-1],
                               caption=f"{user[0]}: {user[1]}ning yoshi {user[2]}\n"
                                       f"Manzili {user[3]}")
    await state.finish()


@dp.message_handler(Text(equals="View users"))
async def start_bot(message: types.Message):
    users = db.show_users()
    for user in users:
        await message.answer_photo(photo=user[-1],
                                   caption=f"{user[1]}ning yoshi {user[2]}da\n"
                                           f"Manzili {user[3]}")


@dp.message_handler(Text(equals="Add user"), state=None)
async def start_bot(message: types.Message):
    await message.answer("Ismingizni kiriting",
                         reply_markup=ReplyKeyboardRemove())
    await AddUserState.name.set()


@dp.message_handler(state=UpdateUserForm.id)
async def process_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await UpdateUserForm.next()
    await message.reply("Yangi ismni kiriting (yoki /skip ni bosib o'tkazib yuboring):")


@dp.message_handler(state=UpdateUserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await UpdateUserForm.next()
    await message.reply("Yangi yoshni kiriting (yoki /skip ni bosib o'tkazib yuboring):")


@dp.message_handler(state=UpdateUserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await UpdateUserForm.next()
    await message.reply("Yangi addressni kiriting (yoki /skip ni bosib o'tkazib yuboring):")


@dp.message_handler(state=UpdateUserForm.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await UpdateUserForm.next()
    await message.reply("Yangi rasmni kiriting (yoki /skip ni bosib o'tkazib yuboring):")


@dp.message_handler(content_types=['photo'], state=UpdateUserForm.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file = await bot.download_file_by_id(photo.file_id)

    photo_path = f"photos/{photo.file_id}.png"
    with open(photo_path, 'wb') as f:
        f.write(photo_file.read())

    async with state.proxy() as data:
        data['photo'] = photo_path

    db.update_user(
        id=data['id'],
        name=data.get('name'),
        age=data.get('age'),
        address=data.get('address'),
        photo=data.get('photo')
    )

    await state.finish()
    await message.reply("Foydalanuvchi haqida ma'lumot yangilandi")


@dp.message_handler(state='*', commands='skip')
@dp.message_handler(Text(equals='skip', ignore_case=True), state='*')
async def process_skip(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'UpdateUserForm:name':
        await UpdateUserForm.next()
        await message.reply("Yangi yoshni kiriting (yoki /skip ni bosib o'tkazib yuboring):")
    elif current_state == 'UpdateUserForm:age':
        await UpdateUserForm.next()
        await message.reply("Yangi manzilni kiriting yoki /skip ni bosib o'tkazib yuboring):")
    elif current_state == 'UpdateUserForm:address':
        await UpdateUserForm.next()
        await message.reply("Yangi rasmni kiriting yoki /skip ni bosib o'tkazib yuboring):")
    elif current_state == 'UpdateUserForm:photo':
        async with state.proxy() as data:

            db.update_user(
                id=data['id'],
                name=data.get('name'),
                age=data.get('age'),
                address=data.get('address')
            )
        await state.finish()
        await message.reply("Foydalanuvchi haqida ma'lumot yangilandi")


@dp.message_handler(state=AddUserState.name)
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Yoshingizni kiriting")
    await AddUserState.next()


@dp.message_handler(state=AddUserState.age)
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Manzilingizni kiriting")
    await AddUserState.next()


@dp.message_handler(state=AddUserState.address)
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer("Rasmingizni kiriting")
    await AddUserState.next()


@dp.message_handler(state=AddUserState.photo, content_types="photo")
async def start_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await state.finish()
    await message.answer_photo(photo=data['photo'],
                               caption=f"{data['name']}ning yoshi {data['age']}da\n"
                                       f"Manzili {data['address']}")
    db.add_user(name=data['name'], age=data['age'], address=data['address'], photo=data['photo'])


@dp.message_handler(Text(equals="Update user"), state=None)
async def start_bot(message: types.Message):
    await message.answer("Foydalanuvchi haqida qaysi ma'lumotni almashtirasiz",
                         reply_markup=update_menu())
    await AddUserState.name.set()


@dp.message_handler(Text(equals="name"))
async def cmd_update(message: types.Message):
    await UpdateUserForm.id.set()
    await message.reply("Foydalanuvchining name ini kiriting")


@dp.message_handler(state=UpdateUserForm.name)
async def process_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await UpdateUserForm.next()
    await message.reply("Yangi ismni kiriting")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
