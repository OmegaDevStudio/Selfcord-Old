# selfcord.api package

## Subpackages


* [selfcord.api.voice package](selfcord.api.voice.md)


    * [Submodules](selfcord.api.voice.md#submodules)


    * [selfcord.api.voice.voice module](selfcord.api.voice.md#module-selfcord.api.voice.voice)


        * [`Voice`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice)


            * [`Voice.CHANNELS`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.CHANNELS)


            * [`Voice.FRAME_LENGTH`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.FRAME_LENGTH)


            * [`Voice.HEARTBEAT`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.HEARTBEAT)


            * [`Voice.HEARTBEAT_ACK`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.HEARTBEAT_ACK)


            * [`Voice.READY`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.READY)


            * [`Voice.SAMPLES_PER_FRAME`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.SAMPLES_PER_FRAME)


            * [`Voice.SAMPLE_SIZE`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.SAMPLE_SIZE)


            * [`Voice.SAMPLING_RATE`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.SAMPLING_RATE)


            * [`Voice.SESSION_DESCRIPTION`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.SESSION_DESCRIPTION)


            * [`Voice.checked_add()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.checked_add)


            * [`Voice.close()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.close)


            * [`Voice.connect()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.connect)


            * [`Voice.convert()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.convert)


            * [`Voice.encode_data()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.encode_data)


            * [`Voice.encrypt_xsalsa20_poly1305()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.encrypt_xsalsa20_poly1305)


            * [`Voice.get_voice_packet()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.get_voice_packet)


            * [`Voice.handle_description()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.handle_description)


            * [`Voice.handle_ready()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.handle_ready)


            * [`Voice.heartbeat()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.heartbeat)


            * [`Voice.identify()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.identify)


            * [`Voice.ip_discovery()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.ip_discovery)


            * [`Voice.play()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.play)


            * [`Voice.recv_msg()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.recv_msg)


            * [`Voice.send_audio_data()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.send_audio_data)


            * [`Voice.send_json()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.send_json)


            * [`Voice.speak()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.speak)


            * [`Voice.start()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.start)


            * [`Voice.udp_select()`](selfcord.api.voice.md#selfcord.api.voice.voice.Voice.udp_select)


    * [Module contents](selfcord.api.voice.md#module-selfcord.api.voice)


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


#### _async_ handle_guild_role_delete(role: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
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


#### _async_ handle_voice_server_update(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles the voice server updating

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ handle_voice_state_update(data: dict, user: [Client](selfcord.models.md#selfcord.models.client.Client), http)
Handles the voice state updating

Args:

    data (dict): JSON data from gateway
    user (Client): The client instance
    http (http): HTTP instance


#### _async_ voice_start(voice: [Voice](selfcord.api.voice.md#selfcord.api.voice.voice.Voice))
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

#### _async_ call(channel: str, guild=None)
Initiates a discord call

Args:

    channel (str): Channel ID
    guild (str, optional): Guild ID. Defaults to None.


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


#### _async_ stream_call(channel: str, guild=None)
Initiates a discord stream call

Args:

    channel (str): Channel ID
    guild (str, optional): Guild ID. Defaults to None.


#### _async_ video_call(channel: str, guild=None)
Initiates a discord video call

Args:

    channel (str): Channel ID
    guild (str, optional): Guild ID. Defaults to None.

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
