import discord

from conf import TOKEN


class BotClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {self.user}')
        invite = await self.fetch_invite('https://discord.gg/dpy')
        print(invite.approximate_member_count)

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')



client = BotClient()

client.run(TOKEN)
