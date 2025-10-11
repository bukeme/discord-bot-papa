import discord
from discord.ext import commands
# from google import genai
import google.generativeai as genai
from collections import defaultdict
from keep_alive import keep_alive
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize Gemini client
# client = genai.Client(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
genai.configure(api_key=GEMINI_API_KEY)

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# FAQ_CONTEXT = """
# Forex Funds Flow FAQ:
# 1. What is Forex Funds Flow? -> Forex Funds Flow is a proprietary trading firm...
# 2. How do payouts work? -> Payouts are processed within X days...
# 3. What are the account sizes? -> We offer $10k, $25k, $50k accounts...
# ...
# """

FAQ_CONTEXT = """
# Forex Funds Flow FAQ.
Give users a brief response to their question from the text below. Answer users like you would answer a typical customer or user.
Here is the text:
Forex Funds Flow (FFF) — FAQ 
1. General Questions 
Q1: What is Forex Funds Flow (FFF)? 
A proprietary trading firm that funds skilled traders with capital to trade the forex and related markets. Traders keep a portion of profits while we cover the risk. 
Q2: How does it work? 
You start by purchasing a challenge for one of our account sizes ($5K, $10K, $25K, $50K, or $100K). After passing the evaluation phase(s), you receive a funded account where you trade and earn profit splits. 
Q3: Who can join Forex Funds Flow? 
Anyone aged 18+ from eligible countries with trading experience can apply. We exclude residents of countries sanctioned by the UN, OFAC, FATF, and other regulatory bodies: Somalia, Tanzania, North Korea, Angola, Venezuela, Haiti, Croatia, Lebanon, Iran, West Bank, Syria, Mali, Sudan, Burkina Faso, Myanmar, Yemen, South Sudan, Mozambique, Monaco, Cameroon, Algeria, Nepal, Russia, Congo, Côte d’Ivoire, Ukraine. 
Q4: Do I need a license to trade with you? 
No. Traders operate with virtual capital (demo accounts) and receive profit splits, so no formal trading license is required. 
2. Program Structure & Account Types 
Q5: What account sizes do you offer? 
$5,000, $10,000, $25,000, $50,000, and $100,000 challenge accounts. 
Q6: How many phases are in the challenge? 
We offer several challenge models, including: 
● 1 Step Challenge (FFF Risk Taker) 
● 2 Step Challenge (FFF Elite Trader)
● FFF Boost Instant Funding


Q7: What are the trading objectives? 
Examples: 
● 1 Step Challenge: 10% profit target, 4% daily drawdown, 6% trailing max drawdown. 
● 2 Step Challenge: Phase 1 – 10% target, Phase 2 – 5% target, 4% daily drawdown, 12% max drawdown. 
Q8: What is the leverage offered? 
Up to 60:1 on Forex, 20:1 Metals, 10:1 Indices, 10:1 on Oil; and 2:1 on Crypto, with paid add-ons 
Standard Leverage offered on all plans: 30:1 on Forex, 10:1 Metals, 10:1 Indices, 5:1 Oil, and 1:1 Crypto 
Q9: What platforms can I trade on? 
MT5 (Coming Soon), DXtrade, cTrader, Match Trader. 
3. Rules & Trading Conditions 
Q10: What instruments can I trade? 
Forex majors and minors, Metals (Gold, Silver), Indices, Oil, Cryptocurrencies. 
Q11: Are there trading hours or restrictions? 
No News trading 5 minutes before and after major “red folder” news events (ForexFactory standard). Crypto trading allowed 24/7, including weekends.. 
Q12: Can I use Expert Advisors (EAs) or copy trading? 
The use of EA’s requires confirmation from our team before proceeding. No HFT EA’s Allowed whatsoever
Q13: What happens if I break a rule? 
Breaking rules results in challenge failure and account closure. A new challenge purchase is required to restart. 
Q14: How do you detect rule violations? 
Both automated and manual monitoring detect irregular behavior such as arbitrage, tick scalping, latency abuse, and more. 
4. Payouts & Scaling 
Q15: How do payouts work? 
First payout is available after 14 days of trading. Subsequent payouts are bi-weekly.Minimum payout is $50. 
Q16: What’s the profit split? 
75% profit split at start. Add-on available to increase profit split to 90%. 
Q17: Do you offer a scaling plan? 
Yes, traders can scale to higher capital upon meeting performance criteria. Kindly, visit or VIP Plan to learn more 
Q18: How are payouts sent? 
Via Crypto, Wire Transfer - More Methods will be added in the future 
5. Fees & Refunds 
Q19: Is the challenge fee refundable? 
Yes, the fee is refunded with your 3rd payout. 
Q20: Do you offer discounts or promotions? 
Kindly, join our discord server, sign up on our mail list, and follow us on social media to find the latest discount codes available 
Q21: What happens if I fail the challenge? 
You must repurchase a new challenge to try again. 
6. Technical Support & Help
Q22: How do I get support? 
Support is available 24/7 via Email, Discord, and Live Chat. 
Q23: I’m having issues with my platform — what should I do? 
Contact support with detailed information and screenshots to assist quickly. 
7. Compliance & Integrity 
Q24: Is Forex Funds Flow regulated? 
No. We are not a brokerage and do not hold client funds. We provide simulated capital for funded traders to earn profit splits. 
Q25: Do you use real funds or demo accounts? 
Funded accounts trade with virtual/demo capital. Payouts are made from company profits. 
Q26: Can I get banned from joining again if I break the rules? 
Yes. Multiple violations or fraud attempts may lead to permanent ban. 
8. Affiliate & Community 
Q27: Do you have an affiliate program? 
Yes, paying 15% commission on first purchases and 10% on subsequent purchases. We built a tiered affiliate program. Make sure to take advantage of it! 
Q28: Where can I find your community? 
Join our Discord, follow us on Twitter, instagram,, and watch for announcements, live events, and trader competitions. 
limit for today would be $95,000. 

What leverage is offered? 
● Forex: Up to 1:60 
● Metals: Up to 1:20 
● Indices: Up to 1:10 
● Oils: Up to 1:10 
● Cryptocurrencies: Up to 1:2 
Standard Leverage offered on all plans: 30:1 on Forex, 10:1 Metals, 10:1 Indices, 5:1 Oil, and 1:1 Crypto 
Can I hold positions over the weekend?
● All trades must be closed by Friday 3:45 PM EST unless you purchase the Hold Over Weekend add-on. 
● Any open positions after this time will be automatically closed (soft breach). 
What is the "Flat for Weekend" rule? 
Positions must be flat (closed) on weekends unless the Weekend Hold add-on is purchased at the time of account setup. 
What is the difference between a Hard Breach and a Soft Breach? 
● Hard Breach: Violation of daily loss limit, max drawdown, or inactivity rules results in account closure. 
● Soft Breach: Minor rule violations, such as holding trades over the weekend without the add-on, result in closing the violating trades but allow continued trading. 
Is there an inactivity rule? 
Yes. If no trades are placed within 30 days, your account will be closed for inactivity (hard breach). 
What is 1 lot equal to on the trading platform? 
● Forex: $100,000 notional 
● Index: 1 lot = 1 contract (exceptions below) 
● SPX500: 1 lot = 10 contracts 
● JPN225: 1 lot = 500 contracts 
● Cryptos: 1 lot = 1 coin 
● Silver: 1 lot = 5,000 ounces 
● Gold: 1 lot = 100 ounces 
● Oil: 1 lot = 100 barrels
Are there position limits? 
Maximum open positions depend on your available margin. The company reserves the right to increase margin requirements, limit open positions, or halt trading based on market conditions. 
Instant Funded Accounts Overview 
What is the FFF Boost Instant Funding Plan? 
A funded account is provided immediately after payment, without an assessment or challenge phase. You receive a fully funded account to trade instantly. You will need to complete 3 minimum trading days
How long does it take to receive my funded account? 
You will receive an account and login instructions shortly after payment confirmation. Do I need to complete KYC or sign a contract before trading? 
No, not initially. KYC and a signed trading contract are required only when requesting withdrawals. 
What happens if I fail KYC? 
Your withdrawal will be rejected, and your funded account closed. Please ensure you can meet KYC requirements before opting for Instant Funding. 
Are prices or trade executions manipulated? 
No. All pricing and executions are provided directly by the Broker without markup or manipulation. 
Can I use automated trading strategies? 
Yes, except those expressly prohibited by the company or Broker. 
What trading platforms are supported? 
● Platform 5 (coming soon) 
● DXtrade
● MatchTrader 
● cTrader 
How many Instant Funded Accounts can I have? 
A maximum of $100,000 in active FFF Boost Instant Funded Plans per person is allowed. What products can I trade? 
All products offered by the Broker, including Forex pairs, CFDs on Indices, Metals, and Cryptocurrencies. 
Available Add-Ons: 
● Hold Over Weekend (10% extra): Allows positions to remain open over weekends. 
● Profit Share Increase to 90% (20% extra): Increases trader’s profit share from 80% to 90%. 
General Questions 
Who can participate? 
● Traders must be 18 years or older (or legal age in their jurisdiction). 
● US residents are prohibited. 
● Traders from all other countries except OFAC-sanctioned countries may participate. 
How do I track my account progress? 
You will get access to a real-time trader dashboard upon purchase. 
How are charges shown on statements? 
Payments appear under the name FF Flow Limited, or Fx Funds Flow Limited How are taxes handled?
Traders are independent contractors responsible for their own taxes on profits. 
Trading Policies & Prohibited Activities 
What trading activities are prohibited? 
Prohibited activities include but are not limited to: 
● Exploiting platform or pricing errors 
● Using insider or non-public information 
● Front-running trades 
● Trading that jeopardizes Broker relationships or causes trade cancellations ● Using third-party or off-the-shelf challenge-passing strategies 
● Arbitraging between accounts 
● Opening positions within 5 minutes before or after news events 
● Reverse hedging 
● Gambling or reckless risk-taking (e.g., max leverage hoping for a single price move) Violation may lead to account closure and forfeiture of fees. 
   Prohibited Trading Strategies (Forex Funds Flow) 
To maintain a fair trading environment and protect the integrity of our programs, the following trading practices are strictly prohibited on all Forex Funds Flow accounts. Engaging in any of these may result in account termination, loss of funded status, and forfeiture of profits: 
1. Latency Arbitrage / High-Frequency Arbitrage 
Exploiting price feed delays between brokers or platforms to profit from stale prices. 2. Copy Trading / Account Mirroring
Copying trades from another account (including funded or evaluation accounts) using software, trade copiers, or manual mirroring. This includes internal or external copying. 
3. Reverse Trading 
Opening opposite positions on multiple accounts with the goal of guaranteeing profit on at least one account. 
4. Grid or Martingale Strategies 
Using infinite lot sizing or lot doubling tactics that can bypass drawdown limits by relying on eventual reversals rather than sound risk management. 
5. News Trading Abuse 
Executing trades 5 minutes before, or 5 minutes after high-impact news events purely to exploit volatile market spikes is strictly prohibited. This includes (pending orders, buy limits, sell limits, Tp’s,SL’s) 
Traders can open trades 5 hours before scheduled red folder news, and hold through the news. If take profit triggers the trade will count. 
6. Tick Scalping / Platform Exploits 
Placing rapid in/out trades (typically within milliseconds to a few seconds) solely to exploit minor tick movements or demo environment flaws. 
7. Lot Size Manipulation 
Opening disproportionately large lot sizes compared to your average risk per trade to pass targets quickly and withdraw payouts without consistent risk management. 
8. Intentional Drawdown Breaching 
Deliberately violating drawdown rules after payout or profit split to reset or test limits. This includes "blow and go" strategies. 
9. Soft Arbitrage / Hedging Across Brokers 
Hedging trades between different brokers or platforms to lock in risk-free profits, including taking long on one and short on another. 
10. EA or Bot Trading Without Approval
Using Expert Advisors (EAs), bots, or algorithms that haven't been pre-approved. Even approved EAs must not violate any of the prohibited strategies listed here. 
11. Trade Manipulation via Lot Size Stacking 
Layering trades rapidly to manipulate platform pricing, execution, or commissions. 12. Using Delayed Data Feeds or Plug-ins 
Trading using tools or plugins that delay price feeds or distort market data for arbitrage or unfair advantage. 
13. Passing Accounts for Others / Selling Funded Accounts 
Account credentials must not be shared or sold. Only the trader who registered can operate the account. 
⚠ Important: 
Forex Funds Flow uses advanced monitoring tools to detect and review suspicious trading activity. If we detect that any of the above violations have occurred, we reserve the right to take immediate action, including disabling accounts and denying profit withdrawals. 
Maximum Capital Allocation – FAQ 
Q1: What is the maximum funding I can receive from Forex Funds Flow? The maximum capital you can be funded with at any given time is $100,000. This applies across all active funded accounts combined. 
Q2: How many challenges can I purchase at once? 
You can purchase up to $200,000 worth of challenges at any time. 
Examples: 
● 2 × 100k challenges 
● 4 × 50k challenges
● 1 × 100k + 2 × 50k challenges 
However, even if you pass them all, you can only be funded with $100,000 live capital at once. 
Q3: What happens if I pass multiple challenges? 
You may pass multiple challenges, but you must choose which funded accounts to activate, keeping your live capital at or below $100,000. 
You can pause one funded account and activate another anytime — just never exceed the cap. 
Q4: Can I hold two 100k funded accounts at once? 
No. Even if you pass two 100k challenges, you can only activate one at a time. You must deactivate one before switching. 
Q5: Can I rotate between funded accounts? 
Yes! You can switch funded accounts by deactivating one and activating another, as long as the total funded amount stays within $100,000. 
Q6: What’s the 30-Day Inactivity Rule? 
If you don’t place any trades for 30 consecutive days on a funded account, it will be considered inactive and may be closed permanently. 
However: 
This rule does NOT apply if: 
● You have already reached the $100,000 funding limit, and 
● You have a funded account awaiting activation, and 
● You are actively trading on at least one funded account. 
In this case, your other funded accounts will remain protected until you rotate them in.
Q7: Can I merge my funded accounts? 
Yes, account merging is supported up to 100k of funded accounts at any given time. 
Q8: What if I try to bypass the cap using multiple identities or accounts? Strictly prohibited. Doing so will result in account termination, blacklisting, and forfeiture of all payouts. 
VPN & VPS Usage – FAQ (Forex Funds Flow) 
Q: Can I use a VPN (Virtual Private Network) while trading with Forex Funds Flow? 
No. The use of VPNs is strictly prohibited. We require traders to operate from their actual physical location to ensure transparency, compliance, and fair usage of our services. 
Q: Can I use a VPS (Virtual Private Server) for my trading activities? 
No. VPS usage is also not allowed. All trades must be executed manually and directly by the trader to ensure accurate performance evaluation and to prevent automation, signal copying, or unauthorized third-party access. 
Q: Why are VPNs and VPSs banned? 
We prohibit VPNs and VPSs to prevent: 
● Identity masking or IP spoofing 
● Automated trading or copy trading systems 
● Multi-account abuse or coordinated trading schemes 
● Geographic misrepresentation that violates our regional policies 
Maintaining a secure and fair trading environment for all traders is our top priority. Q: What happens if I’m found using a VPN or VPS?
Any detected use of VPNs, VPSs, or similar masking/automation tools will result in immediate account suspension or disqualification, with no eligibility for refunds or payouts. 
Q: What if I need to travel or my IP changes for a valid reason? 
If you're planning to travel or expect your IP/location to change, please notify our support team beforehand. We may request additional verification to ensure the integrity of your account. 
Q: Can I use mobile hotspots or dynamic IPs? 
Yes, as long as you're not using VPNs, VPSs, or proxy tools to intentionally hide or manipulate your connection. Any suspicious behavior will be investigated. 
Q: How do you detect VPN or VPS usage? 
We use advanced security systems and IP detection tools to monitor trading activity, location, and connectivity patterns. Attempts to bypass these systems may result in permanent bans. 
Q: Is there any exception to this rule? 
No exceptions. Our rules apply to all traders equally to maintain a fair and level playing field. 
   Giveaway Accounts – FAQ (Forex Funds Flow) 
Q: What is a Giveaway Account? 
A Giveaway Account is a free funded account awarded through promotions, contests, or special campaigns run by Forex Funds Flow. These accounts allow traders to experience our platform and showcase their skills without paying for a challenge. 
Q: Are profits from Giveaway Accounts withdrawable? 
Yes, but with limitations. Profits are capped at 2.5% of the account size. This cap represents the maximum amount you can withdraw from a Giveaway Account.
Q: Why is there a 2.5% profit cap? 
The 2.5% cap ensures fairness and sustainability of our promotions. Giveaway Accounts are provided at no cost, and this cap allows traders to benefit from real rewards while maintaining balanced risk management on our side. 
Q: What happens if I make more than 2.5% profit on a Giveaway Account? 
Congratulations! However, only the first 2.5% in profit will be eligible for withdrawal. The rest will be considered as part of your performance and may qualify you for other exclusive offers or upgrades, but will not be withdrawable. 
Q: Can I scale or upgrade a Giveaway Account? 
No. Giveaway Accounts are non-scalable and non-upgradable. They are meant as a limited-time promotional opportunity. If you’re interested in scaling, we encourage you to join one of our standard challenge programs. 
Q: Can I receive multiple Giveaway Accounts? 
No. Each trader is eligible for only one Giveaway Account per promotion, and accounts are monitored for duplicate entries. Attempting to bypass this rule may lead to disqualification and account closure. 
Q: Can I combine profits from multiple Giveaway Accounts? 
No. Profits from Giveaway Accounts are individual and non-transferable. You cannot combine or merge them with other accounts or challenges. 
Q: When and how can I request a withdrawal from a Giveaway Account? 
Once you reach the 2.5% profit target and meet any trading day or lot minimums required for payout, you can request a withdrawal through our client portal. Payouts are processed within our standard timeframe (typically 12–24 hours).
Q: What if I breach a rule on a Giveaway Account? 
All standard trading rules apply. Breaching them will result in immediate disqualification with no eligibility for withdrawal, even if profits were earned. 
   Forex Funds Flow – 1-Step Challenge FAQ 
❓ What is the profit target to pass the 1-Step Challenge? 
To pass the challenge, you must achieve a 10% profit on your starting balance. Example: 
If you purchase a $10,000 account, you must grow the account to $11,000 to pass and become a funded FFF Trader. 
❓ What is the Daily Drawdown Limit? 
Your daily drawdown is capped at 4% of your starting balance, and includes both floating and closed losses. 
Example: 
On a $10,000 account, your max daily loss is $400. If your balance falls to $9,600 or lower at any point during the day, your account will be breached. 
   Note: The daily drawdown limit is always based on your starting balance, not your current equity. 
❓ How does the Trailing Drawdown (Maximum Drawdown) work? 
FFF uses a 6% trailing drawdown that moves up with your new equity highs but never moves down. 
Example: 
● Starting balance: $10,000 
● Trailing Drawdown starts at: $9,400
● If your equity hits $10,500, the new drawdown moves to $9,870 
● If your equity then falls below $9,870, your account is breached. 
   The trailing drawdown never resets downward—only upwards with new equity highs. 
❓ How long do I have to complete the challenge? 
You have unlimited time to complete the challenge. 
   However, if no trades are placed within 30 calendar days of activation, your account will be marked as inactive and automatically breached. No refunds will be issued for inactivity. 
❓ When can I request my first payout? 
Once you become a funded FFF Trader, you can request your first payout after: ● Completing at least 3 trading days, and 
● Waiting 2 weeks from your first trade execution. 
Payouts are then available bi-weekly, provided all rules are followed. 
❓ What is the minimum payout amount? 
The minimum payout you can request is $50, as long as all payout eligibility conditions are met. 
❓ Are there any trading restrictions around news events? 
Yes. You may not execute trades 5 minutes before or after high-impact (red folder) news purely to exploit spikes. 
   This includes pending orders, buy/sell limits, or preset SL/TP meant to catch volatility. ✅ You can open trades up to 5 hours before scheduled red news and hold through it. If TP hits during the news, it will count.
❓ Are grid, martingale, or doubling strategies allowed? 
No. Strategies that involve lot doubling or infinite scaling to recover losses (like martingale or grid systems) are strictly prohibited. 
❓ Is tick scalping allowed? 
No. Strategies that place ultra-fast trades (milliseconds to seconds) to exploit minor tick movements or demo environment flaws are not allowed. 
❓ Is there a minimum trade duration requirement? 
Yes. The average duration of all your trades must be at least 2 minutes. This helps ensure trades are based on strategy and not exploits. 
   Forex Funds Flow – 2-Step Challenge FAQ 
❓ What are the profit targets for the 2-Step Challenge? 
To pass the evaluation, you must meet the following profit targets while staying within risk limits: 
● Phase 1: Achieve a 10% profit 
● Phase 2: Achieve a 5% profit 
Example (on a $50,000 account): 
● Phase 1 Target: Grow from $50,000 → $55,000 
● Phase 2 Target: Grow from $50,000 → $52,500 
Once both phases are passed successfully, you’ll become a funded FFF Trader.
❓ What is the Daily Drawdown Limit? 
Your account cannot lose more than 4% of the starting balance in a single trading day. This includes both closed and open (floating) losses. 
Example: 
● On a $50,000 account, your daily loss limit is $2,000. 
● If your equity falls below $48,000 at any time during the day, your account will be breached. 
   This limit is always based on the initial balance, not your current or increased balance. 
❓ What is the Maximum Drawdown? 
The maximum total loss you can incur is 12% of the starting balance. 
Example: 
● On a $50,000 account, your max loss is $6,000. 
● If your equity or balance drops to $44,000 at any time (even across multiple days), your account will be breached. 
✅ Unlike the trailing drawdown in the 1-Step Challenge, the 2-Step Challenge uses a fixed drawdown that does not move up. 
❓ How long do I have to complete each phase? 
You have unlimited time to complete both Phase 1 and Phase 2. 
   However, if no trades are placed within 30 calendar days of activation, the account will be automatically breached due to inactivity. No refunds will be issued. 
❓ Are there any rules around news trading? 
Yes. Traders are prohibited from executing trades 5 minutes before or after high-impact (red folder) news purely to exploit spikes.
   This includes setting pending orders, limits, SLs, or TPs near news for quick scalps. ✅ You may open trades 5 hours before the news and hold through it. If your take profit hits during news volatility, the trade will count. 
❓ Are grid or martingale strategies allowed? 
No. Any strategy that involves lot doubling, infinite scaling, or gambling-style recovery methods is strictly not allowed. 
❓ Is tick scalping permitted? 
No. Placing trades that enter and exit within milliseconds or a few seconds just to exploit small price movements or demo environment behavior is prohibited. 
❓ What is the minimum trade duration? 
The average duration of all trades must be at least 2 minutes. 
Trades below this time may be flagged and disqualified. 
Your daily drawdown is capped at 5% of the starting balance, and applies to both closed and open (floating) losses. 
Example:
● If you have a $10,000 account, your daily loss limit is $500. 
● If your account drops to $9,500 or below on any given trading day (including floating losses), your account will be breached. 
   The daily limit resets at the start of each new trading day. 


   Weekend Holding 
Weekend holding is not allowed unless you’ve purchased a specific Add-on. All trades must be closed by 4:59 PM EST on Friday. 
   News Trading Policy 
Trading 5 minutes before or after high-impact news events to exploit spikes is strictly prohibited. 
This includes placing pending orders, limits, SLs, or TPs around news releases. 
✅ However, you may open trades up to 5 hours before a red folder news event and hold through it. If your TP is hit, the trade will be valid. 
⚙ Prohibited Trading Strategies 
❌ Grid or Martingale 
No lot doubling or infinite scaling systems that rely on reversals rather than risk management. ❌ Tick Scalping or Platform Exploits 
No ultra-short-term trades (milliseconds to a few seconds) that attempt to exploit minor price ticks or demo environment weaknesses. 
⏱ Minimum Trade Duration 
The average duration of all trades must be at least 2 minutes. 
⚠ Repeated violations of this rule will lead to disqualification. 
⚙ Prohibited Trading Strategies 
❌ Grid or Martingale 
No use of lot doubling, infinite recovery tactics, or systems based on reversals without risk control. 
❌ Tick Scalping / Platform Exploits 
Trades placed for a few seconds or to exploit system flaws are not permitted. 
⏱ Minimum Trade Duration 
The average duration of all trades must be at least 2 minutes. 
Consistent violations may lead to disqualification.

📌 FFF Boost Program – Frequently Asked Questions
1. What is the FFF Boost Program?
FFF Boost is our elite payout-focused funding program designed for active traders who want
frequent payouts, fair trading conditions, and scalable rewards based on consistency —
not rigid rules.
2. How often do I get paid?
Traders under FFF Boost receive payouts every 3 days (yes, seriously). No more waiting
weeks or months for your performance to pay off.
3. What are the trading rules under FFF Boost?
● Minimum trading days: 3
● No consistency rule (You can hit target in a day if you want)
● No trailing drawdown
● Static drawdown: 3% max
● News trading restriction:
○ No trades 5 minutes before or after news
○ You can open a position 5 hours before the news and hold through (ideal for
swing traders)
4. What’s the profit split structure?
● Starts at 65%
● Increases to 70% after 3 successful payouts
● 75% after 6 payouts● 80% after 9 payouts
The more you withdraw, the more you keep.
5. Is there a minimum withdrawal amount?
Yes. You must reach $50 in profit before requesting a payout.
6. Are there any restrictions on holding trades overnight or over the
weekend?
There are no restrictions on holding trades overnight. However, you
can’t hold trades over the weekend if you haven’t purchased the
weekend add-on
7. Are there any hidden rules or gimmicks?
No. There’s no trailing drawdown, no minimum lot size, no scaling requirement, and no
consistency rule. Just trade and get paid.
8. What account sizes are available and what are the fees?
● $2,500 account – $50
● $5,000 account – $100
● $10,000 account – $200
More sizes may be introduced as the program expands.
9. Can I swing trade with FFF Boost?
Yes. Swing trading is allowed. You can open trades up to 5 hours before major news
events and hold through, as long as the entry time complies.10. How do I qualify for FFF Boost?
You can join by purchasing a FFF Boost account from our platform. It's not invite-only, but
early access is limited.
11. Is this available internationally?
Yes. FFF Boost is available to traders worldwide, subject to our general compliance
requirements.
12. How is this different from other prop firm programs?
● 3-day payouts
● No trailing drawdown
● Profit split upgrades based on your withdrawal record
● No unnecessary restrictions
● Clear, trader-first structure
It’s built by traders, for traders. No fluff. Just funding and freedom.
13. How many accounts can I buy?
You can purchase accounts totaling up to $100,000 in funding.
14. Is copy trading allowed?
● ✅ Copy trading is allowed on a maximum of 2 accounts only
If you have more than 2 accounts, the remaining ones must be traded
independently, using different markets or strategies.
● 🚫 Copying across more than 2 accounts is strictly prohibited.
Violating this rule will lead to immediate disqualification from the program and
forfeiture of any earnings.


VIP PLAN

For the VIP plan, kindly visit https://www.forexfundsflow.com/en/vip-plan for detailed information
"""

# TARGET_CHANNEL_ID = 1411391065264754740

# async def ask_gemini(prompt):
#     response = model.generate_content(FAQ_CONTEXT + "\nUser: " + prompt)
#     return response.text

user_histories = defaultdict(list)


async def ask_gemini(user_id, prompt):
   # Add the new user message to history
   user_histories[user_id].append(f"User: {prompt}")

   # Limit history to last 6 exchanges (to prevent token overflow)
   history = "\n".join(user_histories[user_id][-12:])

   # Build the prompt with context and history
   full_prompt = FAQ_CONTEXT + "\n" + history + "\nAI:"

   response = model.generate_content(full_prompt)

   # Save AI response to history
   user_histories[user_id].append(f"AI: {response.text}")

   return response.text


@bot.event
async def on_ready():
   print(f"Discord bot ready as {bot.user.name}")


@bot.event
async def on_message(message):
   if message.author == bot.user:
      return
   if bot.user.mentioned_in(message):
      user_q = message.content
      answer = await ask_gemini(message.author.id, user_q)
      # await message.channel.send(answer)
      await message.reply(answer, mention_author=True)
   await bot.process_commands(message)

keep_alive()

bot.run(DISCORD_TOKEN)
