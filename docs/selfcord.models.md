# selfcord.models package

## Submodules

## selfcord.models.channel module


### _class_ selfcord.models.channel.Category(data, bot, http)
Bases: `object`

Category Object


#### _async_ delete()

### _class_ selfcord.models.channel.DMChannel(data, bot, http)
Bases: `Messageable`

DM Channel Object


#### _async_ call()

#### _async_ delete()

#### _async_ leave()

### _class_ selfcord.models.channel.GroupChannel(data, bot, http)
Bases: `Messageable`

Group Channel Object


#### _async_ call()

#### _async_ delete()

#### _async_ leave()

### _class_ selfcord.models.channel.Messageable(http, bot)
Bases: `object`


#### _async_ history()
Get channel message history.

Args:

    No arguments required

Returns:

    messages(list) : List of messages from the channel.


#### _async_ purge(amount: Optional[int] = None)
Delete a number of messages, starting from the most recent.

Args:

    amount(int) : Number of messages to purge/delete.

Returns:

    No return value


#### _async_ reply(message, content=None, tts=False)

#### _async_ send(content=None, tts=False)
Send a message to the text channel.

Args:

    
    * content(str) : Message content. Should be string type or similar. Discord embed type is not allowed.


    * tts(bool) :


#### _async_ spam(amount: int, content: str, tts=False)
Send multiple of the same message.

Args:

    
    * amount(int) : Number of spam messages to send.


    * content(str) : The message to send.


    * tts(bool) = False : Specify whether it is a TTS message.

Returns:

    No return value.


### _class_ selfcord.models.channel.TextChannel(data, bot, http)
Bases: `Messageable`

Text Channel Object

    Represents a Guild/Server channel within Discord.
    All methods are coroutines and thus need to be awaited.

Returns:

    Name of the channel

Functions:

    
    * delete()


    * edit(name[str], parent_id[int], position[int], topic[str])


    * history()


    * purge(amount[int])


    * spam(amount[int], content[str], tts[bool]=False)


    * send()


    * reply()


    * create_webhook()

Example Object (ref: [https://discord.com/developers/docs/resources/channel#channel-object-example-guild-text-channel](https://discord.com/developers/docs/resources/channel#channel-object-example-guild-text-channel))

    {

        “id”: “41771983423143937”,
        “guild_id”: “41771983423143937”,
        “name”: “general”,
        “type”: 0,
        “position”: 6,
        “permission_overwrites”: [],
        “rate_limit_per_user”: 2,
        “nsfw”: true,
        “topic”: “24/7 chat about how to gank Mike #2”,
        “last_message_id”: “155117677105512449”,
        “parent_id”: “399942396007890945”,
        “default_auto_archive_duration”: 60

    }


#### _async_ create_webhook(name: Optional[str] = None, avatar_url: Optional[str] = None)

#### _async_ delete()
Deletes the text channel object.

Args:

    No arguments required

Returns:

    No return value


#### _async_ edit(name: Optional[str] = None, parent_id: Optional[int] = None, position: Optional[int] = None, topic: Optional[str] = None)
Edits the text channel object details. Requires the Manage Channels permission.
Not all details can be modified.

Args:

    
    * name(str) : Optional - Specifies a new name for the channel object. Defaults to None.


    * parent_id(int) : Optional - Specifies a new parent (category) for the text channel object.


    * position(int) : Optional - Modifies the sorting position of the text channel within the guild.


    * topic(str)

        0-1024 characters for all others)

Notice: Each parent category can contain up to 50 channels.

Returns:

    e(str) : Exception parsed as string value.


### _class_ selfcord.models.channel.VoiceChannel(data, bot, http)
Bases: `Messageable`

Voice Channel Object


#### _async_ call()

#### _async_ create_webhook(name: Optional[str] = None, avatar_url: Optional[str] = None)

#### _async_ delete()

#### _async_ leave()
## selfcord.models.client module


### _class_ selfcord.models.client.Client(UserPayload: dict)
Bases: `object`

Client Object

## selfcord.models.emoji module


### _class_ selfcord.models.emoji.Emoji(data, bot, http)
Bases: `object`

Emoji Object


#### _async_ delete()
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

#### _async_ ban(user_id: str)

#### _async_ category_channel_create(name)

#### _async_ delete()

#### _async_ edit(name: Optional[str] = None, icon_url: Optional[str] = None, banner_url: Optional[str] = None, description: Optional[str] = None)

#### _async_ emoji_create(name: str, image_url: str)

#### _async_ get_members(channel_id: str)

#### _async_ kick(user_id: str)

#### _async_ role_create(name)

#### _async_ txt_channel_create(name, parent_id=None)

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

#### _async_ react(emoji)
## selfcord.models.permission module


### _class_ selfcord.models.permission.Permission(data)
Bases: `object`

Permission Object


#### calculate_permissions(perm_value)
## selfcord.models.role module


### _class_ selfcord.models.role.Role(data: dict, http, \*\*kwargs)
Bases: `object`

Role Object


#### _async_ delete()
## selfcord.models.user module


### _class_ selfcord.models.user.Connected_Account(data)
Bases: `object`


### _class_ selfcord.models.user.Profile(UserPayload: dict, bot, http)
Bases: `object`


### _class_ selfcord.models.user.User(UserPayload: dict, bot, http)
Bases: `object`

User Object


#### _property_ b64token()

#### _async_ create_dm()

#### _property_ created_at()

#### _async_ get_profile()
## selfcord.models.webhook module


### _class_ selfcord.models.webhook.Webhook(data: dict, bot, http)
Bases: `object`


#### _async_ delete()

#### _async_ send(content)
## Module contents

Data objects from discord, used throughout selfcord
