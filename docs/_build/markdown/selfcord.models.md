# selfcord.models package

## Submodules

## selfcord.models.channel module


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


### _class_ selfcord.models.client.Client(UserPayload: dict)
Bases: `object`

Client Object

## selfcord.models.emoji module


### _class_ selfcord.models.emoji.Emoji(data)
Bases: `object`

Emoji Object

## selfcord.models.guild module


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


### _class_ selfcord.models.member.Member(UserPayload: dict)
Bases: `object`

Member Object

## selfcord.models.message module


### _class_ selfcord.models.message.Message(data, bot, http)
Bases: `object`

Message Object


#### _async_ delete()
## selfcord.models.permission module


### _class_ selfcord.models.permission.Permission(data)
Bases: `object`

Permission Object


#### calculate_permissions(perm_value)
## selfcord.models.role module


### _class_ selfcord.models.role.Role(data: dict, http, \*\*kwargs)
Bases: `object`

Role Object

## selfcord.models.user module


### _class_ selfcord.models.user.User(UserPayload: dict)
Bases: `object`

User Object


#### _property_ b64token()

#### _property_ created_at()
## selfcord.models.webhook module


### _class_ selfcord.models.webhook.Webhook(data: dict, bot, http)
Bases: `object`


#### _async_ delete()

#### _async_ send(content)
## Module contents

Data objects from discord, used throughout selfcord
