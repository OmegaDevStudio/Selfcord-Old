# selfcord.api.voice package

## Submodules

## selfcord.api.voice.voice module


### _class_ selfcord.api.voice.voice.Voice(session_id: str, token: str, endpoint: str, server_id: str, bot)
Bases: `object`


#### CHANNELS(_ = _ )

#### FRAME_LENGTH(_ = 2_ )

#### HEARTBEAT(_ = _ )

#### HEARTBEAT_ACK(_ = _ )

#### READY(_ = _ )

#### SAMPLES_PER_FRAME(_ = 96_ )
Op codes


#### SAMPLE_SIZE(_ = _ )

#### SAMPLING_RATE(_ = 4800_ )

#### SESSION_DESCRIPTION(_ = _ )

#### checked_add(attr: str, value: int, limit: int)

#### _async_ close()
Close the connection to websocket


#### _async_ connect()
Connect to discord voice ws


#### _async_ convert(path)

#### encode_data(data: bytes)

#### encrypt_xsalsa20_poly1305(header: bytes, data)

#### get_voice_packet(encoded: bytes)

#### _async_ handle_description(data: dict)

#### _async_ handle_ready(data: dict)

#### _async_ heartbeat(data: dict)

#### _async_ identify()

#### _async_ ip_discovery()

#### _async_ play(path)

#### _async_ recv_msg()
Receives Message from websocket, encodes as json and runs tasks


#### _async_ send_audio_data(data: bytes)

#### _async_ send_json(payload: dict)
Send json to the websocket
Args:

> payload (dict): Valid payload to send to the gateway


#### _async_ speak(state: bool)

#### _async_ start()

#### _async_ udp_select()
## Module contents
