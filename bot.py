#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
import tags
import datetime

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


bot = Bot()

# write general commands here
@bot.group(invoke_without_command=True)
async def tag(ctx, *, tag: str=None):
    tags = await bot.tags.get_tags(str(ctx.guild.id))

    if tag is None:
        return await ctx.send(tags['help']['content'])
    
    tag = tags.get(tag, None)

    if tag is not None:
        await ctx.send(tag['content'])
    else:
        await ctx.send('Tag not found')

@tag.command()
async def owner(ctx, *, tag: str=None):
    tags = await bot.tags.get_tags(str(ctx.guild.id))

    if tag is None:
        return

    tag = tags.get(tag)
    
    if tag is not None:
        await ctx.send(tag.get('author', 'Could not find tag owner'))
    else:
        await ctx.send('Tag not found')

@tag.command()
async def create(ctx, tag: str, *, content: str):
    tags = await bot.tags.get_tags(str(ctx.guild.id))

    if tags.get(tag) is not None:
        await ctx.send(f'Tag `{tag}` already exists')
    else:
        tag = {'author': str(ctx.author.id), 'content': content, 'name': tag, 'timestamp': datetime.datetime.now()}
        await bot.tags.edit_tag(str(ctx.guild.id), tag)
        await ctx.send('Tag added successfully')

@tag.command()
async def edit(ctx, tag: str, *, content: str):
    tags = await bot.tags.get_tags(str(ctx.guild.id))
    name = tag
    tag = tags.get(tag)

    if tag.get('author') != str(ctx.author.id):
        await ctx.send('You do not own this tag!')
    else:
        tag = {'author': tag['author'], 'content': content, 'name': name, 'timestamp': datetime.datetime.now()}
        await bot.tags.edit_tag(str(ctx.guild.id), tag)
        await ctx.send(f'Tag `{name}` edited successfully')


@tag.command()
async def delete(ctx, *, tag: str):
    tags = await bot.tags.get_tags(str(ctx.guild.id))

    if tags.get(tag) is not None:
        if tags.get(tag)['author'] != str(ctx.author.id):
            await ctx.send('You do not own this tag!')
        else:
            await bot.tags.del_tag(str(ctx.guild.id), tag)
            await ctx.send(f'Deleted tag `{tag}`')
    else:
        await ctx.send('Could not find that tag!')

bot.run(config.token)
