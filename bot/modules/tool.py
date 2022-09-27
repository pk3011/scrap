import asyncio
import io
import os
import sys
import traceback
from getpass import getuser

from pyrogram import Client, filters

from bot import CMD, Config
from bot.helpers.utilities.terminal import Terminal


@Client.on_message(filters.command(CMD.TEML) & filters.user(Config.AUTH_USER))
async def teml(bot, update):
    cmd = update.text.split(" ", 1)
    if len(cmd) == 1:
        await update.reply_text("No command to execute was given.")
        return
    cmd = cmd[1]
    try:
        t_obj = await Terminal.execute(cmd)
    except Exception as t_e:
        await update.reply(f"**ERROR:** `{t_e}`")
        return
    curruser = getuser()
    try:
        uid = os.geteuid()
    except ImportError:
        uid = 1
    output = f"`{curruser}:~#` `{cmd}`\n" if uid == 0 else f"`{curruser}:~$` `{cmd}`\n"
    count = 0
    k = None
    while not t_obj.finished:
        count += 1
        await asyncio.sleep(0.5)
        if count >= 5:
            count = 0
            out_data = f"{output}`{t_obj.read_line}`"
            try:
                if not k:
                    k = await update.reply(out_data)
                else:
                    await k.edit(out_data)
            except BaseException:
                pass
    out_data = f"`{output}{t_obj.get_output}`"
    if len(out_data) > 4096:
        if k:
            await k.delete()
        with open("terminal.txt", "w+") as ef:
            ef.write(out_data)
            ef.close()
        await update.reply_document("terminal.txt", caption=cmd)
        os.remove("terminal.txt")
        return
    send = k.edit if k else update.reply
    await send(out_data)


@Client.on_message(filters.command(CMD.RUNF) & filters.user(Config.AUTH_USER))
async def eval(bot, update):
    status_m = await update.reply_text("`Processing...`")
    cmd = update.text.split(" ", 1)
    if len(cmd) == 1:
        await update.reply_text("No command to execute was given.")
        return
    cmd = cmd[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, bot, update)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = (
        "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
            cmd, evaluation.strip()
        )
    )

    if len(final_output) > Config.MAX_MESSAGE_LENGTH:
        OUTPUT = clear_string(OUTPUT)
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "eval.txt"
            await update.reply_document(
                document=f,
                caption=f"<code>{cmd}</code>",
            )
        await status_m.delete()
    else:
        await status_m.edit(final_output)
    await update.delete()
    return


async def aexec(code, bot, update):
    exec(
        f"async def __aexec(bot, update): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](bot, update)
