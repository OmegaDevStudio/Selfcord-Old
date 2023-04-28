# selfcord.api package

## Submodules

## selfcord.api.errors module


### _exception_ selfcord.api.errors.DiscordException()
Bases: `Exception`


### _exception_ selfcord.api.errors.Funnu(\*args: object)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.LoginFailure(message: dict, status: int)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.ReconnectWebsocket(message: str)
Bases: `DiscordException`


### _exception_ selfcord.api.errors.RuntimeError(message: str)
Bases: `DiscordException`

## selfcord.api.events module


### _class_ selfcord.api.events.EventHandler(bot, http)
Bases: `object`

Used to handle discord events


#### _async_ handle_channel_create(channel: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a channel is created

Args:

    channel (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_channel_delete(data, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a channel is deleted

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_guild_create(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a guild is created

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_guild_member_list_update(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a member chunk payload is received

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_guild_role_create(role, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a role is created

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_guild_role_delete(role, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a role is deleted

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_message_create(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a message is created, or sent
Args:

> data (dict): JSON data from gateway
> user (Client): The client instance
> http (http): HTTP instance


#### _async_ handle_message_delete(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when a message is deleted. Very little data will be logged if the message is not in the bots cache.

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_ready(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles what happens when the ready event is fired, when the bot first connects

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance

## selfcord.api.gateway module


### _class_ selfcord.api.gateway.Activity()
Bases: `object`


#### _static_ Game(name: str, details: str, state: str, buttons: dict, application_id: str, key: str)
Method to generate activity dict for the “Playing …” payload

Args:

    name (str): Name of the activity
    details (str): Details of the activity
    state (str): State of the activity
    buttons (dict): Buttons for the activity.
    Example:

    > { “My Website”: “[https://google.com](https://google.com)”}

    application_id (str): Application ID
    key (str): Key for the large image

Returns:

    dict[str, int]: Dict for the activity object for payload


#### _static_ Listen(name: str, details: str, state: str, buttons: dict, application_id: str, key: str)
Method to generate activity dict for the “Listening …” payload

Args:

    name (str): Name of the activity
    details (str): Details of the activity
    state (str): State of the activity
    buttons (dict): Buttons for the activity.
    Example:

    > { “My Website”: “[https://google.com](https://google.com)”}

    application_id (str): Application ID
    key (str): Key for the large image

Returns:

    dict[str, int]: Dict for the activity object for payload


#### _static_ Stream(name: str, details: str, state: str, url: str, buttons: dict, application_id: str, key: str)
Method to generate activity dict for the “Streaming …” payload

Args:

    name (str): Name of the activity
    details (str): Details of the activity
    state (str): State of the activitiy
    url (str): URL for streaming
    buttons (dict): Buttons for the activity.
    Example:

    > { “My Website”: “[https://google.com](https://google.com)”}

    application_id (str): Application ID
    key (str): Key for the large image

Returns:

    dict[str, int]: Dict for the activity object for payload


#### _static_ Watch(name: str, details: str, state: str, buttons: dict, application_id: str, key: str)
Method to generate activity dict for the “Watching …” payload

Args:

    name (str): Name of the activity
    details (str): Details of the activity
    state (str): State of the activity
    buttons (dict): Buttons for the activity.
    Example:

    > { “My Website”: “[https://google.com](https://google.com)”}

    application_id (str): Application ID
    key (str): Key for the large image

Returns:

    dict[str, int]: Dict for the activity object for payload


### _class_ selfcord.api.gateway.gateway(http, show_heartbeat=False)
Bases: `object`

OP CODES


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

#### _async_ change_presence(status: str, afk: bool, activity: dict)
Change the clients current presence

Args:

    status (str): online, offline or dnd
    afk (bool): Whether client is set as AFK
    activity (Activity): Activity object


#### chunks(lst, n)

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


#### _async_ lazy_chunk(guild_id: str, channel_id: str, amount: int)
Sends lazy guild request to gather current online members

Args:

    guild_id (str): The guild id specified
    channel_id (str): The channel id specified


#### _async_ leave_call()
Leaves a discord call


#### _async_ recv_msg()
Receives Message from gateway, encodes as json and does things depending on op code


#### _async_ ring(channel: str, guild=None)
Initiates a discord call

Args:

    channel (str): Channel ID
    guild (str, optional): Guild ID. Defaults to None.


#### roundup(n)

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


### _class_ selfcord.api.http.http()
Bases: `object`


#### _async_ encode_image(url: str)
Turn an image url into a b64 payload

Args:

    url (str): The URL of the image

Returns:

    str: The b64 payload


#### _async_ get_cookie()
Gather cookie for user upon client start


#### remove_dupes(dictionary: dict)

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

Discord API related modules, used to interact with discord
