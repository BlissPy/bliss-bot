import datetime
import typing

import discord
from discord.ext import commands
import humanize

from utils import formatting

class CommandError:

	def __init__(self, exception):
		self.exception = exception

		self.ignored = (
			commands.CommandNotFound,
		)
		
		self.messages = {
			commands.MissingRequiredArgument: {"title": "Missing Argument", "description": "You are missing the required argument {0.param.name}. Please enter that parameter and try again.", "reset": True},
			commands.BadArgument: {"title": "Bad Argument", "description": "You passed a bad argument. If you are having trouble, refer to the help documentation for the command.", "reset": True},
			commands.BadUnionArgument: {"title": "Bad Or Missing Argument", "description": "You passed a bad argument or forgot an argument. If you are having trouble, refer to the help documentation for the command.", "reset": True},
			commands.UserInputError: {"title": "Input Error", "description": "Your input was invalid. If you are having trouble, refer to the help documentation for the command.", "reset": True},
			commands.CommandOnCooldown: {"title": "Command On Cooldown", "description": "That command is currently on a cooldown, **you can try again in {formatting.humanize_command_cooldown(0.cooldown)}**.", "reset": False},
			commands.MissingPermissions: {"title": "Missing Permissions", "description": "You are missing {0.missing_perms} which is/are required for this command."}, "reset": True,
			"unknown": {"title": "Error", "description": "An error occurred, that is all I know", "reset": True}
		}

	@property
	def reset_cooldown(self):
		return self.messages[type(self.exception)]["retry"]
	
	@property
	def _message(self):
		if type(self.exception) in self.messages:
			return self.messages[type(self.exception)]
		else:	
			return self.messages["unknown"]
	
	@property
	def ignored(self):
		return type(self.exception) in self.ignored
	
	@property
	def embed(self):
		return discord.Embed(title=self._message["title"], description=self._message["description"].format(self.exception), color=discord.Color.red())

	async def send_to(self, channel: typing.Union[commands.Context, discord.TextChannel]):
		await channel.send(embed=self.embed)


class ErrorHandler(commands.Cog, name="Error Handler", command_attrs=dict(hidden=True, checks=[commands.is_owner])):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, exception):
		error = CommandError(exception)
		
		if error.ignored:
			return
		
		if error.reset_cooldown:
			await ctx.command.reset_cooldown(ctx)
		
		await error.send_to(ctx)


def setup(bot):
	bot.add_cog(ErrorHandler(bot))
