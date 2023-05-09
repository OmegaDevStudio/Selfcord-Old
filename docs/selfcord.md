# selfcord package

## Subpackages


* [selfcord.api package](selfcord.api.md)


    * [Subpackages](selfcord.api.md#subpackages)


        * [selfcord.api.voice package](selfcord.api.voice.md)


            * [Submodules](selfcord.api.voice.md#submodules)


            * [selfcord.api.voice.voice module](selfcord.api.voice.md#module-selfcord.api.voice.voice)


            * [Module contents](selfcord.api.voice.md#module-selfcord.api.voice)


    * [Submodules](selfcord.api.md#submodules)


    * [selfcord.api.errors module](selfcord.api.md#module-selfcord.api.errors)


        * [`DiscordException`](selfcord.api.md#selfcord.api.errors.DiscordException)


        * [`Funnu`](selfcord.api.md#selfcord.api.errors.Funnu)


        * [`LoginFailure`](selfcord.api.md#selfcord.api.errors.LoginFailure)


        * [`ReconnectWebsocket`](selfcord.api.md#selfcord.api.errors.ReconnectWebsocket)


        * [`RuntimeError`](selfcord.api.md#selfcord.api.errors.RuntimeError)


    * [selfcord.api.events module](selfcord.api.md#module-selfcord.api.events)


        * [`EventHandler`](selfcord.api.md#selfcord.api.events.EventHandler)


            * [`EventHandler.handle_channel_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_channel_create)


            * [`EventHandler.handle_channel_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_channel_delete)


            * [`EventHandler.handle_guild_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_create)


            * [`EventHandler.handle_guild_member_list_update()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_member_list_update)


            * [`EventHandler.handle_guild_role_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_role_create)


            * [`EventHandler.handle_guild_role_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_role_delete)


            * [`EventHandler.handle_message_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_message_create)


            * [`EventHandler.handle_message_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_message_delete)


            * [`EventHandler.handle_ready()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_ready)


            * [`EventHandler.handle_voice_server_update()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_voice_server_update)


            * [`EventHandler.handle_voice_state_update()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_voice_state_update)


            * [`EventHandler.voice_start()`](selfcord.api.md#selfcord.api.events.EventHandler.voice_start)


    * [selfcord.api.gateway module](selfcord.api.md#module-selfcord.api.gateway)


        * [`Activity`](selfcord.api.md#selfcord.api.gateway.Activity)


            * [`Activity.Game()`](selfcord.api.md#selfcord.api.gateway.Activity.Game)


            * [`Activity.Listen()`](selfcord.api.md#selfcord.api.gateway.Activity.Listen)


            * [`Activity.Stream()`](selfcord.api.md#selfcord.api.gateway.Activity.Stream)


            * [`Activity.Watch()`](selfcord.api.md#selfcord.api.gateway.Activity.Watch)


        * [`gateway`](selfcord.api.md#selfcord.api.gateway.gateway)


            * [`gateway.DISPATCH`](selfcord.api.md#selfcord.api.gateway.gateway.DISPATCH)


            * [`gateway.GUILD_SYNC`](selfcord.api.md#selfcord.api.gateway.gateway.GUILD_SYNC)


            * [`gateway.HEARTBEAT`](selfcord.api.md#selfcord.api.gateway.gateway.HEARTBEAT)


            * [`gateway.HEARTBEAT_ACK`](selfcord.api.md#selfcord.api.gateway.gateway.HEARTBEAT_ACK)


            * [`gateway.HELLO`](selfcord.api.md#selfcord.api.gateway.gateway.HELLO)


            * [`gateway.IDENTIFY`](selfcord.api.md#selfcord.api.gateway.gateway.IDENTIFY)


            * [`gateway.INVALIDATE_SESSION`](selfcord.api.md#selfcord.api.gateway.gateway.INVALIDATE_SESSION)


            * [`gateway.PRESENCE`](selfcord.api.md#selfcord.api.gateway.gateway.PRESENCE)


            * [`gateway.RECONNECT`](selfcord.api.md#selfcord.api.gateway.gateway.RECONNECT)


            * [`gateway.REQUEST_MEMBERS`](selfcord.api.md#selfcord.api.gateway.gateway.REQUEST_MEMBERS)


            * [`gateway.RESUME`](selfcord.api.md#selfcord.api.gateway.gateway.RESUME)


            * [`gateway.VOICE_PING`](selfcord.api.md#selfcord.api.gateway.gateway.VOICE_PING)


            * [`gateway.VOICE_STATE`](selfcord.api.md#selfcord.api.gateway.gateway.VOICE_STATE)


            * [`gateway.call()`](selfcord.api.md#selfcord.api.gateway.gateway.call)


            * [`gateway.change_presence()`](selfcord.api.md#selfcord.api.gateway.gateway.change_presence)


            * [`gateway.chunks()`](selfcord.api.md#selfcord.api.gateway.gateway.chunks)


            * [`gateway.close()`](selfcord.api.md#selfcord.api.gateway.gateway.close)


            * [`gateway.connect()`](selfcord.api.md#selfcord.api.gateway.gateway.connect)


            * [`gateway.heartbeat()`](selfcord.api.md#selfcord.api.gateway.gateway.heartbeat)


            * [`gateway.heartbeat_ack()`](selfcord.api.md#selfcord.api.gateway.gateway.heartbeat_ack)


            * [`gateway.identify()`](selfcord.api.md#selfcord.api.gateway.gateway.identify)


            * [`gateway.lazy_chunk()`](selfcord.api.md#selfcord.api.gateway.gateway.lazy_chunk)


            * [`gateway.leave_call()`](selfcord.api.md#selfcord.api.gateway.gateway.leave_call)


            * [`gateway.recv_msg()`](selfcord.api.md#selfcord.api.gateway.gateway.recv_msg)


            * [`gateway.roundup()`](selfcord.api.md#selfcord.api.gateway.gateway.roundup)


            * [`gateway.send_json()`](selfcord.api.md#selfcord.api.gateway.gateway.send_json)


            * [`gateway.start()`](selfcord.api.md#selfcord.api.gateway.gateway.start)


            * [`gateway.stream_call()`](selfcord.api.md#selfcord.api.gateway.gateway.stream_call)


            * [`gateway.video_call()`](selfcord.api.md#selfcord.api.gateway.gateway.video_call)


    * [selfcord.api.http module](selfcord.api.md#module-selfcord.api.http)


        * [`http`](selfcord.api.md#selfcord.api.http.http)


            * [`http.encode_image()`](selfcord.api.md#selfcord.api.http.http.encode_image)


            * [`http.get_cookie()`](selfcord.api.md#selfcord.api.http.http.get_cookie)


            * [`http.remove_dupes()`](selfcord.api.md#selfcord.api.http.http.remove_dupes)


            * [`http.request()`](selfcord.api.md#selfcord.api.http.http.request)


            * [`http.static_login()`](selfcord.api.md#selfcord.api.http.http.static_login)


    * [Module contents](selfcord.api.md#module-selfcord.api)


* [selfcord.models package](selfcord.models.md)


    * [Submodules](selfcord.models.md#submodules)


    * [selfcord.models.channel module](selfcord.models.md#module-selfcord.models.channel)


        * [`Category`](selfcord.models.md#selfcord.models.channel.Category)


            * [`Category.delete()`](selfcord.models.md#selfcord.models.channel.Category.delete)


        * [`DMChannel`](selfcord.models.md#selfcord.models.channel.DMChannel)


            * [`DMChannel.delete()`](selfcord.models.md#selfcord.models.channel.DMChannel.delete)


        * [`GroupChannel`](selfcord.models.md#selfcord.models.channel.GroupChannel)


            * [`GroupChannel.delete()`](selfcord.models.md#selfcord.models.channel.GroupChannel.delete)


        * [`Messageable`](selfcord.models.md#selfcord.models.channel.Messageable)


            * [`Messageable.history()`](selfcord.models.md#selfcord.models.channel.Messageable.history)


            * [`Messageable.purge()`](selfcord.models.md#selfcord.models.channel.Messageable.purge)


            * [`Messageable.reply()`](selfcord.models.md#selfcord.models.channel.Messageable.reply)


            * [`Messageable.send()`](selfcord.models.md#selfcord.models.channel.Messageable.send)


            * [`Messageable.spam()`](selfcord.models.md#selfcord.models.channel.Messageable.spam)


        * [`TextChannel`](selfcord.models.md#selfcord.models.channel.TextChannel)


            * [`TextChannel.create_webhook()`](selfcord.models.md#selfcord.models.channel.TextChannel.create_webhook)


            * [`TextChannel.delete()`](selfcord.models.md#selfcord.models.channel.TextChannel.delete)


            * [`TextChannel.edit()`](selfcord.models.md#selfcord.models.channel.TextChannel.edit)


        * [`VoiceChannel`](selfcord.models.md#selfcord.models.channel.VoiceChannel)


            * [`VoiceChannel.create_webhook()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.create_webhook)


            * [`VoiceChannel.delete()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.delete)


        * [`Voiceable`](selfcord.models.md#selfcord.models.channel.Voiceable)


            * [`Voiceable.call()`](selfcord.models.md#selfcord.models.channel.Voiceable.call)


            * [`Voiceable.leave_call()`](selfcord.models.md#selfcord.models.channel.Voiceable.leave_call)


            * [`Voiceable.stream_call()`](selfcord.models.md#selfcord.models.channel.Voiceable.stream_call)


            * [`Voiceable.video_call()`](selfcord.models.md#selfcord.models.channel.Voiceable.video_call)


    * [selfcord.models.client module](selfcord.models.md#module-selfcord.models.client)


        * [`Client`](selfcord.models.md#selfcord.models.client.Client)


    * [selfcord.models.emoji module](selfcord.models.md#module-selfcord.models.emoji)


        * [`Emoji`](selfcord.models.md#selfcord.models.emoji.Emoji)


            * [`Emoji.delete()`](selfcord.models.md#selfcord.models.emoji.Emoji.delete)


    * [selfcord.models.guild module](selfcord.models.md#module-selfcord.models.guild)


        * [`Guild`](selfcord.models.md#selfcord.models.guild.Guild)


            * [`Guild.ANNOUNCEMENT_THREAD`](selfcord.models.md#selfcord.models.guild.Guild.ANNOUNCEMENT_THREAD)


            * [`Guild.CATEGORY`](selfcord.models.md#selfcord.models.guild.Guild.CATEGORY)


            * [`Guild.GUILD_ANNOUNCEMENT`](selfcord.models.md#selfcord.models.guild.Guild.GUILD_ANNOUNCEMENT)


            * [`Guild.GUILD_DIRECTORY`](selfcord.models.md#selfcord.models.guild.Guild.GUILD_DIRECTORY)


            * [`Guild.GUILD_FORUM`](selfcord.models.md#selfcord.models.guild.Guild.GUILD_FORUM)


            * [`Guild.GUILD_STAGE_VOICE`](selfcord.models.md#selfcord.models.guild.Guild.GUILD_STAGE_VOICE)


            * [`Guild.PRIVATE_THREAD`](selfcord.models.md#selfcord.models.guild.Guild.PRIVATE_THREAD)


            * [`Guild.PUBLIC_THREAD`](selfcord.models.md#selfcord.models.guild.Guild.PUBLIC_THREAD)


            * [`Guild.TEXTCHANNEL`](selfcord.models.md#selfcord.models.guild.Guild.TEXTCHANNEL)


            * [`Guild.VOICECHANNEL`](selfcord.models.md#selfcord.models.guild.Guild.VOICECHANNEL)


            * [`Guild.ban()`](selfcord.models.md#selfcord.models.guild.Guild.ban)


            * [`Guild.category_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.category_channel_create)


            * [`Guild.delete()`](selfcord.models.md#selfcord.models.guild.Guild.delete)


            * [`Guild.edit()`](selfcord.models.md#selfcord.models.guild.Guild.edit)


            * [`Guild.emoji_create()`](selfcord.models.md#selfcord.models.guild.Guild.emoji_create)


            * [`Guild.get_members()`](selfcord.models.md#selfcord.models.guild.Guild.get_members)


            * [`Guild.kick()`](selfcord.models.md#selfcord.models.guild.Guild.kick)


            * [`Guild.role_create()`](selfcord.models.md#selfcord.models.guild.Guild.role_create)


            * [`Guild.timeout()`](selfcord.models.md#selfcord.models.guild.Guild.timeout)


            * [`Guild.txt_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.txt_channel_create)


            * [`Guild.utc_now()`](selfcord.models.md#selfcord.models.guild.Guild.utc_now)


            * [`Guild.vc_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.vc_channel_create)


    * [selfcord.models.member module](selfcord.models.md#module-selfcord.models.member)


        * [`Member`](selfcord.models.md#selfcord.models.member.Member)


    * [selfcord.models.message module](selfcord.models.md#module-selfcord.models.message)


        * [`Message`](selfcord.models.md#selfcord.models.message.Message)


            * [`Message.delete()`](selfcord.models.md#selfcord.models.message.Message.delete)


            * [`Message.edit()`](selfcord.models.md#selfcord.models.message.Message.edit)


            * [`Message.react()`](selfcord.models.md#selfcord.models.message.Message.react)


    * [selfcord.models.permission module](selfcord.models.md#module-selfcord.models.permission)


        * [`Permission`](selfcord.models.md#selfcord.models.permission.Permission)


            * [`Permission.calculate_permissions()`](selfcord.models.md#selfcord.models.permission.Permission.calculate_permissions)


    * [selfcord.models.role module](selfcord.models.md#module-selfcord.models.role)


        * [`Role`](selfcord.models.md#selfcord.models.role.Role)


            * [`Role.delete()`](selfcord.models.md#selfcord.models.role.Role.delete)


    * [selfcord.models.user module](selfcord.models.md#module-selfcord.models.user)


        * [`Connected_Account`](selfcord.models.md#selfcord.models.user.Connected_Account)


        * [`Profile`](selfcord.models.md#selfcord.models.user.Profile)


        * [`User`](selfcord.models.md#selfcord.models.user.User)


            * [`User.b64token`](selfcord.models.md#selfcord.models.user.User.b64token)


            * [`User.create_dm()`](selfcord.models.md#selfcord.models.user.User.create_dm)


            * [`User.created_at`](selfcord.models.md#selfcord.models.user.User.created_at)


            * [`User.get_profile()`](selfcord.models.md#selfcord.models.user.User.get_profile)


    * [selfcord.models.webhook module](selfcord.models.md#module-selfcord.models.webhook)


        * [`Webhook`](selfcord.models.md#selfcord.models.webhook.Webhook)


            * [`Webhook.delete()`](selfcord.models.md#selfcord.models.webhook.Webhook.delete)


            * [`Webhook.send()`](selfcord.models.md#selfcord.models.webhook.Webhook.send)


    * [Module contents](selfcord.models.md#module-selfcord.models)


* [selfcord.utils package](selfcord.utils.md)


    * [Submodules](selfcord.utils.md#submodules)


    * [selfcord.utils.command module](selfcord.utils.md#module-selfcord.utils.command)


        * [`Command`](selfcord.utils.md#selfcord.utils.command.Command)


        * [`CommandCollection`](selfcord.utils.md#selfcord.utils.command.CommandCollection)


            * [`CommandCollection.add()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.add)


            * [`CommandCollection.append()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.append)


            * [`CommandCollection.clear()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.clear)


            * [`CommandCollection.copy()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.copy)


            * [`CommandCollection.get()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.get)


            * [`CommandCollection.recents()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.recents)


        * [`Context`](selfcord.utils.md#selfcord.utils.command.Context)


            * [`Context.alias`](selfcord.utils.md#selfcord.utils.command.Context.alias)


            * [`Context.author`](selfcord.utils.md#selfcord.utils.command.Context.author)


            * [`Context.channel`](selfcord.utils.md#selfcord.utils.command.Context.channel)


            * [`Context.command`](selfcord.utils.md#selfcord.utils.command.Context.command)


            * [`Context.command_content`](selfcord.utils.md#selfcord.utils.command.Context.command_content)


            * [`Context.content`](selfcord.utils.md#selfcord.utils.command.Context.content)


            * [`Context.convert()`](selfcord.utils.md#selfcord.utils.command.Context.convert)


            * [`Context.edit()`](selfcord.utils.md#selfcord.utils.command.Context.edit)


            * [`Context.get_arguments()`](selfcord.utils.md#selfcord.utils.command.Context.get_arguments)


            * [`Context.get_converter()`](selfcord.utils.md#selfcord.utils.command.Context.get_converter)


            * [`Context.guild`](selfcord.utils.md#selfcord.utils.command.Context.guild)


            * [`Context.invoke()`](selfcord.utils.md#selfcord.utils.command.Context.invoke)


            * [`Context.prefix`](selfcord.utils.md#selfcord.utils.command.Context.prefix)


            * [`Context.purge()`](selfcord.utils.md#selfcord.utils.command.Context.purge)


            * [`Context.reply()`](selfcord.utils.md#selfcord.utils.command.Context.reply)


            * [`Context.send()`](selfcord.utils.md#selfcord.utils.command.Context.send)


            * [`Context.spam()`](selfcord.utils.md#selfcord.utils.command.Context.spam)


        * [`Event`](selfcord.utils.md#selfcord.utils.command.Event)


        * [`Extender`](selfcord.utils.md#selfcord.utils.command.Extender)


            * [`Extender.add_cmd()`](selfcord.utils.md#selfcord.utils.command.Extender.add_cmd)


            * [`Extender.cmd()`](selfcord.utils.md#selfcord.utils.command.Extender.cmd)


            * [`Extender.commands`](selfcord.utils.md#selfcord.utils.command.Extender.commands)


            * [`Extender.on()`](selfcord.utils.md#selfcord.utils.command.Extender.on)


        * [`Extension`](selfcord.utils.md#selfcord.utils.command.Extension)


        * [`ExtensionCollection`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection)


            * [`ExtensionCollection.add()`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection.add)


            * [`ExtensionCollection.get()`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection.get)


    * [Module contents](selfcord.utils.md#module-selfcord.utils)


## Submodules

## selfcord.bot module


### _class_ selfcord.bot.Bot(show_beat: bool = False, prefixes: list = ['s!'], inbuilt_help=True, userbot=False, eval=False)
Bases: `object`


#### add_cmd(coro, description='', aliases=[])
Function to add commands manually without decorator

Args:

    coro (coroutine): The function to add
    description (str, optional): Description of command. Defaults to “”.
    aliases (list, optional): Alternative names for command. Defaults to [].

Raises:

    RuntimeWarning: If you suck and don’t use a coroutine


#### _async_ add_friend(user_id: str)
Function to add a specific user as a friend.

Args:

    user_id (str): ID of the possible random user.

Returns:

    No return value.


#### _async_ change_hypesquad(house: str)
Helper function to change hypesquad

Args:

    house (str): Hypesquad name


#### _async_ change_pfp(avatar_url=None)
Disclaimer: This may phone lock your account :(

Args:

    avatar_url (str): URL of image

Raises:

    TypeError: URL not specified


#### _async_ change_presence(status: str, afk: bool, activity: dict)
Change discord activity presence

Args:

    status (str): Online, Offline, Dnd, Invisible
    afk (bool): True or False
    activity (dict): Selfcord.Activity method.


#### cmd(description='', aliases=[])
Decorator to add commands for the bot

Args:

    description (str, optional): Description of command. Defaults to “”.
    aliases (list, optional): Alternative names for command. Defaults to [].

Raises:

    RuntimeWarning: If you suck and don’t use a coroutine


#### _async_ create_dm(recipient_id: int)
Function to create new DM Channel with other user. Can be used with bots too.

Args:

    recipient_id (snowflake): ID of recipient - Has to be user or bot ID

Raises:

    TypeError: Recipient ID not specified

Returns:

    DMChannel object


#### _async_ create_guild(name: str, icon_url: str = None, template: str = '2TffvPucqHkN')
Creates a guild


#### _async_ edit_profile(bio: str = None, accent: int = None)
Edits user profile


#### _async_ emit(event, \*args, \*\*kwargs)
Used to essentially push values to the decorator when the event fires

Args:

    event (str): The event name


#### get_channel(channel_id: str)
Function to help retrieve channel from bot cache

Args:

    channel_id (str): The channel id to search for

Returns:

    Channel: The Channel object


#### get_guild(guild_id: str)
Function to help retrieve guild from bot cache

Args:

    guild_id (str): The guild id to search for

Returns:

    Guild: The Guild object


#### _async_ get_user(user_id: str)
Function to retrieve user data. Probably need to be friends with them to retrieve the details.

Args:

    user_id (Str): ID of the other user.

Returns:

> User: The User object


#### _async_ inbuilt_commands()
I call this on bot initialisation, it’s the inbuilt help command


#### _property_ latency()
Latency of heartbeat ack, gateway latency essentially


#### _async_ load_extension(name: str)
Load various extensions/plugins/cogs if any.

Args:

    name (str): Name of the extension to load

Raises:

    ModuleNotFoundError: If you suck and don’t know the name of what you want to load


#### on(event: str)
Decorator for events

Args:

    event (str): The event to check for


#### _async_ process_commands(msg)
What is called in order to actually get command input and run commands

Args:

    msg (str): The message containing command


#### _async_ redeem_nitro(code: str)
Helper function to redeem nitro

Args:

    code (str): Nitro code


#### run(token: str)
Used to start connection to gateway as well as gather user information

Args:

    token (str): _description_

## Module contents
