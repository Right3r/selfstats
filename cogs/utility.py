import discord
from discord.ext import commands
from ext.colors import ColorNames
from PIL import Image
import io


class Utility:
    '''Useful commands to make your life easier'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='logout')
    async def _logout(self, ctx):
        '''
        Shuts down the selfbot,
        equivalent to a restart if you are hosting on heroku
        '''
        await ctx.send('`Selfbot Logging out...`')
        await self.bot.logout()

    @commands.command()
    async def dcolor(self, ctx, *, url):
        '''A command that gets the dominant color of an image url'''
        await ctx.message.delete()
        color = await ctx.get_dominant_color(url)
        string_col = ColorNames.color_name(str(color))
        info = f'`{str(color)}`\n`{color.to_rgb()}`\n`{str(string_col)}`'
        em = discord.Embed(color=color, title='Dominant Color', description=info)
        em.set_thumbnail(url=url)
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em.set_image(url="attachment://color.png")
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @commands.command()
    async def tinyurl(self, ctx, *, link: str):
        '''Makes a link shorter using the tinyurl api'''
        await ctx.message.delete()
        url = 'http://tinyurl.com/api-create.php?url=' + link
        async with ctx.session.get(url) as resp:
            new = await resp.text()
        emb = discord.Embed(color=await ctx.get_dominant_color(ctx.author.avatar_url))
        emb.add_field(name="Original Link", value=link, inline=False)
        emb.add_field(name="Shortened Link", value=new, inline=False)
        await ctx.send(embed=emb)

    @commands.command()
    async def hastebin(self, ctx, code):
        '''Hastebin-ify your code!'''
        async with ctx.session.post("https://hastebin.com/documents", data=code) as resp:
            data = await resp.json()
        await ctx.message.edit(content=f"Hastebin-ified! <https://hastebin.com/{data['key']}.py>")


def setup(bot):
    bot.add_cog(Utility(bot))
