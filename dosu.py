import discord, random, os, string, requests
from discord.ext import commands
from discord.ext.commands import Bot

from osuapi import OsuApi, ReqConnector

osu_key = 'OSU_API_KEY_GOES_HERE'
bot_key = 'DISCORD_BOT_KEY_GOES_HERE'

api = OsuApi(osu_key, connector=ReqConnector())
bot = commands.Bot(command_prefix='dosu ')

# If you're going to use the emojis that were pre-assigned to this bot, DM @boop#1692 to get you bot added to the server.
# Also, A little credit pls <3

def changeToEmoji(letter):
    value = ''
    if letter == "A":
        value = "<:A_:463922386647908382>"
    elif letter == "S":
        value = '<:S_:463922496081625100>'
    elif letter == "SH":
        value = "<:S_:463922547382288385>"
    elif letter == "X":
        value = "<:SS:463922656668811265>"
    elif letter == "XH":
        value = "<:SS:463922701925613569>"
    elif letter == "B":
        value = "<:B_:464028170434248705>"
    elif letter == 'C':
        value = "<:C:464028225211727874>"
    elif letter == 'D':
        value = '<:D:464028285521756180>'
    else:
        value = "**[{}]**".format(letter.upper())
    return value

@bot.event
async def on_ready():
    print("Welcome to dOsu!\nClick the cirlces!")

@bot.command(pass_context=True)
async def get_stats(ctx, user):
    """Get stats on a user"""
    results = api.get_user(user)
    
    string = """
<:300:463916719208005638> {0[0].count300} <:100:463916808643149824> {0[0].count100} <:50:463916860253929474> {0[0].count50}
<:A_:463922386647908382> {0[0].count_rank_a} <:S_:463922496081625100> {0[0].count_rank_s} <:S_:463922547382288385> {0[0].count_rank_sh} <:SS:463922656668811265> {0[0].count_rank_ss} <:SS:463922701925613569> {0[0].count_rank_ssh}
:star: **Total Score:** {0[0].total_score} **Ranked Score:** {0[0].ranked_score}
:chart_with_upwards_trend: **Global Ranking:** #{0[0].pp_rank} ({0[0].pp_raw}pp) **Local Ranking:** {0[0].pp_country_rank}
:arrow_up: **Level:** {0[0].level} **Plays:** {0[0].playcount}
:ping_pong: **Accuracy:** {1}%
[Click Here to view this user's account](https://osu.ppy.sh/users/{0[0].user_id})
    """.format(results, round(results[0].accuracy,2))
    osuStats = discord.Embed()
    osuStats.add_field(name="**{0[0]}'s Statistics**".format(results), value=string)
    osuStats.set_footer(text="dOSU was built by boop#1692")
    await bot.send_message(ctx.message.channel, embed=osuStats)

@bot.command(pass_context=True)
async def best_scores(ctx, user):
    """Gets stats on a user's best scores!"""
    results = api.get_user_best(user, limit=5)
    print(results)
    strings = []
    for score in results:
        beatmap_instance = api.get_beatmaps(beatmap_id=score.beatmap_id)
        str2 = """[{1.title}](https://osu.ppy.sh/beatmaps/{0.beatmap_id}) **"{1.version}"** [{2}:star:]
{3} **Score:** {0.score} | **MaxCombo:** {0.maxcombo}
<:300:463916719208005638> {0.count300} <:100:463916808643149824> {0.count100} <:50:463916860253929474> {0.count50} <:miss:463917908364361729> {0.countmiss}
""".format(score, beatmap_instance[0], round(beatmap_instance[0].difficultyrating, 2), changeToEmoji(score.rank))
        strings.append(str2)
    big_string = ":medal: {0}'s Best Plays\n".format(user)
    for map in strings:
        big_string = big_string + "\n{}".format(map)
    print(len(big_string))
    osuStats2 = discord.Embed(description=big_string)
    #osuStats2.set_description(text=big_string)
    osuStats2.set_footer(text="Hey there, I'm a feetor")
    await bot.send_message(ctx.message.channel, embed=osuStats2)

@bot.command(pass_context=True)
async def recent_scores(ctx, user):
    """Gets stats on a user's recent scores!"""
    results = api.get_user_recent(user, limit=5)
    print(results)
    strings = []
    for score in results:
        beatmap_instance = api.get_beatmaps(beatmap_id=score.beatmap_id)
        str2 = """[{1.title}](https://osu.ppy.sh/beatmaps/{0.beatmap_id}) **"{1.version}"** [{2}:star:]
{3} **Score:** {0.score} | **MaxCombo:** {0.maxcombo}
<:300:463916719208005638> {0.count300} <:100:463916808643149824> {0.count100} <:50:463916860253929474> {0.count50} <:miss:463917908364361729> {0.countmiss}
""".format(score, beatmap_instance[0], round(beatmap_instance[0].difficultyrating, 2), changeToEmoji(score.rank))
        strings.append(str2)
    big_string = ":clock1: {0}'s Recent Plays\n".format(user)
    for map in strings:
        big_string = big_string + "\n{}".format(map)
    print(len(big_string))
    osuStats2 = discord.Embed(description=big_string)
    #osuStats2.set_description(text=big_string)
    osuStats2.set_footer(text="Hey there, I'm a feetor")
    await bot.send_message(ctx.message.channel, embed=osuStats2)

bot.run(bot_key)