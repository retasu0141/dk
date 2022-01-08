from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import random as r
import requests
import signal,os
from PIL import Image

import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import os

import random,time,asyncio
import datetime



options = Options()
options.add_argument('--incognito')
options.add_experimental_option('detach', True)
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get("https://www.musasi.jp/kurume/login")
driver.set_window_size(1400, 941)
wait = WebDriverWait(driver, 2)
WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located)

WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "signin_username"))).click()
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "signin_username"))).send_keys("30626")

WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "signin_password"))).click()
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "signin_password"))).send_keys("01234")

WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.NAME, "Signin"))).click()
sleep(0.2)
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "selfStudy"))).click()
sleep(0.2)
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "excersise"))).click()
sleep(0.2)
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "testRehearsal"))).click()



bot = commands.Bot(command_prefix="!",activity=discord.Game("!help"))
bot.remove_command('help')
token = os.environ['DISCORD_BOT_TOKEN']
matti_data = {}

@bot.event
async def on_ready():
    print('Botを起動しました。')

@bot.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.command(aliases=["開始","スタート"])
async def start(ctx):
    await ctx.send("開始します。画像と問題文が送られます。\n回答の際は[!まよった]の入力の有無後に[!まる]か[!ばつ]で答えてください。\n問題を終了する際は[!終了]と送信してください。\n\n")
    driver.get("https://www.musasi.jp/workbook/3/4411/no?workbook=17&start={}".format(str(r.choice([1,2,3,4,5,6]))))
    wait = WebDriverWait(driver, 2)
    WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located)
    sleep(0.2)
    driver.save_screenshot("./image/"+"Q"+'.png')
    word_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionContainer")))
    word = word_data.find_element_by_xpath('//div[@class="customScrollBox"]/div[@class="container"]/div[@class="content"]/p[@class="noBoth"]').get_attribute("textContent")
    print(word)
    await ctx.send(word)
    await ctx.send(file=discord.File("./image/"+"Q"+'.png'))



@bot.command(aliases=["迷った","まよった"])
async def unsure(ctx):
    a_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionsItems")))
    a_data.find_element_by_xpath('//a[@id="btn_unsure"]').click()


@bot.command(aliases=["まる","丸"])
async def true(ctx):
    a_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionsItems")))
    #a_data.find_element_by_xpath('//a[@id="btn_unsure"]').click()
    a_data.find_element_by_xpath('//a[@class="btn_true"]').click()
    #a_data.find_element_by_xpath('//a[@class="btn_false"]').click()
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_nextQuestion"))).click()
    sleep(0.2)
    driver.save_screenshot("./image/"+"Q"+'.png')
    word_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionContainer")))
    word = word_data.find_element_by_xpath('//div[@class="customScrollBox"]/div[@class="container"]/div[@class="content"]/p[@class="noBoth"]').get_attribute("textContent")
    print(word)
    await ctx.send(word)
    await ctx.send(file=discord.File("./image/"+"Q"+'.png'))


@bot.command(aliases=["ばつ","×"])
async def false(ctx):
    a_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionsItems")))
    #a_data.find_element_by_xpath('//a[@id="btn_unsure"]').click()
    #a_data.find_element_by_xpath('//a[@class="btn_true"]').click()
    a_data.find_element_by_xpath('//a[@class="btn_false"]').click()
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_nextQuestion"))).click()
    sleep(0.2)
    driver.save_screenshot("./image/"+"Q"+'.png')
    word_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "questionContainer")))
    word = word_data.find_element_by_xpath('//div[@class="customScrollBox"]/div[@class="container"]/div[@class="content"]/p[@class="noBoth"]').get_attribute("textContent")
    print(word)
    await ctx.send(word)
    await ctx.send(file=discord.File("./image/"+"Q"+'.png'))

@bot.command(aliases=["終了","おわり"])
async def finish(ctx):
    await ctx.send("お疲れ様です。結果と間違えた問題の写真を送信します。\n\n")
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_finish"))).click()
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_finishResultConfirm"))).click()
    driver.save_screenshot("./image/"+"A"+'.png')
    await ctx.send(file=discord.File("./image/"+"A"+'.png'))
    WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_review"))).click()
    try:
        for n in range(50):
            Re_data = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, "explanation")))
            Re_title = Re_data.find_element_by_xpath('//p[@class="title"]').get_attribute("textContent")
            driver.save_screenshot("./image/"+Re_title+'.png')
            im = Image.open("./image/"+Re_title+'.png')
            im_crop = im.crop((150, 300, 2250, 800))
            im_crop.save("./image/"+Re_title+"問題"+'.png', quality=95)
            await ctx.send(file=discord.File("./image/"+Re_title+"問題"+'.png'))
            im = Image.open("./image/"+Re_title+'.png')
            im_crop = im.crop((150 , 800, 2250, 1414))
            im_crop.save("./image/"+Re_title+"回答"+'.png', quality=95)
            await ctx.send(file=discord.File("./image/"+Re_title+"回答"+'.png'))
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "btn_nextQuestion"))).click()
    except:
        pass

bot.run(token)
