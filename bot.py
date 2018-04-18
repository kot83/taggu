#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
import tags

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('t '), **kwargs)
        self.tags = tags
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, e))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        await bot.change_presence(activity=discord.Game(name='t help'))

bot = Bot()

# write general commands here

bot.run(config.token)

