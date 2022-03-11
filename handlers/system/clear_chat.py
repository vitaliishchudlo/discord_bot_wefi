from loader import bot


@bot.command()
async def clear(ctx, amount=10):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
