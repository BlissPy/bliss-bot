import datetime

import humanize


def humanize_command_cooldown(cooldown):
		return humanize.naturaltime(datetime.datetime.now() + datetime.timedelta(seconds=cooldown.retry_after))
