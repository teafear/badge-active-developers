import os
import requests
from colorama import *
from discord import app_commands, Intents, Client, Interaction

def CheckTokenValidity(token: str) -> dict:
    response = requests.get("https://discord.com/api/v10/users/@me", headers = {"Authorization": f"Bot {token}"})
    return response.json()

print("main.py запущен")

while True:
    token = input("Введите токен вашего бота  ")
    data = CheckTokenValidity(token)

    if data.get("id", None):
        break

    print("")
    print("Введён некорректный токен.")

print("")
print("Введён валидный токен.")
print("Не закрывайте консоль около 24-48 часов...")
print("")

class Badge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild = None)

client = Badge(intents = Intents.none())

@client.event
async def on_ready():
    print("Бот успешно активирован.")
    print(f"{client.user} | {client.user.id}")
    print(" ")
    print(f"Ссылка для приглашения бота на сервер:")
    print(f"> https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot")
    print(" ")

@client.event
async def on_error():
    print("Во время выполнения произошла ошибка.")

    os._exit(0)

@client.tree.command()
async def getbadge(interaction: Interaction):
    print(f"Команда была использована пользователем {interaction.user}.")

    await interaction.response.send_message(
        f"Приветствую, **{interaction.user}**, спасибо за использование этого бота.\n"
        "__**Когда я смогу получить значок?**__\n"
        "Получение доступа к значку занимает до 24 часов, т.к. проверка происходит раз в сутки.\n"
        "\n"
        "__**Как забрать значок**__\n"
        "После того как прошло 24 часа нужно перейти по ссылке: https://discord.com/developers/active-developer и заполнить форму.\n"
        "Если вы сделали всё правильно значок автоматически появится у вас в аккаунте.\n"
        )
    
    print("Чтобы забрать значок заполните форму по ссылке: https://discord.com/developers/active-developer")
    print("Получение доступа к форме занимает до 24 часов.")
    
    await interaction.client.close()
    await interaction.client.clear()
    os._exit(0)

client.run(token)