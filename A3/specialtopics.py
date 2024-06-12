#!/usr/bin/env python

import re
from typing import Callable, Pattern, Any


def regex_select(message: str, selector: Pattern) -> set[str]:
    mentions = re.findall(selector, message)

    return set(mentions)


def reChatParseCommand(message, state):
    """
    given an input `message` and a previous user state,
    parse the `message` input return an `action` and update the `state` appropriately
    """

    # base cases:
    # initial connection - set initial action and mode
    if (
        message == ""
        or type(state) == type(None)
        or [k for k in state.keys()][0] is None
    ):
        (action, state) = ({"action": "greeting"}, {"command": None})
        return action, state

    # '\quit' command - disconnect and clear state
    if message.__contains__("\\quit"):
        (action, state) = ({"action": "quit"}, {None: None})
        return action, state

    # regex to select a particular substring
    channel_selector = re.compile(r"^#[a-zA-Z0-9]+$")
    user_selector = re.compile(r"@[a-zA-Z\.]+@[a-zA-Z\.]+\.[\.a-zA-Z]+")

    # assign current mode to a variable
    curr_state = [k for k in state.keys()][0]
    argv = message.split(" ")  # list of input arguments
    input_invalid = (
        {"error": "Invalid command"},
        state,
    )  # assign `invalid` to variable

    dispatch = {
        "command": {
            # COMMAND MODE dispatcher functions
            # ---------------------------------
            #
            # `\join #<channel>` : transition from command mode to channel mode
            # if
            #   - <channel> is not a valid channel name (must use format: `#` followed by alphanumeric characters),
            # return invalid
            #
            # otherwise return
            #   - action: 'join',
            #   - channel: #<channel>,
            #   - state: channel mode
            "\\join": lambda argv: (
                ({"action": "join", "channel": argv[1]}, {"channel": argv[1]})
                if (regex_select(argv[1], channel_selector) != set())
                else input_invalid
            ),
            # `\list [channels, users]` : set the list action (remain in command mode)
            # if
            #   - `\list` is not followed by one of ['channels', 'users'],
            # return invalid,
            #
            # otherwise return
            #   - action: 'list',
            #   - param: ['channels' or 'users'],
            #   - do not modify state
            "\\list": lambda argv: (
                ({"action": "list", "param": argv[1]}, {"command": None})
                if argv[1] in ["channels", "users"]
                else input_invalid
            ),
            # `\dm <username>` : transition from command mode to dm mode
            # if
            #   - `<username>` is not a valid username
            # return invalid,
            #
            # otherwise return
            #   - action: 'dm'
            #   - user: <username>
            #   - state: dm mode
            "\\dm": lambda argv: (
                ({"action": "dm", "user": argv[1]}, {"dm": argv[1]})
                if (regex_select(argv[1], user_selector) != set())
                else input_invalid
            ),
        },
        "channel": {
            # CHANNEL MODE dispatcher functions
            # ---------------------------------
            #
            # `\leave` : transition from channel mode to command mode
            # if
            #   - state does not contain a valid channel name (must use format: `#` followed by alphanumeric characters),
            # return invalid
            #
            # otherwise return
            #   - action: 'leaveChannel',
            #   - channel: #<channel>,
            #   - state: command mode
            "\\leave": lambda argv: (
                (
                    {"action": "leaveChannel", "channel": state["channel"]},
                    {"command": None},
                )
                if (state["channel"] is not None)
                and (regex_select(state["channel"], channel_selector) != set())
                else input_invalid
            ),
            # `\read` : set the action to 'readChannel'
            # if
            #   - state does not contain a valid channel name (must use format: `#` followed by alphanumeric characters),
            # return invalid
            #
            # otherwise return
            #   - action: 'readChannel',
            #   - channel: #<channel>,
            #   - return the previous state
            "\\read": lambda argv: (
                ({"action": "readChannel", "channel": state["channel"]}, state)
                if (state["channel"] is not None)
                and (regex_select(state["channel"], channel_selector) != set())
                else input_invalid
            ),
        },
        "dm": {
            # DM MODE dispatcher functions
            # ---------------------------------
            #
            # `\leave` : transition from dm mode to command mode
            # if
            #   - `state` does not contain a valid username
            # return invalid
            #
            # otherwise return
            #   - action: 'leaveDM',
            #   - user: <username>
            #   - state: command mode
            "\\leave": lambda argv: (
                ({"action": "leaveDM", "user": state["dm"]}, {"command": None})
                if (state["dm"] is not None)
                and (regex_select(state["dm"], user_selector) != set())
                else input_invalid
            ),
            # `\read` : set the action to 'readDM'
            # if
            #   - state does not contain a valid username
            # return invalid
            #
            # otherwise return
            #   - action: 'readDM',
            #   - user: <username>,
            #   - return the previous state
            "\\read": lambda argv: (
                ({"action": "readDM", "user": state["dm"]}, state)
                if (state["dm"] is not None)
                and (re.findall(user_selector, state["dm"]) != [])
                else input_invalid
            ),
        },
    }

    dispatch_message = {
        # MESSAGE dispatch handler
        # ------------------------
        # return depends on whether we are in DM or channel mode:
        #   - action: 'post[DM, Channel]',
        #   - channel: unmodified from previous state,
        #   - message: the user's input message,
        #   - mentions: any <username> strings present in input
        #
        # validation is handled elsewhere, no need to check whether our
        # input is invalid here
        "channel": lambda msg: (
            (
                {
                    "action": "postChannel",
                    "channel": state["channel"],
                    "message": msg,
                    "mentions": regex_select(msg, user_selector),
                },
                {"channel": state["channel"]},
            )
        ),
        "dm": lambda msg: (
            (
                {
                    "action": "postDM",
                    "user": state["dm"],
                    "message": msg,
                    "mentions": regex_select(msg, user_selector),
                },
                {"dm": state["dm"]},
            )
        ),
    }

    # try/except block to handle commands that don't match a key in the state's dispatch table
    try:
        table_output = (
            # input = '\<cmd> <args?>'
            dispatch[curr_state][argv[0]](argv)
            if (argv[0].startswith("\\"))
            # state = one of ['channel', 'state'],
            # input = '<anything> <[usernames?]>'
            else (
                dispatch_message[curr_state](message)
                if (curr_state in ["channel", "dm"])
                # input is not a `\` command or we are not in a
                # messaging mode
                else input_invalid
            )
        )

    except KeyError:
        table_output = input_invalid

    # '\quit' is handled as base case as it can be called in any mode and doesn't conform to the
    # structure of the dispatch tables (ie, we don't try to unpack a `None` state from `table_output`)
    (action, state) = table_output

    return action, state


