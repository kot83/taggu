    bot.add_cog(Tags(bot))
m discord.ext import commands
import discord
import datetime

class Tags:
    """The tag system."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def setup(self, ctx):
        try:
            tags = await self.bot.tags.get_tags(str(ctx.guild.id))
        except:
            await self.bot.tags.initiate_guild(str(ctx.guild.id))
            return await ctx.send('Guild has been successfully set up!')
        await ctx.send('Guild already set up!')

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag: str=None):
        tags = await self.bot.tags.get_tags(str(ctx.guild.id))

        if tag is None:
            return await ctx.send(tags['help']['content'])
        
        tag = tags.get(tag, None)

        if tag is not None:
            await ctx.send(tag['content'])
        else:
            await ctx.send('Tag not found')

    @tag.command()
    async def owner(self, ctx, *, tag: str=None):
        tags = await self.bot.tags.get_tags(str(ctx.guild.id))

        if tag is None:
            return

        tag = tags.get(tag)
        
        if tag is not None:
            await ctx.send(tag.get('author', 'Could not find tag owner'))
        else:
            await ctx.send('Tag not found')

    @tag.command()
    async def create(self, ctx, tag: str, *, content: str):
        tags = await self.bot.tags.get_tags(str(ctx.guild.id))

        if tags.get(tag) is not None:
            await ctx.send(f'Tag `{tag}` already exists')
        else:
            tag = {'author': str(ctx.author.id), 'content': content, 'name': tag, 'timestamp': datetime.datetime.now()}
            await self.bot.tags.edit_tag(str(ctx.guild.id), tag)
            await ctx.send('Tag added successfully')

    @tag.command()
    async def edit(self, ctx, tag: str, *, content: str):
        tags = await self.bot.tags.get_tags(str(ctx.guild.id))
        name = tag
        tag = tags.get(tag)

        if tag.get('author') != str(ctx.author.id):
            await ctx.send('You do not own this tag!')
        else:
            tag = {'author': tag['author'], 'content': content, 'name': name, 'timestamp': datetime.datetime.now()}
            await self.bot.tags.edit_tag(str(ctx.guild.id), tag)
            await ctx.send(f'Tag `{name}` edited successfully')


    @tag.command()
    async def delete(self, ctx, *, tag: str):
        tags = await self.bot.tags.get_tags(str(ctx.guild.id))

        if tags.get(tag) is not None:
            if tags.get(tag)['author'] != str(ctx.author.id):
                await ctx.send('You do not own this tag!')
            else:
                await self.bot.tags.del_tag(str(ctx.guild.id), tag)
                await ctx.send(f'Deleted tag `{tag}`')
        else:
            await ctx.send('Could not find that tag!')

def setup(bot):
    bot.add_cog(Tags(bot))

