from fastapi import FastAPI, status
import uvicorn
import asyncio

import discord
from discord import Interaction
from discord.ext import commands
from discord.app_commands import autocomplete
from discord.app_commands import Choice, choices, Group

from dotenv import load_dotenv
import os

import service.record as r
import service.staff as s
import service.table as t

# API 伺服器
app = FastAPI()

@app.get("/check/{rfid}")
async def check(rfid: str):
    try:
        r.check_io(rfid)
        return status.HTTP_200_OK
    except Exception as e:
        print(e)
        return status.HTTP_404_NOT_FOUND
    
@app.get("/new/{name}/{rfid}")
async def set(name: str, rfid: str):
    try:
        s.new_staff(name, rfid)
        return status.HTTP_200_OK
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST


# Discord 機器人
bot = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.all()
)

staff_group = Group(name="staff", description="員工管理")
record_group = Group(name="record", description="紀錄管理")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"登入使用者 {bot.user}")

# - Staff
async def staff_autocomplete(inter: Interaction, current: str):
    try:
        staffs = s.get_all_staff()
        return [
            Choice(name=staff.name, value=staff.name)
            for staff in staffs if current in staff.name
        ]
    except Exception as e:
        print(f"Autocomplete 錯誤: {e}")
        return []

@staff_group.command(description="移除員工")
@autocomplete(staff_name=staff_autocomplete)
async def remove(inter: Interaction, staff_name:str):
    s.remove_staff(staff_name)

    await inter.response.send_message(f"已移除員工: {staff_name}")


@staff_group.command(description="取得當前已簽退/簽到員工")
@choices(status=[
    Choice(name="已簽到", value="check_in"),
    Choice(name="已簽退", value="check_out")
])
async def check(inter: Interaction, status: Choice[str]):
    staff = s.get_staff_by_io(status.value)
    if not staff:
        await inter.response.send_message(f"當前無{status.name}員工")
    else:
        table = t.make_staff_table(staff)
        await inter.response.send_message(
            f"## {status.name}員工\n" + \
            f"```{table}```"
        )

# - Record

@record_group.command(description="查詢所有打卡紀錄")
async def all(inter: Interaction):
    record = r.get_all_record()
    if not record:
        await inter.response.send_message("當前無打卡紀錄")
    else:
        table = t.make_record_table(record)
        await inter.response.send_message(
            "所有打卡紀錄\n" + \
            f"```{table}```"
        )

@record_group.command(description="查詢今日打卡紀錄")
async def today(inter: Interaction):
    record = r.get_record_today()
    if not record:
        await inter.response.send_message("今日無打卡紀錄")
    else:
        table = t.make_record_table(record)
        await inter.response.send_message(
            "今日打卡紀錄\n" + \
            f"```{table}```"
        )

@record_group.command(description="查詢員工打卡紀錄")
@autocomplete(staff_name=staff_autocomplete)
async def staff(inter: Interaction, staff_name: str):
    record = r.get_record_by_name(staff_name)
    if not record:
        await inter.response.send_message("員工無打卡紀錄")
    else:
        table = t.make_record_table(record)
        await inter.response.send_message(
            f"{staff_name} 打卡紀錄\n" + \
            f"```{table}```"
        )



bot.tree.add_command(staff_group)
bot.tree.add_command(record_group)

# 主函數
async def main():
    discord.utils.setup_logging()
    load_dotenv()
    config = uvicorn.Config(app=app)
    server = uvicorn.Server(config)

    await asyncio.gather(
        server.serve(),
        bot.start(os.environ["BOT_TOKEN"])
    )

asyncio.run(main())