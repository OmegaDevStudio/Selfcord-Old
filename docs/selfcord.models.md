# selfcord.models package

The multiple different objects Selfcord uses, generally mostly the same as the discord objects.

## Submodules

## selfcord.models.channel module

Channel model, meant to represent a channel object.


### _class_ selfcord.models.channel.Category(data, bot, http)
Bases: `object`

Category Object


#### _async_ delete()

### _class_ selfcord.models.channel.DMChannel(data, bot, http)
Bases: `object`

DM Channel Object


#### _async_ delete()

#### _async_ history()

#### _async_ purge(amount: Optional[int] = None)

#### _async_ reply(message, content=None, tts=False)

#### _async_ send(content=None, tts=False)

#### _async_ spam(amount: int, content: str, tts=False)

### _class_ selfcord.models.channel.GroupChannel(data, bot, http)
Bases: `object`

Group Channel Object


#### _async_ delete()

#### _async_ history()

#### _async_ purge(amount: Optional[int] = None)

#### _async_ reply(message, content=None, tts=False)

#### _async_ send(content=None, tts=False)

#### _async_ spam(amount: int, content: str, tts=False)

### _class_ selfcord.models.channel.TextChannel(data, bot, http)
Bases: `object`

Text Channel Object


#### _async_ create_webhook(name: Optional[str] = None, avatar_url: Optional[str] = None)

#### _async_ delete()

#### _async_ history()

#### _async_ purge(amount: Optional[int] = None)

#### _async_ reply(message, content=None, tts=False)

#### _async_ send(content=None, tts=False)

#### _async_ spam(amount: int, content: str, tts=False)

### _class_ selfcord.models.channel.VoiceChannel(data, bot, http)
Bases: `object`

Voice Channel Object


#### _async_ create_webhook(name: Optional[str] = None, avatar_url: Optional[str] = None)

#### _async_ delete()

#### _async_ history()

#### _async_ purge(amount: Optional[int] = None)

#### _async_ reply(message, content=None, tts=False)

#### _async_ send(content=None, tts=False)

#### _async_ spam(amount: int, content: str, tts=False)
## selfcord.models.client module

Channel client, meant to represent a client object. Used for the bot user.


### _class_ selfcord.models.client.Client(UserPayload: dict)
Bases: `object`

Client Object

## selfcord.models.emoji module

Emoji model, meant to represent a emoji object.


### _class_ selfcord.models.emoji.Emoji(data)
Bases: `object`

Emoji Object

## selfcord.models.guild module

Guild model, meant to represent a guild object.


### _class_ selfcord.models.guild.Guild(data, bot, http)
Bases: `object`

Guild Object


#### ANNOUNCEMENT_THREAD(_ = 1_ )

#### CATEGORY(_ = _ )

#### GUILD_ANNOUNCEMENT(_ = _ )

#### GUILD_DIRECTORY(_ = 1_ )

#### GUILD_FORUM(_ = 1_ )

#### GUILD_STAGE_VOICE(_ = 1_ )

#### PRIVATE_THREAD(_ = 1_ )

#### PUBLIC_THREAD(_ = 1_ )

#### TEXTCHANNEL(_ = _ )

#### VOICECHANNEL(_ = _ )

#### _async_ category_channel_create(name)

#### _async_ delete()

#### _async_ edit(name: Optional[str] = None, icon_url: Optional[str] = None, banner_url: Optional[str] = None, description: Optional[str] = None)

#### _async_ role_create(name)

#### _async_ txt_channel_create(name)

#### _async_ vc_channel_create(name)
## selfcord.models.member module

Member model, meant to represent a member object. Used for guilds.


### _class_ selfcord.models.member.Member(UserPayload: dict)
Bases: `object`

Member Object

## selfcord.models.message module

Message model, meant to represent a message object.


### _class_ selfcord.models.message.Message(data, bot, http)
Bases: `object`

Message Object


#### _async_ delete()
## selfcord.models.permission module

Permission model, meant to represent a permissions object. Used for Roles and Channels.


### _class_ selfcord.models.permission.Permission(data)
Bases: `object`

Permission Object


#### calculate_permissions(perm_value)
## selfcord.models.role module

Role model, used to represent a role object. Used for guilds.


### _class_ selfcord.models.role.Role(data: dict, http, \*\*kwargs)
Bases: `object`

Role Object

## selfcord.models.user module

User model, used to represent a user object. Used throughout discord.


### _class_ selfcord.models.user.User(UserPayload: dict)
Bases: `object`

User Object


#### _property_ b64token()

#### _property_ created_at()
## selfcord.models.webhook module

Webhook model, used to represent a webhook object. Used specifically in guilds.


### _class_ selfcord.models.webhook.Webhook(data: dict, bot, http)
Bases: `object`


#### _async_ delete()

#### _async_ send(content)
## Module contents

The multiple different objects Selfcord uses, generally mostly the same as the discord objects.

Data objects from discord, used throughout selfcord
