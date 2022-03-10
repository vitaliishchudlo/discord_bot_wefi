from discord_bot_wefi.loader import bot


@bot.command()
async def test(ctx, amount=50):
    message = await ctx.reply('mesage')
    print(message.id)

    # await ctx.message.delete()
    # await ctx.channel.purge(limit=amount)

    message = await ctx.channel.fetch_message(951222622459420692)
    await message.edit(content="the new content of the message")

