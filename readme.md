[![PyPI](https://img.shields.io/pypi/v/dpyecm)](https://pypi.org/project/dpyecm/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dpyecm) ![PyPI - Downloads](https://img.shields.io/pypi/dm/dpyecm) ![PyPI - License](https://img.shields.io/pypi/l/dpyecm) [![Discord](https://img.shields.io/discord/777430548951728149?label=chat&logo=discord)](https://discord.gg/kfMwZUyGFG) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)
# dpyecm
A library to add more context menus that can be used in discord.py 2.0.  
It is implemented by creating a context menu that displays a select box for selecting a context menu.

## Example
```python
...

from dpyecm import ExtendContextMenu

...

ecm = ExtendContextMenu(tree, discord.AppCommandType.user)

@discord.app_commands.context_menu()
async def show_id(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"This member's id is `{member.id}`.", ephemeral=True
    )
ecm.add_context(test)

...
```
<img width="522" alt="dpyecm" src="https://user-images.githubusercontent.com/45121209/180586407-91eff192-419b-4a78-ba8b-cf57a627c7ec.png">

## Documentation
Documentation is avaliable at [here](https://tasuren.github.io/dpyecm)

## License
MiT License
