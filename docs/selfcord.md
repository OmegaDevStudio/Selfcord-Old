# selfcord package

Selfcord is a Discord API Wrapper with the design intended to be specifically for selfbots. Please do note that selfbots are against Discord TOS and using a selfbot can risk your account to be permanently terminated even though we may try to prevent this.

## Subpackages


* [selfcord.api package](selfcord.api.md)


    * [Submodules](selfcord.api.md#submodules)


    * [selfcord.api.errors module](selfcord.api.md#selfcord-api-errors-module)


        * [`DiscordException`](selfcord.api.md#selfcord.api.errors.DiscordException)


        * [`Funnu`](selfcord.api.md#selfcord.api.errors.Funnu)


        * [`LoginFailure`](selfcord.api.md#selfcord.api.errors.LoginFailure)


        * [`ReconnectWebsocket`](selfcord.api.md#selfcord.api.errors.ReconnectWebsocket)


        * [`RuntimeError`](selfcord.api.md#selfcord.api.errors.RuntimeError)


    * [selfcord.api.events module](selfcord.api.md#selfcord-api-events-module)


        * [`EventHandler`](selfcord.api.md#selfcord.api.events.EventHandler)


            * [`EventHandler.handle_channel_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_channel_create)


            * [`EventHandler.handle_channel_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_channel_delete)


            * [`EventHandler.handle_guild_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_create)


            * [`EventHandler.handle_guild_role_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_role_create)


            * [`EventHandler.handle_guild_role_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_guild_role_delete)


            * [`EventHandler.handle_message_create()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_message_create)


            * [`EventHandler.handle_message_delete()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_message_delete)


            * [`EventHandler.handle_ready()`](selfcord.api.md#selfcord.api.events.EventHandler.handle_ready)


    * [selfcord.api.gateway module](selfcord.api.md#selfcord-api-gateway-module)


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


            * [`gateway.close()`](selfcord.api.md#selfcord.api.gateway.gateway.close)


            * [`gateway.connect()`](selfcord.api.md#selfcord.api.gateway.gateway.connect)


            * [`gateway.heartbeat()`](selfcord.api.md#selfcord.api.gateway.gateway.heartbeat)


            * [`gateway.heartbeat_ack()`](selfcord.api.md#selfcord.api.gateway.gateway.heartbeat_ack)


            * [`gateway.identify()`](selfcord.api.md#selfcord.api.gateway.gateway.identify)


            * [`gateway.recv_msg()`](selfcord.api.md#selfcord.api.gateway.gateway.recv_msg)


            * [`gateway.send_json()`](selfcord.api.md#selfcord.api.gateway.gateway.send_json)


            * [`gateway.start()`](selfcord.api.md#selfcord.api.gateway.gateway.start)


    * [selfcord.api.http module](selfcord.api.md#selfcord-api-http-module)


        * [`http`](selfcord.api.md#selfcord.api.http.http)


            * [`http.encode_image()`](selfcord.api.md#selfcord.api.http.http.encode_image)


            * [`http.get_cookie()`](selfcord.api.md#selfcord.api.http.http.get_cookie)


            * [`http.remove_dupes()`](selfcord.api.md#selfcord.api.http.http.remove_dupes)


            * [`http.request()`](selfcord.api.md#selfcord.api.http.http.request)


            * [`http.static_login()`](selfcord.api.md#selfcord.api.http.http.static_login)


    * [Module contents](selfcord.api.md#module-contents)


* [selfcord.models package](selfcord.models.md)


    * [Submodules](selfcord.models.md#submodules)


    * [selfcord.models.channel module](selfcord.models.md#selfcord-models-channel-module)


        * [`Category`](selfcord.models.md#selfcord.models.channel.Category)


            * [`Category.delete()`](selfcord.models.md#selfcord.models.channel.Category.delete)


        * [`DMChannel`](selfcord.models.md#selfcord.models.channel.DMChannel)


            * [`DMChannel.delete()`](selfcord.models.md#selfcord.models.channel.DMChannel.delete)


            * [`DMChannel.history()`](selfcord.models.md#selfcord.models.channel.DMChannel.history)


            * [`DMChannel.purge()`](selfcord.models.md#selfcord.models.channel.DMChannel.purge)


            * [`DMChannel.reply()`](selfcord.models.md#selfcord.models.channel.DMChannel.reply)


            * [`DMChannel.send()`](selfcord.models.md#selfcord.models.channel.DMChannel.send)


            * [`DMChannel.spam()`](selfcord.models.md#selfcord.models.channel.DMChannel.spam)


        * [`GroupChannel`](selfcord.models.md#selfcord.models.channel.GroupChannel)


            * [`GroupChannel.delete()`](selfcord.models.md#selfcord.models.channel.GroupChannel.delete)


            * [`GroupChannel.history()`](selfcord.models.md#selfcord.models.channel.GroupChannel.history)


            * [`GroupChannel.purge()`](selfcord.models.md#selfcord.models.channel.GroupChannel.purge)


            * [`GroupChannel.reply()`](selfcord.models.md#selfcord.models.channel.GroupChannel.reply)


            * [`GroupChannel.send()`](selfcord.models.md#selfcord.models.channel.GroupChannel.send)


            * [`GroupChannel.spam()`](selfcord.models.md#selfcord.models.channel.GroupChannel.spam)


        * [`TextChannel`](selfcord.models.md#selfcord.models.channel.TextChannel)


            * [`TextChannel.create_webhook()`](selfcord.models.md#selfcord.models.channel.TextChannel.create_webhook)


            * [`TextChannel.delete()`](selfcord.models.md#selfcord.models.channel.TextChannel.delete)


            * [`TextChannel.history()`](selfcord.models.md#selfcord.models.channel.TextChannel.history)


            * [`TextChannel.purge()`](selfcord.models.md#selfcord.models.channel.TextChannel.purge)


            * [`TextChannel.reply()`](selfcord.models.md#selfcord.models.channel.TextChannel.reply)


            * [`TextChannel.send()`](selfcord.models.md#selfcord.models.channel.TextChannel.send)


            * [`TextChannel.spam()`](selfcord.models.md#selfcord.models.channel.TextChannel.spam)


        * [`VoiceChannel`](selfcord.models.md#selfcord.models.channel.VoiceChannel)


            * [`VoiceChannel.create_webhook()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.create_webhook)


            * [`VoiceChannel.delete()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.delete)


            * [`VoiceChannel.history()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.history)


            * [`VoiceChannel.purge()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.purge)


            * [`VoiceChannel.reply()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.reply)


            * [`VoiceChannel.send()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.send)


            * [`VoiceChannel.spam()`](selfcord.models.md#selfcord.models.channel.VoiceChannel.spam)


    * [selfcord.models.client module](selfcord.models.md#selfcord-models-client-module)


        * [`Client`](selfcord.models.md#selfcord.models.client.Client)


    * [selfcord.models.emoji module](selfcord.models.md#selfcord-models-emoji-module)


        * [`Emoji`](selfcord.models.md#selfcord.models.emoji.Emoji)


    * [selfcord.models.guild module](selfcord.models.md#selfcord-models-guild-module)


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


            * [`Guild.category_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.category_channel_create)


            * [`Guild.delete()`](selfcord.models.md#selfcord.models.guild.Guild.delete)


            * [`Guild.edit()`](selfcord.models.md#selfcord.models.guild.Guild.edit)


            * [`Guild.role_create()`](selfcord.models.md#selfcord.models.guild.Guild.role_create)


            * [`Guild.txt_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.txt_channel_create)


            * [`Guild.vc_channel_create()`](selfcord.models.md#selfcord.models.guild.Guild.vc_channel_create)


    * [selfcord.models.member module](selfcord.models.md#selfcord-models-member-module)


        * [`Member`](selfcord.models.md#selfcord.models.member.Member)


    * [selfcord.models.message module](selfcord.models.md#selfcord-models-message-module)


        * [`Message`](selfcord.models.md#selfcord.models.message.Message)


            * [`Message.delete()`](selfcord.models.md#selfcord.models.message.Message.delete)


    * [selfcord.models.permission module](selfcord.models.md#selfcord-models-permission-module)


        * [`Permission`](selfcord.models.md#selfcord.models.permission.Permission)


            * [`Permission.calculate_permissions()`](selfcord.models.md#selfcord.models.permission.Permission.calculate_permissions)


    * [selfcord.models.role module](selfcord.models.md#selfcord-models-role-module)


        * [`Role`](selfcord.models.md#selfcord.models.role.Role)


    * [selfcord.models.user module](selfcord.models.md#selfcord-models-user-module)


        * [`User`](selfcord.models.md#selfcord.models.user.User)


            * [`User.b64token`](selfcord.models.md#selfcord.models.user.User.b64token)


            * [`User.created_at`](selfcord.models.md#selfcord.models.user.User.created_at)


    * [selfcord.models.webhook module](selfcord.models.md#selfcord-models-webhook-module)


        * [`Webhook`](selfcord.models.md#selfcord.models.webhook.Webhook)


            * [`Webhook.delete()`](selfcord.models.md#selfcord.models.webhook.Webhook.delete)


            * [`Webhook.send()`](selfcord.models.md#selfcord.models.webhook.Webhook.send)


    * [Module contents](selfcord.models.md#module-contents)


* [selfcord.utils package](selfcord.utils.md)


    * [Submodules](selfcord.utils.md#submodules)


    * [selfcord.utils.command module](selfcord.utils.md#module-selfcord.utils.command)


        * [`Command`](selfcord.utils.md#selfcord.utils.command.Command)


        * [`CommandCollection`](selfcord.utils.md#selfcord.utils.command.CommandCollection)


            * [`CommandCollection.add()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.add)


            * [`CommandCollection.get()`](selfcord.utils.md#selfcord.utils.command.CommandCollection.get)


        * [`Context`](selfcord.utils.md#selfcord.utils.command.Context)


            * [`Context.alias`](selfcord.utils.md#selfcord.utils.command.Context.alias)


            * [`Context.author`](selfcord.utils.md#selfcord.utils.command.Context.author)


            * [`Context.channel`](selfcord.utils.md#selfcord.utils.command.Context.channel)


            * [`Context.command`](selfcord.utils.md#selfcord.utils.command.Context.command)


            * [`Context.command_content`](selfcord.utils.md#selfcord.utils.command.Context.command_content)


            * [`Context.content`](selfcord.utils.md#selfcord.utils.command.Context.content)


            * [`Context.convert()`](selfcord.utils.md#selfcord.utils.command.Context.convert)


            * [`Context.get_arguments()`](selfcord.utils.md#selfcord.utils.command.Context.get_arguments)


            * [`Context.get_converter()`](selfcord.utils.md#selfcord.utils.command.Context.get_converter)


            * [`Context.guild`](selfcord.utils.md#selfcord.utils.command.Context.guild)


            * [`Context.invoke()`](selfcord.utils.md#selfcord.utils.command.Context.invoke)


            * [`Context.prefix`](selfcord.utils.md#selfcord.utils.command.Context.prefix)


            * [`Context.purge()`](selfcord.utils.md#selfcord.utils.command.Context.purge)


            * [`Context.reply()`](selfcord.utils.md#selfcord.utils.command.Context.reply)


            * [`Context.send()`](selfcord.utils.md#selfcord.utils.command.Context.send)


            * [`Context.spam()`](selfcord.utils.md#selfcord.utils.command.Context.spam)


        * [`Extension`](selfcord.utils.md#selfcord.utils.command.Extension)


        * [`ExtensionCollection`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection)


            * [`ExtensionCollection.add()`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection.add)


            * [`ExtensionCollection.get()`](selfcord.utils.md#selfcord.utils.command.ExtensionCollection.get)


    * [Module contents](selfcord.utils.md#module-selfcord.utils)


## Submodules

## selfcord.bot module

Used to represent the bot itself running the selfcord client.

## Module contents
