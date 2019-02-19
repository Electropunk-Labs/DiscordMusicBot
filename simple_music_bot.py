import discord
from discord.ext.commands import Bot
from settings import BOT_TOKEN


class MusicBot:

    def __init__(self, token):
        self.bot = Bot(command_prefix=('!', '?'))
        self.token = token
        self.prepare_bot()
        self.player = None

    def run(self):
        self.bot.run(self.token)

    async def new_player(self, url):
        self.player = await self.voice.create_ytdl_player(url)
        self.player.start()

    def prepare_bot(self):
        @self.bot.command(name='play',
                          description="Starts playing a YouTube song",
                          brief="Play music",
                          aliases=['start', 'music', 'playmusic', 'jam', 'rockout'],
                          pass_context=True)
        async def play(context, url):

            # Example: 'https://www.youtube.com/watch?v=SXtYbaHP2As'

            # if bot is connected...
            #
            # state = VoiceState(bot)
            async def announce_song():
                await self.bot.say("Now playing: %s - %s" % (self.player.title, self.player.description))

            self.voice_channel = self.get_proper_channel('General')

            try:
                self.voice = await self.bot.join_voice_channel(self.voice_channel)
            except discord.ClientException as e:
                print("Client exception caught: %s" % e)
                await self.bot.say("I'm already in a channel!")

            if self.player is None:
                await self.new_player(url)
                await announce_song()
            else:
                self.player.stop()
                await self.new_player(url)
                await announce_song()

    def get_proper_channel(self, channel_name):
        for channel in self.bot.get_all_channels():
            if channel.name == channel_name and channel.type is discord.ChannelType.voice:
                return channel


if __name__ == '__main__':
    music_bot = MusicBot(BOT_TOKEN)
    music_bot.run()
