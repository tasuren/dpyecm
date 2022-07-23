".. include:: ../readme.md" # dpyecm

from __future__ import annotations

from typing import TypeAlias, Union, Any
from collections.abc import Sequence

import discord


__version__ = "0.1.0"
__author__ = "tasuren"


__all__ = ("CallbackObj", "SelectExtendContextMenuView", "ExtendContextMenu")
CallbackObj: TypeAlias = Union[discord.Message, discord.User, discord.Member]
"Alias of the type Union of the object that the callback may receive."


class SelectExtendContextMenuView(discord.ui.View):
    """This View implements a select box for selecting other additionally registered context menus.

    Args:
        ecm: An instance of `ExtendContextMenu`.
        interaction: `discord.Interaction` using this View.
        *args: Arguments to be passed to super class's constructor.
        **kawrgs: Keyword arguments to be passed to super class's constructor."""

    placeholder = "Select what you want to order"

    def __init__(
        self, ecm: ExtendContextMenu, interaction: discord.Interaction,
        obj: CallbackObj, *args: Any, **kwargs: Any
    ):
        self.ecm, self.obj = ecm, obj
        super().__init__(*args, **kwargs)
        self.contexts: list[discord.app_commands.ContextMenu] = [
            context for context in self.ecm.contexts
            if not isinstance(context._guild_ids, list) or (
                interaction.guild_id is not None
                and interaction.guild_id in context._guild_ids
            )
        ]
        select, count = self.make_select(), 0
        for context in self.contexts:
            count += 1
            select.add_option(label=context.name, value=context.name)
            if count == 25:
                self.add_item(select)
                select = self.make_select()
                count = 0
        if count != 0:
            self.add_item(select)

    def make_select(self) -> discord.ui.Select:
        "Function to return a select for an additional context menu."
        select = discord.ui.Select(placeholder=self.placeholder)
        select.callback = self.callback
        return select

    async def callback(self, interaction: discord.Interaction) -> None:
        "Function called when a select is selected for an additional context menu."
        for item in self.children:
            if isinstance(item, discord.ui.Select):
                if not item.values:
                    continue
                for context in self.contexts:
                    if context.name == item.values[0]:
                        await context.callback(interaction, self.obj) # type: ignore
                        return


class ExtendContextMenu:
    """Cog to register more than 5 context menus.
    Here's how it works:
    Registers a single context menu.
    When the item in the context menu is clicked, another registered context menu item is selected in the select box.
    Executes the selected context menu item.
    This allows you to run more context menus than you can.

    Args:
        tree: Command tree.
        name: The name of the context menu to be created to display a select menu that contains the context menu to be expanded.
        guild: A guild that can use this context menu.
        guilds: Guilds that can use this context menu.
        **kwargs: Keyword arguments to be passed to `discord.app_commands.ContextMenu`."""

    def __init__(
        self, tree: discord.app_commands.CommandTree, type_: discord.AppCommandType,
        name: str = "Other", guild: discord.abc.Snowflake | None = discord.utils.MISSING,
        guilds: Sequence[discord.abc.Snowflake] = discord.utils.MISSING, **kwargs: Any
    ):
        self.tree = tree
        self.contexts: list[discord.app_commands.ContextMenu] = []
        callback = self._callback_for_message
        if type_ == discord.AppCommandType.user:
            callback = self._callback_for_user
        if "guild_ids" not in kwargs and (guild or guilds):
            kwargs["guild_ids"] = [guild.id] if guild else [guild.id for guild in guilds]
        self.tree.add_command(discord.app_commands.ContextMenu(
            name=name, callback=callback, type=type_, **kwargs
        ), guild=guild, guilds=guilds)

    def get_reply_kwargs(self, interaction: discord.Interaction, obj: CallbackObj) -> dict[str, Any]:
        """Returns an argument to be passed to the function `discord.InteractionResponse.send_message` when replying with a select box for selecting an item in a context menu registered with other additions.
        Override if you want to customize it.

        Args:
            interaction: `discord.Interaction`.
            obj: Any of the objects that the callback may receive.
                For example, if the context menu is a message context menu, it will be a message object."""
        return {
            "content": "Choose what you want to do.", "ephemeral": True,
            "view": SelectExtendContextMenuView(self, interaction, obj)
        }

    async def callback(self, interaction: discord.Interaction, obj: CallbackObj) -> None:
        """Callback called when a context menu added by this class is selected to display a select box for selecting a context menu added elsewhere.

        Args:
            interaction: `discord.Interaction`.
            obj: Any of the objects that the callback may receive.
                For example, if the context menu is a message context menu, it will be a message object."""
        await interaction.response.send_message(**self.get_reply_kwargs(interaction, obj))

    async def _callback_for_message(self, interaction: discord.Interaction, obj: discord.Message) -> None:
        await self.callback(interaction, obj)
    async def _callback_for_user(self, interaction: discord.Interaction, obj: discord.User) -> None:
        await self.callback(interaction, obj)

    def add_context(self, context: discord.app_commands.ContextMenu) -> None:
        """Add a context menu.

        Args:
            context: This is the context menu to be expanded."""
        self.contexts.append(context)

    def remove_context(self, target: discord.app_commands.ContextMenu | str, guild_id: int | None = None) -> None:
        """Deletes the context menu specified by the name of the context menu object or context menu.
        The function also returns the deleted context.
        If it is a non-existent context menu, a `KeyError` or `ValueError` is occured.

        Args:
            target: The object or name of the context menu to be deleted.
            guild_id: The guild ID from which the context menu to delete can be run."""
        if isinstance(target, str):
            for index, context in enumerate(self.contexts):
                if context.name == target and (
                    guild_id is None or guild_id in context._guild_ids # type: ignore
                ):
                    del self.contexts[index]
                    break
            else:
                raise ValueError(target)
        else:
            self.contexts.remove(target)