# selfcord.utils package

## Submodules

## selfcord.utils.command module


### _class_ selfcord.utils.command.Command(\*\*kwargs)
Bases: `object`

Command Object pretty much


### _class_ selfcord.utils.command.CommandCollection(\*\*kwargs)
Bases: `object`

Commands collection, where commands are stored into


#### add(cmd)

#### append(collection)

#### clear()

#### copy()

#### get(alias, prefix='')

#### recents()

### _class_ selfcord.utils.command.Context(bot, message, http)
Bases: `object`

Context related for commands, and invokation


#### _property_ alias()

#### _property_ author()

#### _property_ channel()

#### _property_ command()

#### _property_ command_content()
The content minus the prefix and command name, essentially the args

Returns:

    str: String of content


#### _property_ content()

#### convert(param, value)
Attempts to turn x value in y value, using get_converter func for the values

Args:

    param (_type_): function parameter
    value (_type_): value in message

Returns:

    Type[str]: The type of parameter


#### _async_ get_arguments()
Get arguments by checking function arguments and comparing to arguments in message.

Returns:

    _type_: _description_


#### get_converter(param)

#### _property_ guild()

#### _async_ invoke()
Used to actually run the command


#### _property_ prefix()

#### _async_ purge(amount: Optional[int] = None)
Helper function to purge messages in the current channel, uses asyncio gather.

Args:

    amount (int): The amount of messages to purge, defaults to All.


#### _async_ reply(content: str, tts=False)
Helper function to reply to your own message containing the command

Args:

    content (str): The message you would like to send
    tts (bool, optional): Whether message should be tts or not. Defaults to False.


#### _async_ send(content: str, tts=False)
Helper function to send message to the current channel

Args:

    content (str): The message you would like to send
    tts (bool, optional): Whether message should be tts or not. Defaults to False.


#### _async_ spam(amount: int, content: str)
Helper function to spam messages in the current channel (uses asyncio.gather !!!!)

Args:

    amount (int): Amount of messages to spam
    content (str): The message you would like to send


### _class_ selfcord.utils.command.Event(name, coro, ext)
Bases: `object`


### _class_ selfcord.utils.command.Extender()
Bases: `object`


#### _classmethod_ add_cmd(coro, description='', aliases=[])
Function to add commands manually without decorator

Args:

    coro (coroutine): The function to add
    description (str, optional): Description of command. Defaults to “”.
    aliases (list, optional): Alternative names for command. Defaults to [].

Raises:

    RuntimeWarning: If you suck and don’t use a coroutine


#### _classmethod_ cmd(description='', aliases=[])
Decorator to add commands for the bot

Args:

    description (str, optional): Description of command. Defaults to “”.
    aliases (list, optional): Alternative names for command. Defaults to [].

Raises:

    RuntimeWarning: If you suck and don’t use a coroutine


#### commands(_ = <selfcord.utils.command.CommandCollection object_ )

#### _classmethod_ on(event: str)
Decorator for events

Args:

    event (str): The event to check for


### _class_ selfcord.utils.command.Extension(\*\*kwargs)
Bases: `object`

Extension object pretty much


### _class_ selfcord.utils.command.ExtensionCollection()
Bases: `object`

Extension collection, where extensions are stored into


#### add(ext)

#### get(alias, prefix='')
## Module contents

Utility related modules for selfcord
