# selfcord.api package

Holds all classes to interact with Discord, includes interactions via the Discord API and Discord Gateway.

## Submodules

## selfcord.api.errors module

Error class for selfcord related API errors, includes Discord Gateway and Discord API.


### _exception_ selfcord.api.errors.DiscordException()
Bases: `Exception`


### _exception_ selfcord.api.errors.Funny(\*args: object)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.LoginFailure(message: dict, status: int)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.ReconnectWebsocket(message: str)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.RuntimeDiscordError(message: str)
Bases: `DiscordException`

## selfcord.api.events module

Class specifically made to handle the different events sent via Discord Gateway. They also dictate selfcords @bot.on(“event”) decorator.


### _class_ selfcord.api.events.EventHandler(bot, http)
Bases: `object`

Used to handle discord events


#### _async_ handle_channel_create(channel, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a channel is created


#### _async_ handle_channel_delete(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a channel is deleted


#### _async_ handle_guild_create(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a guild is created


#### _async_ handle_guild_role_create(role, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a role is created


#### _async_ handle_guild_role_delete(role, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a role is deleted


#### _async_ handle_message_create(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a message is created


#### _async_ handle_message_delete(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a message is created. Disclaimer: Only guild id, message id and channel id will be present if the message is not in bots cache.


#### _async_ handle_ready(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles the ready event, what is executed when it appears

## selfcord.api.gateway module

Gateway implementation designed to essentially start a connection to Discord Gateway and maintain connection via Heartbeats. It also sends data to the events class.


### _class_ selfcord.api.gateway.Gateway(http, show_heartbeat=False)
Bases: `object`


#### DISPATCH(_ = _ )

#### GUILD_SYNC(_ = 1_ )

#### HEARTBEAT(_ = _ )

#### HEARTBEAT_ACK(_ = 1_ )

#### HELLO(_ = 1_ )

#### IDENTIFY(_ = _ )

#### INVALIDATE_SESSION(_ = _ )

#### PRESENCE(_ = _ )

#### RECONNECT(_ = _ )

#### REQUEST_MEMBERS(_ = _ )

#### RESUME(_ = _ )

#### VOICE_PING(_ = _ )

#### VOICE_STATE(_ = _ )

#### _async_ close()
Close the connection to discord gateway


#### _async_ connect()
Connect to discord gateway


#### _async_ heartbeat(interval)
Heartbeat for gateway to maintain connection

Args:

    interval (int): Interval between sends


#### _async_ heartbeat_ack()
Whenever heartbeat ack is sent, logs the time between last send of heartbeat json and receive of the ack


#### _async_ identify()
Identify to gateway, uses amazing mobile client spoof


#### _async_ recv_msg()
Receives Message from gateway, encodes as json and does things depending on op code


#### _async_ send_json(payload: dict)
Send json to the gateway

Args:

    payload (dict): Valid payload to send to the gateway


#### _async_ start(token: str, user: [Client](selfcord.models.md#selfcord.models.client.Client), bot)
Start discord gateway connection

Args:

    token (str): User token
    user (Client): User client
    bot (_type_): Bot class

## selfcord.api.http module

Used for majority of discords interactions via the Discord HTTPS/REST API.


### _class_ selfcord.api.http.http()
Bases: `object`


#### _async_ encode_image(url)

#### _async_ get_cookie()

#### remove_dupes(item: dict)

#### _async_ request(method: str, endpoint: str, \*args, \*\*kwargs)
Used to send requests

Args:

    method (str): HTTP method
    endpoint (str): Discord api endpoint

Raises:

    LoginFailure: If you suck

Returns:

    dict: Data, json data


#### _async_ static_login(token: str)
Used to retrieve basic token information

Args:

    token (str): User token

Returns:

    Client: A Client object

## Module contents

Holds all classes to interact with Discord, includes interactions via the Discord API and Discord Gateway.

Discord API related modules, used to interact with discord
