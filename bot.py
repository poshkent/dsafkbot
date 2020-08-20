import config
import datetime
import discord
import asyncio
import os
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import Activity, ActivityType

prefix = config.prefix
col = config.color
role_channel_id = config.role_channel_id
muterole_id = config.muterole_id
greeting_channel_id = config.greeting_channel_id
newbie_role_id = config.newbie_role_id

Bot = commands.Bot(command_prefix=prefix)


async def status_task():
	while True:
			offset = datetime.timezone(datetime.timedelta(hours=3))
			minsk_time = datetime.datetime.now(offset)
			await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{prefix} | {minsk_time.hour} : {minsk_time.minute}, {minsk_time.day}.{minsk_time.month}.{minsk_time.year}'))
			await asyncio.sleep(60)




@Bot.event
async def on_ready():
	Bot.loop.create_task(status_task())
	print("Бот запущен")


@Bot.command() 
async def info(ctx, member:discord.Member): 
	emb = discord.Embed(title = 'Информация о чепухе', color = col )
	emb.add_field(name = "Когда присоеденился", value = member.joined_at, inline = False)
	emb.add_field(name = "Акк был создан", value = member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"), inline = False)
	emb.add_field(name = "Ник", value = member.display_name, inline = False)
	emb.add_field(name = "Статус", value = member.activity, inline = False)
	emb.add_field(name = "Состояние", value = member.status, inline = False)
	emb.add_field(name = "Роли и их id", value = member.roles, inline = False)
	emb.add_field(name = "Упоминание", value = member.mention, inline = False)
	emb.add_field(name = "Состояние войса", value = member.voice, inline = False)
	emb.set_thumbnail(url = member.avatar_url)
	emb.set_footer(text = f"Вызвал {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
	emb.set_author(name = ctx.message.author, icon_url = ctx.message.author.avatar_url)
	await ctx.send(embed = emb) 



@Bot.command() 
async def all(ctx): 
	emb = discord.Embed(title = 'Информация о коммандах', color = col )
	emb.add_field(name = "info", value = "Показывает информацию о ком-либо", inline = False)
	emb.add_field(name = "mute", value = "Выдаёт роль MUTED на время в минутах", inline = False)
	emb.add_field(name = "unmute", value = "Забирает роль MUTED", inline = False)
	emb.add_field(name = "clear", value = "Удаляет указанное колличество сообщений", inline = False)
	emb.set_footer(text=f"Вызвал {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await ctx.send(embed = emb) 




@Bot.command()
@commands.has_permissions(view_audit_log = True)
async def mute(ctx,member:discord.Member, time:int ,reason):
	channel = Bot.get_channel(role_channel_id)
	muterole = discord.utils.get(ctx.guild.roles, id = muterole_id)
	emb = discord.Embed(title = "Мут", color = col)
	emb.add_field(name = "Нарушитель", value = member.mention, inline = False)
	emb.add_field(name = "Время в минутах", value = time, inline = False)
	emb.add_field(name = "Причина", value = reason, inline = False)
	emb.set_thumbnail(url=member.avatar_url)
	emb.set_footer(text=f"Выдал мут {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await member.add_roles(muterole)
	await channel.send(embed = emb)
	await asyncio.sleep(time * 60)
	await member.remove_roles(muterole)


@Bot.command()
@commands.has_permissions(view_audit_log = True)
async def unmute(ctx,member:discord.Member):
	channel = Bot.get_channel(role_channel_id)
	muterole = discord.utils.get(ctx.guild.roles, id = muterole_id)
	emb = discord.Embed(title = "Размут", color = col)
	emb.add_field(name = "Нарушитель", value = member.mention, inline = False)
	emb.set_thumbnail(url=member.avatar_url)
	emb.set_footer(text=f"Размутил {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
	emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await channel.send(embed = emb)
	await member.remove_roles(muterole)


@Bot.command()
@commands.has_permissions(view_audit_log = True)
async def clear(ctx, amount = 5):
	deleted = await ctx.message.channel.purge(limit = amount + 1)




@Bot.event
async def on_member_join(member):
	channel = Bot.get_channel(greeting_channel_id)
	newbie = discord.utils.get(ctx.guild.roles, id = newbie_role_id)
	await member.add_roles(newbie)
	await channel.send(f"{member.mention} дарова ебать")



@Bot.command()
@commands.has_permissions(view_audit_log = True)
async def spamm(ctx, member:discord.Member, amount = 50):
	deleted = await ctx.message.channel.purge(limit = 1)
	emb = discord.Embed(title = 'Это тебе сука спам прилелел', color = col )
	emb.add_field(name = "Тебе сука", value = member.mention, inline = False)
	x = 0
	while x < amount:
		await member.send(embed = emb)
		x += 1


@Bot.command()
@commands.has_permissions(view_audit_log = True)
async def spamchik(ctx, slovo, amount = 50):
	deleted = await ctx.message.channel.purge(limit = 1)
	x = 0
	while x < amount:
		await ctx.send(slovo)
		x += 1

token = os.environ.get('BOT_TOKEN')
Bot.run(str(token))
