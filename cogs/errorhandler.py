import datetime

import discord
from discord.ext import commands
import humanize


class CommandError:

	def __init__(self, ctx, exception):
		self.ctx = ctx
		self.exception = exception

		self.messages = {
			commands.MissingRequiredArgument: {"title": "Missing Argument", "description": "You are missing the required argument {0.param.name}. Please enter that parameter and try again."},
			commands.BadArgument: {"title": "Bad Argument", "description": "You passed a bad argument. If you are having trouble, refer to the help documentation for the command."},
			commands.BadUnionArgument: {"title": "Bad Or Missing Argument", "description": "You passed a bad argument or forgot an argument. If you are having trouble, refer to the help documentation for the command."},
			commands.UserInputError: {"title": "Input Error", "description": "Your input was invalid. If you are having trouble, refer to the help documentation for the command."},
			commands.CommandOnCooldown: {"title": "Command On Cooldown", "description": "That command is currently on a cooldown, **you can try again in {self.humanize_cooldown(0.cooldown)}**."},
			commands.MissingPermissions: {"title": "Missing Permissions", "description": "You are missing {0.missing_perms} which is/are required for this command."},
			"unknown": {"title": "Error", "description": "An error occurred, that is all I know"}
		}

	@staticmethod
	def humanize_cooldown(cooldown):
		return humanize.naturaltime(datetime.datetime.now() + cooldown.retry_after)

	@property
	def embed(self):
		if type(self.exception) in self.messages:
			message = self.messages[type(self.exception)]
			return discord.Embed(title=message["title"], description=message["description"].format(self.exception), color=discord.Color.red())
		message = self.messages["unknown"]
		return discord.Embed(title=message["title"], description=message["description"], color=discord.Color.red())

	async def send_to(self, context):
		await context.send(embed=self.embed)


class ErrorHandler(commands.Cog, name="Error Handler", command_attrs=dict(hidden=True, checks=[commands.is_owner])):

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, exception):
		error = CommandError(ctx, exception)
		await error.send_to(ctx)


def setup(bot):
	bot.add_cog(ErrorHandler(bot))
