# server setup bot by paranoia
# https://discord.gg/pr3dxBMVMu

import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="setup")
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    try:

        await ctx.send("This will **DELETE ALL** channels in the server. Type `!confirm` within 30 seconds to proceed.")

        def check(m):
            return m.author == ctx.author and m.content.lower() == "!confirm"

        try:
            await bot.wait_for('message', check=check, timeout=30)
        except:
            return await ctx.send("Setup cancelled. No confirmation received.")


        for channel in ctx.guild.channels:
            await channel.delete()

        # role configurations (change if you know what your doing)
        role_configs = {
            "Administrator": {
                "color": discord.Color.red(),
                "permissions": discord.Permissions(administrator=True)
            },
            "Moderator": {
                "color": discord.Color.blue(),
                "permissions": discord.Permissions(
                    kick_members=True,
                    ban_members=True,
                    manage_messages=True
                )
            },
            "Member": {
                "color": discord.Color.green(),
                "permissions": discord.Permissions()
            }
        }


        roles = {}
        for name, config in role_configs.items():
            existing = discord.utils.get(ctx.guild.roles, name=name)
            if existing:
                roles[name] = existing
            else:
                roles[name] = await ctx.guild.create_role(
                    name=name,
                    permissions=config["permissions"],
                    color=config["color"],
                    hoist=True
                )


        important_cat = await ctx.guild.create_category("📌 Important")
        community_cat = await ctx.guild.create_category("💬 Community")
        vc_cat = await ctx.guild.create_category("🔊 Voice Channels")


        rules_channel = await ctx.guild.create_text_channel("📜・rules", category=important_cat)
        await rules_channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await rules_channel.set_permissions(roles["Member"], send_messages=False)
              # server rules (will be sent in the rules channel) you can change if you want
        rules_text = """
**Server Rules** 📜

**Rule 1** - Any links/images/videos/streams about NSFW is not allowed. **[Kick > Ban]**  
**Rule 2** - No Spamming (For anti raid purposes) **[Mute > Kick]**  
**Rule 3** - Do not discuss/promote Hacking or Cheating in the server. **[Mute > Kick > Ban]**  
**Rule 4** - No advertising, self-promotion or general solicitation of any kind (Example: Sending links) **[Warn > Mute]**  
**Rule 5** - No racism, let's keep our community friendly. **[Warn > Mute > Kick]**  
**Rule 6** - Doxxing/Sending harmful links, even if it's fake, is not allowed. **[Kick > Ban]**  
**Rule 7** - Mocking someone’s death/critical condition is not allowed. **[Warn > Mute > Kick > Ban]**  
**Rule 8** - Respect staff at all times and avoid any form of toxicity/harassment **[Warn > Mute > Kick]**  
**Rule 9** - Strictly NO NSFW allowed in the server **[Mute > Kick > Ban]**  
**Rule 10** - Any form of Buying/Selling/Trading is not allowed **[Ban]**  
**Rule 11** - Leaking Personal Information (even if fake) is not allowed **[Mute > Kick > Ban]**  
**Rule 12** - Intentionally asking for a person's age is not allowed **[Warn > Ban]**  
**Rule 13** - Harassing and threatening others **[Warn > Mute]** (If the other reports they're being harassed/threatened, this rule applies.)

**Depending on the severity or number of violations, punishments may escalate. Repeated offenses (e.g. multiple NSFW posts) may result in instant ban.**
"""
        await rules_channel.send(rules_text)

       
        ann_channel = await ctx.guild.create_text_channel("📢・announcements", category=important_cat)
        welcome_channel = await ctx.guild.create_text_channel("👋・welcome", category=important_cat)
        for ch in [ann_channel, welcome_channel]:
            await ch.set_permissions(ctx.guild.default_role, send_messages=False)
            await ch.set_permissions(roles["Member"], send_messages=False)

       
        community_channels = ["💬・general", "🎨・media"]
        for name in community_channels:
            await ctx.guild.create_text_channel(name, category=community_cat)

        
        await ctx.guild.create_voice_channel("🎧・General VC", category=vc_cat)

        # assings the member role to all users
        for member in ctx.guild.members:
            if not member.bot and member != ctx.guild.owner:
                await member.add_roles(roles["Member"])

        await ctx.send("Server setup complete! Channels, roles, and rules are ready.")

    except Exception as e:
        await ctx.send(f"An error occurred: `{e}`")

# Run the bot
bot.run("YOURBOTTOKEN") # replace the "YOURBOTTOKEN with your bot's actual token
